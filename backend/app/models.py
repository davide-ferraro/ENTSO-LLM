"""Pydantic models for the backend API."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., examples=["user", "assistant"])
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    history: Optional[List[ChatMessage]] = None


class FileLink(BaseModel):
    id: str
    type: str
    name: str
    url: str


class RequestResult(BaseModel):
    name: str
    success: bool
    status_code: Optional[int] = None
    summary: Dict[str, Any]
    error: Optional[str] = None
    api_message: Optional[str] = None
    files: List[FileLink] = []
    is_historical: Optional[bool] = None
    chunks_total: Optional[int] = None
    chunks_success: Optional[int] = None
    chunks_with_data: Optional[int] = None
    csv_info: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    request_payload: List[Dict[str, Any]]
    results: List[RequestResult]
    summary: Dict[str, Any]
    files: List[FileLink]
    llm_message: str
