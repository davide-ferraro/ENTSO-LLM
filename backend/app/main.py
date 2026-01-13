"""FastAPI service for ENTSO-LLM chat requests."""

from __future__ import annotations

from pathlib import Path
import os
from typing import Any, Dict, List

import asyncio
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

# Load environment variables from backend/.env
env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)


from backend.app.database import (
    add_file,
    add_message,
    get_conversation,
    get_file,
    init_db,
    list_conversations,
    list_files,
    list_messages,
    create_conversation,
)
from backend.app.entsoe import EntsoeError, run_requests
from backend.app.llm import LLMError, generate_requests, generator_pass, router_pass
from backend.app.models import (
    ChatRequest,
    ChatResponse,
    ConversationDetail,
    ConversationSummary,
    FileLink,
    MessageRecord,
    RequestResult,
)
from backend.app.storage import RESULTS_DIR, StoredFile, ensure_storage, get_storage_backend, register_files
from backend.app.llm_open_source import (
    generator_pass as generator_pass_oss,
    get_model_status as get_model_status_oss,
    router_pass as router_pass_oss,
)

app = FastAPI(title="ENTSO-LLM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup() -> None:
    # Double check env is loaded on startup if needed, 
    # but top-level load_dotenv is usually sufficient.
    ensure_storage()
    init_db()


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


def _register_result_files(
    results: List[Dict[str, Any]],
    conversation_id: str,
) -> List[Dict[str, str]]:
    all_files: List[Dict[str, str]] = []
    for result in results:
        for file_entry in result.get("files", []):
            all_files.append(file_entry)

    storage_backend = get_storage_backend()
    stored_files = register_files(all_files, storage_backend, conversation_id)

    file_links: List[Dict[str, str]] = []
    for stored in stored_files:
        record = add_file(
            conversation_id=conversation_id,
            name=stored["name"],
            file_type=stored["type"],
            storage_key=stored["storage_key"],
            local_path=stored.get("local_path"),
        )
        file_links.append(
            {
                "id": record.id,
                "type": record.type,
                "name": record.name,
                "url": f"/files/{record.id}",
                "created_at": record.created_at,
                "storage_key": record.storage_key,
                "local_path": record.local_path,
            }
        )

    return file_links


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        llm_response = generate_requests(
            request.message,
            history=[msg.model_dump() for msg in request.history or []],
        )
    except LLMError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        execution = run_requests(llm_response.requests)
    except EntsoeError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    conversation = create_conversation(llm_response.requests)
    add_message(conversation.id, "user", request.message)
    add_message(conversation.id, "assistant", llm_response.raw_message)

    files = _register_result_files(execution["results"], conversation.id)

    results: List[RequestResult] = []
    for result in execution["results"]:
        linked_files: List[FileLink] = []
        for file_entry in result.get("files", []):
            for link in files:
                if Path(file_entry["path"]).resolve() == Path(link["local_path"]).resolve():
                    linked_files.append(FileLink(**{k: v for k, v in link.items() if k not in {"storage_key", "local_path"}}))
        # Prevent "got multiple values for keyword argument 'files'"
        # by excluding it from the unpacked result dict
        result_data = {k: v for k, v in result.items() if k != "files"}
        results.append(RequestResult(**result_data, files=linked_files))

    return ChatResponse(
        conversation_id=conversation.id,
        request_payload=llm_response.requests,
        router_endpoints=llm_response.router_endpoints,
        results=results,
        summary=execution["summary"],
        files=[
            FileLink(**{k: v for k, v in link.items() if k not in {"storage_key", "local_path"}})
            for link in files
        ],
        llm_message=llm_response.raw_message,
    )


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    async def event_stream():

        def send_event(event: str, payload: Dict[str, Any]) -> str:
            return f"event: {event}\ndata: {json.dumps(payload)}\n\n"


        def normalize_results(llm_response: Dict[str, Any], execution: Dict[str, Any]) -> Dict[str, Any]:
            conversation = create_conversation(llm_response["requests"])
            add_message(conversation.id, "user", request.message)
            add_message(conversation.id, "assistant", llm_response["raw_message"])

            files = _register_result_files(execution["results"], conversation.id)

            results: List[RequestResult] = []
            for result in execution["results"]:
                linked_files: List[FileLink] = []
                for file_entry in result.get("files", []):
                    for link in files:
                        if Path(file_entry["path"]).resolve() == Path(link["local_path"]).resolve():
                            linked_files.append(
                                FileLink(**{k: v for k, v in link.items() if k not in {"storage_key", "local_path"}})
                            )
                result_data = {k: v for k, v in result.items() if k != "files"}
                results.append(RequestResult(**result_data, files=linked_files))

            return {
                "conversation_id": conversation.id,
                "request_payload": llm_response["requests"],
                "router_endpoints": llm_response["router_endpoints"],
                "results": [result.model_dump() for result in results],
                "summary": execution["summary"],
                "files": [
                    FileLink(**{k: v for k, v in link.items() if k not in {"storage_key", "local_path"}}).model_dump()
                    for link in files
                ],
                "llm_message": llm_response["raw_message"],
            }

        try:
            history_payload = [msg.model_dump() for msg in request.history or []]
            provider = os.getenv("LLM_PROVIDER", "openai").lower()
            if provider in {"oss", "open-source", "open_source", "open"}:
                model_name = os.getenv("OSS_LLM_MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")
            else:
                model_name = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

            if provider in {"oss", "open-source", "open_source", "open"}:
                status_task = asyncio.create_task(asyncio.to_thread(get_model_status_oss))
                model_ready: bool | None = None
                try:
                    model_ready = await asyncio.wait_for(status_task, timeout=0.5)
                except asyncio.TimeoutError:
                    yield send_event(
                        "status",
                        {"message": f"Loading {model_name} for the first time"},
                    )
                    await asyncio.sleep(0)
                    model_ready = await status_task

                if model_ready is None:
                    yield send_event("status", {"message": "Finding the right endpoint"})
                    await asyncio.sleep(0)
                elif not model_ready:
                    yield send_event(
                        "status",
                        {"message": f"Loading {model_name} for the first time"},
                    )
                    await asyncio.sleep(0)
                    yield send_event("status", {"message": "Finding the right endpoint"})
                    await asyncio.sleep(0)
                else:
                    yield send_event("status", {"message": "Finding the right endpoint"})
                    await asyncio.sleep(0)
            else:
                yield send_event("status", {"message": "Finding the right endpoint"})
                await asyncio.sleep(0)

            if provider in {"oss", "open-source", "open_source", "open"}:
                selected_endpoints = await asyncio.to_thread(router_pass_oss, request.message)
            else:
                selected_endpoints = await asyncio.to_thread(router_pass, request.message)

            yield send_event("router", {"endpoints": selected_endpoints})
            await asyncio.sleep(0)
            yield send_event("status", {"message": "Writing the request"})
            await asyncio.sleep(0)

            if provider in {"oss", "open-source", "open_source", "open"}:
                requests_list, raw_message = await asyncio.to_thread(
                    generator_pass_oss, request.message, selected_endpoints
                )
            else:
                requests_list, raw_message = await asyncio.to_thread(
                    generator_pass, request.message, history_payload, selected_endpoints
                )

            llm_response = {
                "requests": requests_list,
                "raw_message": raw_message,
                "router_endpoints": selected_endpoints,
            }

            yield send_event("request", {"request_payload": requests_list})
            await asyncio.sleep(0)
            yield send_event("status", {"message": "Connecting to ENTSO-E APIs"})
            await asyncio.sleep(0)

            execution = await asyncio.to_thread(run_requests, requests_list)
            payload = normalize_results(llm_response, execution)
            yield send_event("results", payload)
            await asyncio.sleep(0)
            yield send_event("done", {"message": "complete"})
        except LLMError as exc:
            yield send_event("error", {"detail": str(exc)})
        except EntsoeError as exc:
            yield send_event("error", {"detail": str(exc)})
        except Exception as exc:
            yield send_event("error", {"detail": str(exc)})

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/conversations", response_model=List[ConversationSummary])
async def get_conversations() -> List[ConversationSummary]:
    return [ConversationSummary(id=conv.id, created_at=conv.created_at) for conv in list_conversations()]


@app.get("/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation_detail(conversation_id: str) -> ConversationDetail:
    conversation = get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    messages = [
        MessageRecord(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            created_at=msg.created_at,
        )
        for msg in list_messages(conversation_id)
    ]

    files = [
        FileLink(id=file.id, type=file.type, name=file.name, url=f"/files/{file.id}", created_at=file.created_at)
        for file in list_files(conversation_id)
    ]

    return ConversationDetail(
        id=conversation.id,
        created_at=conversation.created_at,
        request_payload=conversation.request_payload,
        messages=messages,
        files=files,
    )


@app.get("/files/{file_id}")
async def get_file_link(file_id: str):
    record = get_file(file_id)
    if not record:
        raise HTTPException(status_code=404, detail="File not found")

    storage_backend = get_storage_backend()
    if record.local_path:
        path = Path(record.local_path).resolve()
        if not path.exists() or not path.is_file():
            raise HTTPException(status_code=404, detail="File missing on disk")
        try:
            if not path.is_relative_to(RESULTS_DIR):
                raise HTTPException(status_code=403, detail="File access denied")
        except AttributeError:
            if str(RESULTS_DIR) not in str(path):
                raise HTTPException(status_code=403, detail="File access denied")

    stored_file = StoredFile(
        storage_key=record.storage_key,
        local_path=Path(record.local_path) if record.local_path else None,
    )
    return storage_backend.get_file_response(stored_file=stored_file, filename=record.name)
