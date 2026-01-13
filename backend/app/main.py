"""FastAPI service for ENTSO-LLM chat requests."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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
from backend.app.llm import LLMError, generate_requests
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
        results=results,
        summary=execution["summary"],
        files=[
            FileLink(**{k: v for k, v in link.items() if k not in {"storage_key", "local_path"}})
            for link in files
        ],
        llm_message=llm_response.raw_message,
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
