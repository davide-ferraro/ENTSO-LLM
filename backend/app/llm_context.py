"""Context builder for LLM request generation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, List, Sequence


DOCS_ROOT = Path(__file__).resolve().parents[2] / "docs"
PROMPT_FILES = (
    DOCS_ROOT / "prompts" / "context_prompt.md",
    DOCS_ROOT / "prompts" / "prompt_instructions.md",
)
DOCS_SEARCH_DIRS = (
    DOCS_ROOT / "api",
    DOCS_ROOT / "examples",
)

PROMPT_SECTION_TITLES = {
    "Your Role",
    "Request Format",
    "Important Constraints",
    "Time Format",
    "Most Common Document Types",
    "Most Common Process Types",
    "Most Common PSR Types",
    "Frequently Used EIC Codes",
    "Historical Data Requests",
}


@dataclass(frozen=True)
class DocSnippet:
    source: str
    content: str
    score: int


def _tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _score_snippet(terms: set[str], snippet: str) -> int:
    if not terms:
        return 0
    snippet_terms = set(_tokenize(snippet))
    return sum(1 for term in terms if term in snippet_terms)


def _split_blocks(text: str) -> Iterable[str]:
    for block in re.split(r"\n{2,}", text):
        cleaned = block.strip()
        if cleaned:
            yield cleaned


def _normalize_title(title: str) -> str:
    return " ".join(re.findall(r"[A-Za-z0-9]+", title))


def _load_prompt_sections(path: Path) -> List[str]:
    text = path.read_text(encoding="utf-8")
    sections: List[str] = []
    current_lines: List[str] = []
    current_title: str | None = None
    normalized_targets = {_normalize_title(title) for title in PROMPT_SECTION_TITLES}

    for line in text.splitlines():
        if line.startswith("## "):
            if current_title in normalized_targets and current_lines:
                sections.append("\n".join(current_lines).strip())
            current_title = _normalize_title(line.replace("## ", "", 1).strip())
            current_lines = [line]
        else:
            if current_lines is not None:
                current_lines.append(line)

    if current_title in normalized_targets and current_lines:
        sections.append("\n".join(current_lines).strip())

    return sections


@lru_cache(maxsize=1)
def _base_prompt_sections() -> List[str]:
    sections: List[str] = []
    for path in PROMPT_FILES:
        if path.exists():
            sections.extend(_load_prompt_sections(path))
    return sections


def _collect_doc_snippets(terms: set[str], limit: int) -> List[DocSnippet]:
    snippets: List[DocSnippet] = []
    for directory in DOCS_SEARCH_DIRS:
        for path in directory.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            for block in _split_blocks(text):
                score = _score_snippet(terms, block)
                if score > 0:
                    snippets.append(
                        DocSnippet(
                            source=f"{path.relative_to(DOCS_ROOT)}",
                            content=block,
                            score=score,
                        )
                    )
    snippets.sort(key=lambda item: item.score, reverse=True)
    return snippets[:limit]


def _format_snippets(snippets: Sequence[DocSnippet]) -> str:
    if not snippets:
        return ""
    lines = ["Relevant documentation snippets:"]
    for snippet in snippets:
        lines.append(f"- Source: {snippet.source}")
        lines.append(snippet.content)
    return "\n".join(lines)


def _format_index() -> str:
    entries = [
        "docs/api/ENTSOE_Transparency_API_Documentation.md (API parameters & endpoints)",
        "docs/api/ENTSOE_EIC_Area_Codes.md (EIC area/bidding zone codes)",
        "docs/examples/request_examples.md (working request examples)",
        "docs/examples/natural_language_examples.md (NL prompt examples)",
    ]
    return "Documentation index:\n" + "\n".join(f"- {entry}" for entry in entries)


def build_context(message: str, history: Sequence[dict[str, str]] | None = None) -> str:
    history_text = "\n".join(msg.get("content", "") for msg in history or [])
    query = f"{message}\n{history_text}".strip()
    terms = set(_tokenize(query))

    base_sections = _base_prompt_sections()
    snippets = _collect_doc_snippets(terms, limit=8)
    parts = [
        "You are an ENTSO-E request generator. Return only valid JSON.",
        _format_index(),
        "\n\n".join(base_sections),
        _format_snippets(snippets),
        "Output schema: {\"requests\": [{\"name\": \"...\", \"params\": { ... }}]}",
    ]
    return "\n\n".join(part for part in parts if part)
