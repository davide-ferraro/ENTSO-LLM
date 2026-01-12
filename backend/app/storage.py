"""Storage backends and file registry helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi.responses import FileResponse, RedirectResponse, Response


STORAGE_ROOT = Path(__file__).resolve().parents[1] / "storage"
RESULTS_DIR = STORAGE_ROOT / "results"


@dataclass
class StoredFile:
    storage_key: str
    local_path: Optional[Path]


class StorageBackend:
    """Base interface for storage backends."""

    def store_file(self, local_path: Path) -> StoredFile:
        raise NotImplementedError

    def get_file_response(self, stored_file: StoredFile, filename: str) -> Response:
        raise NotImplementedError


class LocalStorageBackend(StorageBackend):
    """Local filesystem storage (default)."""

    def store_file(self, local_path: Path) -> StoredFile:
        return StoredFile(storage_key=str(local_path), local_path=local_path)

    def get_file_response(self, stored_file: StoredFile, filename: str) -> Response:
        if not stored_file.local_path:
            raise FileNotFoundError("Local path not available")
        return FileResponse(stored_file.local_path, filename=filename)


class S3StorageBackend(StorageBackend):
    """Amazon S3 storage backend using boto3."""

    def __init__(self, bucket: str, prefix: str = "", region: Optional[str] = None) -> None:
        import boto3

        self.bucket = bucket
        self.prefix = prefix.strip("/")
        self.client = boto3.client("s3", region_name=region) if region else boto3.client("s3")

    def store_file(self, local_path: Path) -> StoredFile:
        key_prefix = f"{self.prefix}/" if self.prefix else ""
        storage_key = f"{key_prefix}{uuid4().hex}_{local_path.name}"
        self.client.upload_file(str(local_path), self.bucket, storage_key)
        return StoredFile(storage_key=storage_key, local_path=local_path)

    def get_file_response(self, stored_file: StoredFile, filename: str) -> Response:
        url = self.client.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": stored_file.storage_key, "ResponseContentDisposition": f"attachment; filename={filename}"},
            ExpiresIn=3600,
        )
        return RedirectResponse(url)


def ensure_storage() -> None:
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def get_storage_backend() -> StorageBackend:
    backend = os.getenv("ENTSO_STORAGE_BACKEND", "local").lower()
    if backend == "s3":
        bucket = os.getenv("ENTSO_S3_BUCKET")
        if not bucket:
            raise RuntimeError("ENTSO_S3_BUCKET is required for s3 storage backend.")
        prefix = os.getenv("ENTSO_S3_PREFIX", "")
        region = os.getenv("ENTSO_S3_REGION")
        return S3StorageBackend(bucket=bucket, prefix=prefix, region=region)
    return LocalStorageBackend()


def register_files(
    files: List[Dict[str, str]],
    storage_backend: StorageBackend,
    conversation_id: str,
) -> List[Dict[str, str]]:
    ensure_storage()
    output: List[Dict[str, str]] = []

    for entry in files:
        path = Path(entry["path"]).resolve()
        if not path.exists() or not path.is_file():
            continue

        stored = storage_backend.store_file(path)
        output.append(
            {
                "type": entry.get("type", "file"),
                "name": path.name,
                "storage_key": stored.storage_key,
                "local_path": str(stored.local_path) if stored.local_path else None,
                "conversation_id": conversation_id,
            }
        )

    return output
