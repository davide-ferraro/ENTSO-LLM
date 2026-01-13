"""Shared helpers for LLM-backed request generation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass(frozen=True)
class LLMResponse:
    requests: List[Dict[str, Any]]
    raw_message: str
    router_endpoints: List[str]


class LLMError(RuntimeError):
    """Raised when the LLM fails to produce valid requests."""


def parse_requests(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
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


def extract_json(text: str) -> Dict[str, Any]:
    """Extract JSON from text, handling markdown blocks."""
    text = text.strip()
    # Robustly find the JSON object using regex
    # asking for non-greedy match of dotall
    import re
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        text = match.group(1)
    
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"❌ JSON PARSE ERROR. Content attempting to parse:\n{text}\n")
        raise LLMError(f"Invalid JSON received from LLM: {exc}. Content: {text[:500]}") from exc
