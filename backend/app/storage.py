"""File registry for generated ENTSO-E outputs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List
from uuid import uuid4


STORAGE_ROOT = Path(__file__).resolve().parents[1] / "storage"
RESULTS_DIR = STORAGE_ROOT / "results"
INDEX_PATH = STORAGE_ROOT / "index.json"


def ensure_storage() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
    if not INDEX_PATH.exists():
        INDEX_PATH.write_text(json.dumps({"files": {}}, indent=2), encoding="utf-8")


def load_index() -> Dict[str, Dict[str, str]]:
    ensure_storage()
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def save_index(index: Dict[str, Dict[str, str]]) -> None:
    INDEX_PATH.write_text(json.dumps(index, indent=2), encoding="utf-8")


def register_files(files: List[Dict[str, str]]) -> List[Dict[str, str]]:
    ensure_storage()
    index = load_index()
    registry = index.setdefault("files", {})
    output: List[Dict[str, str]] = []

    for entry in files:
        path = Path(entry["path"]).resolve()
        if not path.exists():
            continue
        try:
            if not path.is_relative_to(RESULTS_DIR):
                continue
        except AttributeError:
            if str(RESULTS_DIR) not in str(path):
                continue

        file_id = uuid4().hex
        registry[file_id] = {
            "path": str(path),
            "type": entry.get("type", "file"),
            "name": path.name,
        }
        output.append(
            {
                "id": file_id,
                "type": entry.get("type", "file"),
                "name": path.name,
                "url": f"/files/{file_id}",
                "path": str(path),
            }
        )

    save_index(index)
    return output


def resolve_file(file_id: str) -> Dict[str, str] | None:
    index = load_index()
    return index.get("files", {}).get(file_id)
