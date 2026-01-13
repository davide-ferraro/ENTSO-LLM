"""
Modal deployment for vLLM serving Qwen2.5-7B-Instruct.
"""
import modal
from fastapi import FastAPI, Request

MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
MODEL_REVISION = "main"
GPU_CONFIG = "L4"

vllm_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "vllm==0.6.3.post1",
        "fastapi[standard]",
        "huggingface_hub",
        "hf_transfer",
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
)

app = modal.App("qwen-7b-vllm")
model_cache = modal.Volume.from_name("llm-model-cache", create_if_missing=True)
CACHE_DIR = "/root/.cache/huggingface"

@app.cls(
    image=vllm_image,
    gpu=GPU_CONFIG,
    timeout=3600,
    scaledown_window=300,
    volumes={CACHE_DIR: model_cache},
)
class VLLMServer:
    @modal.enter()
    def start_engine(self):
        from vllm.engine.arg_utils import AsyncEngineArgs
        from vllm.engine.async_llm_engine import AsyncLLMEngine

        print(f"🚀 Loading model {MODEL_ID}...")
        engine_args = AsyncEngineArgs(
            model=MODEL_ID,
            revision=MODEL_REVISION,
            tensor_parallel_size=1,
            max_model_len=16384,
            gpu_memory_utilization=0.95,
            enforce_eager=False,
            enable_prefix_caching=True,
            download_dir=CACHE_DIR,
            disable_log_stats=False,
        )
        # Using the standard AsyncLLMEngine.from_engine_args is correct, 
        # but we need to ensure we don't accidentally close the loop.
        self.engine = AsyncLLMEngine.from_engine_args(engine_args)
        print("✅ Model loaded successfully!")

    @modal.fastapi_endpoint(method="POST")
    async def chat(self, request: Request):
        import uuid
        import traceback
        from vllm import SamplingParams

        try:
            body = await request.json()
            messages = body.get("messages", [])
            temperature = body.get("temperature", 0.1)
            # Ensure max_tokens is reasonable
            max_tokens = min(body.get("max_tokens", 4096), 2048)

            print(f"🔹 Processing {len(messages)} messages...")

            # Enforce JSON in the prompt itself
            system_msg = "You are a helpful assistant. You must respond with valid JSON only. Do not use markdown blocks."
            if not any(m.get("role") == "system" for m in messages):
                messages.insert(0, {"role": "system", "content": system_msg})

            prompt = self._build_prompt(messages)
            if body.get("response_format", {}).get("type") == "json_object":
                prompt += "\n\nRespond with valid JSON only."

            sampling_params = SamplingParams(
                temperature=temperature, 
                max_tokens=max_tokens,
                stop=["<|im_end|>"]  # Explicitly stop to avoid run-on
            )
            request_id = str(uuid.uuid4())

            # Use the engine's generate method properly
            # We iterate asynchronously over the generator
            results_generator = self.engine.generate(prompt, sampling_params, request_id)
            
            final_output = None
            async for output in results_generator:
                if await request.is_disconnected():
                    # Abort if client disconnects
                    await self.engine.abort(request_id)
                    return {"error": "Client disconnected"}
                final_output = output
            
            if final_output is None:
                raise ValueError("No output generated")

            generated_text = final_output.outputs[0].text
            return {
                "choices": [{"message": {"role": "assistant", "content": generated_text}}]
            }
        except Exception as e:
            print(f"❌ Error in chat endpoint: {e}")
            traceback.print_exc()
            # Return a 500 with the error message so the client sees it
            from fastapi import Response
            return Response(content=f"Internal Server Error: {str(e)}", status_code=500)

    def _build_prompt(self, messages: list) -> str:
        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt_parts.append(f"<|im_start|>{role}\n{content}<|im_end|>")
        prompt_parts.append("<|im_start|>assistant\n")
        return "\n".join(prompt_parts)
