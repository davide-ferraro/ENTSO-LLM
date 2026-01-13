"""LLM integration for generating ENTSO-E requests."""

from __future__ import annotations

import os
from typing import Any, Dict, List

import requests

from backend.app.llm_context import build_generator_context, build_router_context
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

    router_context = build_router_context(message)
    router_messages = [
        {"role": "system", "content": router_context},
        {"role": "user", "content": message},
    ]

    router_response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": router_messages,
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        },
        timeout=120,
    )

    if router_response.status_code != 200:
        raise LLMError(f"OpenAI API error: {router_response.status_code} {router_response.text}")

    router_content = router_response.json()["choices"][0]["message"]["content"]
    selected_endpoints = _parse_router_response(router_content)

    generator_context = build_generator_context(message, selected_endpoints)
    generator_messages = [{"role": "system", "content": generator_context}]
    if history:
        generator_messages.extend(history)
    generator_messages.append({"role": "user", "content": message})

    generator_response = requests.post(
        OPENAI_API_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "model": model,
            "messages": generator_messages,
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        },
        timeout=120,
    )
    
    if generator_response.status_code != 200:
        raise LLMError(f"OpenAI API error: {generator_response.status_code} {generator_response.text}")

    content = generator_response.json()["choices"][0]["message"]["content"]
    parsed = extract_json(content)
    requests_list = parse_requests(parsed)

    return LLMResponse(
        requests=requests_list,
        raw_message=content,
        router_endpoints=selected_endpoints,
    )


def _parse_router_response(content: str) -> List[str]:
    try:
        parsed = extract_json(content)
        endpoints = parsed.get("endpoints", [])
        if endpoints:
            return endpoints
    except Exception:
        pass

    import re

    matches = re.findall(r"E\d+", content)
    if matches:
        return matches[:2]
    return ["E10"]
