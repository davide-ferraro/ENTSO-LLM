"""LLM integration for generating ENTSO-E requests."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List

import requests

from backend.app.prompts import load_system_prompt


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class LLMResponse:
    requests: List[Dict[str, Any]]
    raw_message: str


class LLMError(RuntimeError):
    """Raised when the LLM fails to produce valid requests."""


def _parse_requests(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    if "requests" in payload:
        requests_list = payload.get("requests")
    elif "request" in payload:
        requests_list = [payload.get("request")]
    elif "params" in payload:
        requests_list = [
            {
                "name": payload.get("name", "request"),
                "params": payload.get("params"),
            }
        ]
    else:
        raise LLMError("LLM response must include 'requests', 'request', or 'params'.")

    if not isinstance(requests_list, list) or not requests_list:
        raise LLMError("LLM response 'requests' must be a non-empty list.")

    normalized: List[Dict[str, Any]] = []
    for item in requests_list:
        if not isinstance(item, dict):
            raise LLMError("Each request entry must be a JSON object.")
        params = item.get("params")
        if not isinstance(params, dict):
            raise LLMError("Each request entry must include a 'params' object.")
        normalized.append({"name": item.get("name", "request"), "params": params})

    return normalized


def _extract_json(content: str) -> Dict[str, Any]:
    try:
        return json.loads(content)
    except json.JSONDecodeError as exc:
        raise LLMError(f"LLM response was not valid JSON: {exc}") from exc


def generate_requests(message: str, history: List[Dict[str, str]] | None = None) -> LLMResponse:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise LLMError("OPENAI_API_KEY is not set.")

    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    system_prompt = load_system_prompt()

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
    parsed = _extract_json(content)
    requests_list = _parse_requests(parsed)

    return LLMResponse(requests=requests_list, raw_message=content)
