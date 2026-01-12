"""Open-source LLM integration for generating ENTSO-E requests."""

from __future__ import annotations

import os
from typing import Dict, List

import requests

from backend.app.llm_context import build_context
from backend.app.llm_utils import LLMError, LLMResponse, extract_json, parse_requests


DEFAULT_OSS_MODEL = "meta-llama/Meta-Llama-3.1-70B-Instruct"
DEFAULT_OSS_BASE_URL = "http://localhost:8000/v1"


def _resolve_endpoint(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if normalized.endswith("/chat/completions"):
        return normalized
    if normalized.endswith("/v1"):
        return f"{normalized}/chat/completions"
    return f"{normalized}/v1/chat/completions"


def generate_requests(message: str, history: List[Dict[str, str]] | None = None) -> LLMResponse:
    base_url = os.getenv("OSS_LLM_BASE_URL", DEFAULT_OSS_BASE_URL)
    endpoint = _resolve_endpoint(base_url)
    api_key = os.getenv("OSS_LLM_API_KEY")
    model = os.getenv("OSS_LLM_MODEL", DEFAULT_OSS_MODEL)
    system_prompt = build_context(message, history)

    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": message})

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    response = requests.post(
        endpoint,
        headers=headers,
        json={
            "model": model,
            "messages": messages,
            "response_format": {"type": "json_object"},
            "temperature": 0.1,
        },
        timeout=120,
    )

    if response.status_code != 200:
        raise LLMError(f"Open-source LLM API error: {response.status_code} {response.text}")

    data = response.json()
    content = data["choices"][0]["message"]["content"]
    parsed = extract_json(content)
    requests_list = parse_requests(parsed)

    return LLMResponse(requests=requests_list, raw_message=content)
