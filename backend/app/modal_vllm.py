"""
Modal deployment for vLLM serving Qwen 2.5 32B Instruct.
"""
import os
import modal
from fastapi import Request

MODEL_ID = os.getenv("VLLM_MODEL_ID", "Qwen/Qwen2.5-3B-Instruct")
MODEL_REVISION = "main"
# Modal deprecation: prefer the string GPU selector.
GPU_CONFIG = os.getenv("MODAL_GPU", "A100-40GB")

vllm_image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install(
        "vllm==0.6.3.post1",
        "fastapi[standard]",
        "huggingface_hub",
        "hf_transfer",
        "transformers",
    )
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"})
    .env({"PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"})
)

app = modal.App("qwen-2-5-32b-vllm")
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
    model_ready: bool = False

    @modal.enter()
    async def start_engine(self):
        from vllm.engine.arg_utils import AsyncEngineArgs
        from vllm.engine.async_llm_engine import AsyncLLMEngine
        from transformers import AutoTokenizer

        self.model_ready = False
        print(f"🚀 Loading model {MODEL_ID}...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_ID,
            revision=MODEL_REVISION,
            cache_dir=CACHE_DIR,
        )

        requested_len = int(os.getenv("VLLM_MAX_MODEL_LEN", "32768"))
        # Qwen2.5-3B-Instruct derives 32k max from config; keep a safe default.
        if requested_len > 32768 and os.getenv("VLLM_ALLOW_LONG_MAX_MODEL_LEN") != "1":
            print(
                f"⚠️ VLLM_MAX_MODEL_LEN={requested_len} exceeds model config; clamping to 32768. "
                "Set VLLM_ALLOW_LONG_MAX_MODEL_LEN=1 to override (not recommended unless you know it's safe)."
            )
            requested_len = 32768

        engine_args = AsyncEngineArgs(
            model=MODEL_ID,
            revision=MODEL_REVISION,
            tensor_parallel_size=1,
            max_model_len=requested_len,
            gpu_memory_utilization=float(os.getenv("VLLM_GPU_MEMORY_UTILIZATION", "0.90")),
            dtype=os.getenv("VLLM_DTYPE", "auto"),
            enforce_eager=False,
            enable_prefix_caching=False,
            download_dir=CACHE_DIR,
            disable_log_stats=False,
        )
        # Using the standard AsyncLLMEngine.from_engine_args is correct, 
        # but we need to ensure we don't accidentally close the loop.
        # Ensure the engine loop is created on the active event loop.
        self.engine = AsyncLLMEngine.from_engine_args(engine_args)
        self.model_ready = True
        print("✅ Model loaded successfully!")

    @modal.fastapi_endpoint(method="GET")
    async def status(self):
        return {"loaded": self.model_ready, "model": MODEL_ID}

    @modal.fastapi_endpoint(method="POST")
    async def chat(self, request: Request):
        import uuid
        import traceback
        from vllm import SamplingParams

        try:
            body = await request.json()
            messages = body.get("messages", [])
            temperature = body.get("temperature", 0.1)
            max_tokens = min(body.get("max_tokens", 1024), 1024)  # Short output for JSON

            print(f"🔹 Processing {len(messages)} messages...")

            # Build prompt from messages (system prompt comes from backend)
            prompt = self._build_prompt(messages)

            stop_tokens = []
            eos_token = getattr(getattr(self, "tokenizer", None), "eos_token", None)
            if isinstance(eos_token, str) and eos_token:
                stop_tokens.append(eos_token)
            stop_tokens.extend(["<|eot_id|>", "<|im_end|>"])

            sampling_params = SamplingParams(
                temperature=temperature, 
                max_tokens=max_tokens,
                stop=stop_tokens or None,
                repetition_penalty=1.1,
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
        tokenizer = getattr(self, "tokenizer", None)
        if tokenizer is not None and hasattr(tokenizer, "apply_chat_template"):
            return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

        prompt_parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt_parts.append(f"<|im_start|>{role}\n{content}<|im_end|>")
        prompt_parts.append("<|im_start|>assistant\n")
        return "\n".join(prompt_parts)
