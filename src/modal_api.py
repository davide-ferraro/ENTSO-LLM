"""
ENTSO-E Modal API Service

This module exposes an on-demand HTTP endpoint hosted on Modal.
It accepts request payloads and executes ENTSO-E API calls when invoked.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, List

import modal

from entsoe_core import build_config, parse_results, run_request, setup_directories

# =============================================================================
# MODAL APP CONFIGURATION
# =============================================================================

app = modal.App("entsoe-api")

volume = modal.Volume.from_name("entsoe-fetch", create_if_missing=True)
VOLUME_PATH = Path("/data")

image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "requests",
    "python-dotenv",
)

# =============================================================================
# PAYLOAD HANDLING
# =============================================================================


def _normalize_payload(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
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
        raise ValueError("Payload must include 'params', 'request', or 'requests'.")

    if not isinstance(requests_list, list) or not requests_list:
        raise ValueError("Payload 'requests' must be a non-empty list.")

    normalized: List[Dict[str, Any]] = []
    for item in requests_list:
        if not isinstance(item, dict):
            raise ValueError("Each request entry must be a JSON object.")
        params = item.get("params")
        if not isinstance(params, dict):
            raise ValueError("Each request entry must include a 'params' object.")
        normalized.append({"name": item.get("name", "request"), "params": params})

    return normalized


# =============================================================================
# MODAL HTTP ENDPOINT
# =============================================================================


@app.function(
    image=image,
    volumes={VOLUME_PATH: volume},
    secrets=[modal.Secret.from_name("ENTSOE_API_KEY")],
    timeout=3600,
)
@modal.web_endpoint(method="POST")
def run_entsoe_requests(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Run ENTSO-E requests on-demand via HTTP."""
    try:
        requests_list = _normalize_payload(payload)
    except ValueError as exc:
        return {"error": str(exc)}

    api_key = os.environ.get("ENTSOE_API_KEY")
    if not api_key:
        return {"error": "ENTSOE_API_KEY is not set in the Modal environment."}

    config = build_config(
        api_key,
        project_root=Path("/"),
        output_dir=VOLUME_PATH,
    )
    setup_directories(config)

    results = [run_request(req["params"], req.get("name"), config) for req in requests_list]
    summary_payload = parse_results(results)

    volume.commit()

    return {
        "results": results,
        "output_root": str(VOLUME_PATH),
        **summary_payload,
    }
