"""FastAPI service for ENTSO-LLM chat requests."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from backend.app.entsoe import EntsoeError, run_requests
from backend.app.llm import LLMError, generate_requests
from backend.app.models import ChatRequest, ChatResponse, FileLink, RequestResult
from backend.app.storage import resolve_file, register_files

app = FastAPI(title="ENTSO-LLM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/health")
async def health() -> Dict[str, str]:
    return {"status": "ok"}


def _register_result_files(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    all_files: List[Dict[str, str]] = []
    for result in results:
        for file_entry in result.get("files", []):
            all_files.append(file_entry)
    return register_files(all_files)


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

    files = _register_result_files(execution["results"])

    results: List[RequestResult] = []
    for result in execution["results"]:
        linked_files: List[FileLink] = []
        for file_entry in result.get("files", []):
            for link in files:
                if Path(file_entry["path"]).resolve() == Path(link["path"]).resolve():
                    linked_files.append(FileLink(**{k: v for k, v in link.items() if k != "path"}))
        results.append(RequestResult(**result, files=linked_files))

    return ChatResponse(
        request_payload=llm_response.requests,
        results=results,
        summary=execution["summary"],
        files=[FileLink(**{k: v for k, v in link.items() if k != "path"}) for link in files],
        llm_message=llm_response.raw_message,
    )


@app.get("/files/{file_id}")
async def get_file(file_id: str):
    entry = resolve_file(file_id)
    if not entry:
        raise HTTPException(status_code=404, detail="File not found")

    path = Path(entry["path"]).resolve()
    if not path.exists() or not path.is_file():
        raise HTTPException(status_code=404, detail="File missing on disk")
    try:
        if not path.is_relative_to(Path(__file__).resolve().parents[1] / "storage" / "results"):
            raise HTTPException(status_code=403, detail="File access denied")
    except AttributeError:
        results_root = Path(__file__).resolve().parents[1] / "storage" / "results"
        if str(results_root) not in str(path):
            raise HTTPException(status_code=403, detail="File access denied")

    return FileResponse(path, filename=entry.get("name"))
