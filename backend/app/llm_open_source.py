"""Open-source LLM integration for generating ENTSO-E requests.

Uses a Two-Pass architecture:
1. Router Pass: LLM selects the relevant endpoint(s)
2. Generator Pass: LLM generates JSON using selected endpoint examples
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional, Tuple

import requests

from backend.app.llm_context import build_router_context, build_generator_context
from backend.app.llm_utils import LLMError, LLMResponse, extract_json, parse_requests


DEFAULT_OSS_MODEL = "meta-llama/Meta-Llama-3.1-70B-Instruct"
DEFAULT_OSS_BASE_URL = "http://localhost:8000/v1"


def _resolve_endpoint(base_url: str) -> str:
    """Resolve the LLM API endpoint URL."""
    normalized = base_url.rstrip("/")
    if "modal.run" in normalized:
        return normalized
    if normalized.endswith("/chat/completions"):
        return normalized
    if normalized.endswith("/v1"):
        return f"{normalized}/chat/completions"
    return f"{normalized}/v1/chat/completions"


def _resolve_status_endpoint(base_url: str) -> str:
    normalized = base_url.rstrip("/")
    if normalized.endswith("/chat"):
        normalized = normalized[: -len("/chat")]
    if normalized.endswith("/chat/completions"):
        normalized = normalized[: -len("/chat/completions")]
    if normalized.endswith("/v1"):
        normalized = normalized[: -len("/v1")]
    return f"{normalized}/status"


def _call_llm(endpoint: str, headers: dict, messages: List[Dict[str, str]], temperature: float = 0.1) -> str:
    """Make a single LLM API call and return the content."""
    print(f"🚀 Sending request to LLM Endpoint: {endpoint}")
    response = requests.post(
        endpoint,
        headers=headers,
        json={
            "messages": messages,
            "temperature": temperature,
        },
        timeout=300,
    )

    print(f"🚀 Response Status: {response.status_code}")
    if response.status_code != 200:
        print(f"❌ LLM API Error: {response.status_code} - {response.text}")
        raise LLMError(f"LLM API error: {response.status_code} {response.text}")

    data = response.json()
    print(f"🚀 Response Data Keys: {list(data.keys())}")
    return data["choices"][0]["message"]["content"]


def _parse_router_response(content: str) -> List[str]:
    """Parse the router response to extract endpoint IDs."""
    try:
        # Try to extract JSON from the response
        parsed = extract_json(content)
        endpoints = parsed.get("endpoints", [])
        if endpoints:
            return endpoints
    except Exception:
        pass
    
    # Fallback: look for E## patterns in the text
    import re
    matches = re.findall(r'E\d+', content)
    if matches:
        return matches[:2]  # Max 2 endpoints
    
    # Default fallback
    return ["E10"]


def _build_headers() -> Tuple[str, dict]:
    chat_url_override = os.getenv("OSS_LLM_CHAT_URL")
    print(f"DEBUG: OSS_LLM_CHAT_URL found: '{chat_url_override}'")
    if chat_url_override:
        endpoint = _resolve_endpoint(chat_url_override)
    else:
        base_url = os.getenv("OSS_LLM_BASE_URL", DEFAULT_OSS_BASE_URL)
        endpoint = _resolve_endpoint(base_url)
    api_key = os.getenv("OSS_LLM_API_KEY")

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    return endpoint, headers


def get_model_status(timeout: float = 300) -> Optional[bool]:
    status_override = os.getenv("OSS_LLM_STATUS_URL")
    if status_override:
        status_endpoint = status_override.rstrip("/")
    else:
        base_url = os.getenv("OSS_LLM_BASE_URL", DEFAULT_OSS_BASE_URL)
        status_endpoint = _resolve_status_endpoint(base_url)
    _, headers = _build_headers()
    print(f"DEBUG: Checking status at {status_endpoint}...")
    try:
        response = requests.get(status_endpoint, headers=headers, timeout=timeout)
        print(f"DEBUG: Status check response: {response.status_code}")
        if response.status_code != 200:
            return None
        data = response.json()
        print(f"DEBUG: Status JSON: {data}")
        return bool(data.get("loaded"))
    except requests.RequestException:
        return None


def router_pass(message: str) -> List[str]:
    endpoint, headers = _build_headers()
    print("🔹 Pass 1: Routing to select endpoint...")

    router_context = build_router_context(message)
    router_messages = [
        {"role": "system", "content": router_context},
        {"role": "user", "content": message},
    ]

    router_response = _call_llm(endpoint, headers, router_messages, temperature=0.1)
    print(f"📍 Router response: {router_response[:200]}...")

    selected_endpoints = _parse_router_response(router_response)
    print(f"✅ Selected endpoints: {selected_endpoints}")
    return selected_endpoints


def generator_pass(message: str, selected_endpoints: List[str]) -> Tuple[List[Dict[str, Any]], str]:
    endpoint, headers = _build_headers()
    print("🔹 Pass 2: Generating JSON request...")

    generator_context = build_generator_context(message, selected_endpoints)
    generator_messages = [
        {"role": "system", "content": generator_context},
        {"role": "user", "content": message},
    ]

    generator_response = _call_llm(endpoint, headers, generator_messages, temperature=0.1)
    print(f"📥 Generator response:\n{generator_response}\n")

    parsed = extract_json(generator_response)
    requests_list = parse_requests(parsed)
    return requests_list, generator_response


def generate_requests(message: str, history: List[Dict[str, str]] | None = None) -> LLMResponse:
    """
    Generate ENTSO-E API requests using Two-Pass LLM architecture.

    Pass 1 (Router): Select relevant endpoint(s)
    Pass 2 (Generator): Generate JSON using selected examples
    """
    selected_endpoints = router_pass(message)
    requests_list, generator_response = generator_pass(message, selected_endpoints)

    return LLMResponse(
        requests=requests_list,
        raw_message=generator_response,
        router_endpoints=selected_endpoints,
    )
