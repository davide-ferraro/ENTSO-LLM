"""Gemini integration for routing and request generation."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Tuple

import google.generativeai as genai

from backend.app.llm_context import build_generator_context, build_router_context
from backend.app.llm_utils import LLMError, LLMResponse, extract_json, parse_requests


def _get_model() -> genai.GenerativeModel:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise LLMError("GEMINI_API_KEY is not set.")
    genai.configure(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    return genai.GenerativeModel(model_name)


def _call_model(prompt: str, temperature: float = 0.1) -> str:
    model = _get_model()
    try:
        response = model.generate_content(
            prompt,
            generation_config={"temperature": temperature},
        )
    except Exception as exc:  # pragma: no cover - external call
        raise LLMError(f"Gemini API error: {exc}") from exc

    if not response or not response.text:
        raise LLMError("Empty response from Gemini.")
    return response.text


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


def router_pass(message: str) -> List[str]:
    router_context = build_router_context(message)
    prompt = f"{router_context}\n\nUser request:\n{message}\n\nReturn JSON with an 'endpoints' array."
    router_response = _call_model(prompt, temperature=0.1)
    return _parse_router_response(router_response)


def generator_pass(
    message: str,
    history: List[Dict[str, str]] | None,
    selected_endpoints: List[str],
) -> Tuple[List[Dict[str, Any]], str]:
    generator_context = build_generator_context(message, selected_endpoints)
    history_text = ""
    if history:
        history_text = "\n\nPrevious messages:\n" + "\n".join(
            [f"- {msg.get('role')}: {msg.get('content')}" for msg in history]
        )
    prompt = f"{generator_context}{history_text}"
    generator_response = _call_model(prompt, temperature=0.2)
    parsed = extract_json(generator_response)
    requests_list = parse_requests(parsed)
    return requests_list, generator_response


def generate_requests(message: str, history: List[Dict[str, str]] | None = None) -> LLMResponse:
    selected_endpoints = router_pass(message)
    requests_list, content = generator_pass(message, history, selected_endpoints)
    return LLMResponse(
        requests=requests_list,
        raw_message=content,
        router_endpoints=selected_endpoints,
    )
