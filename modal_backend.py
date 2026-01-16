"""
Modal deployment for the ENTSO-LLM backend using Gemini.

Usage:
  modal deploy modal_backend.py
"""

from __future__ import annotations

import os
from pathlib import Path

import modal

app = modal.App("entso-llm-backend")

volume = modal.Volume.from_name("entso-llm-data", create_if_missing=True)

root_dir = Path(__file__).parent.resolve()
mount = modal.Mount.from_local_dir(
    str(root_dir),
    remote_path="/root/entso-llm",
    condition=lambda p: not any(part in {"node_modules", ".next", ".git", "__pycache__"} for part in Path(p).parts),
)

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install_from_requirements("backend/requirements.txt")
    .env({"ENTSO_STORAGE_ROOT": "/data"})
)


@app.function(image=image, mounts=[mount], volumes={"/data": volume}, timeout=900)
@modal.asgi_app()
def fastapi_app():
    import sys

    sys.path.append("/root/entso-llm")
    from backend.app.main import app as fastapi

    os.environ.setdefault("ENTSO_STORAGE_ROOT", "/data")
    return fastapi
