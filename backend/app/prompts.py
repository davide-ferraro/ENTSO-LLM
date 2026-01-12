"""Prompt loading helpers for the ENTSO-LLM backend."""

from __future__ import annotations

from pathlib import Path

PROMPT_FILES = (
    Path(__file__).resolve().parents[2]
    / "docs"
    / "prompts"
    / "context_prompt.md",
    Path(__file__).resolve().parents[2]
    / "docs"
    / "prompts"
    / "prompt_instructions.md",
)


def load_system_prompt() -> str:
    """Load the LLM system prompt from docs/prompts."""
    parts = []
    for path in PROMPT_FILES:
        parts.append(path.read_text(encoding="utf-8"))
    return "\n\n".join(parts)
