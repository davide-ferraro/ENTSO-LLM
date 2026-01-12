"""LLM integration for generating ENTSO-E requests."""

from __future__ import annotations

import os
from typing import Dict, List

import requests

from backend.app.llm_context import build_context
from backend.app.llm_utils import LLMError, LLMResponse, extract_json, parse_requests
from backend.app.llm_open_source import generate_requests as generate_requests_open_source


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o-mini"


def generate_requests(message: str, history: List[Dict[str, str]] | None = None) -> LLMResponse:
    provider = os.getenv("LLM_PROVIDER", "openai").lower()
    if provider in {"oss", "open-source", "open_source", "open"}:
        return generate_requests_open_source(message, history=history)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise LLMError("OPENAI_API_KEY is not set.")

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    system_prompt = build_context(message, history)

    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": message})

    response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": messages,
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        },
        timeout=120,
    )

    if response.status_code != 200:
        raise LLMError(f"OpenAI API error: {response.status_code} {response.text}")

    data = response.json()
    content = data["choices"][0]["message"]["content"]
    parsed = extract_json(content)
    requests_list = parse_requests(parsed)

    return LLMResponse(requests=requests_list, raw_message=content)
