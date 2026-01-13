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
    """Load the full content of the prompt file."""
    return [path.read_text(encoding="utf-8")]


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


COMMON_EIC_CODES = """
### REFERENCE: COMMON EIC CODES
| Country | Code |
|---|---|
| Austria | 10YAT-APG------L |
| Belgium | 10YBE----------2 |
| Bosnia & Herz. | 10YBA-JPCC-----D |
| Bulgaria | 10YCA-BULGARIA-R |
| Croatia | 10YHR-HEP------M |
| Czech Republic | 10YCZ-CEPS-----N |
| Denmark (DK1) | 10YDK-1--------W |
| Denmark (DK2) | 10YDK-2--------M |
| Finland | 10YFI-1--------U |
| France | 10YFR-RTE------C |
| Germany-Luxembourg | 10Y1001A1001A82H |
| Great Britain | 10YGB----------A |
| Greece | 10YGR-HTSO-----Y |
| Hungary | 10YHU-MAVIR----U |
| Ireland | 10Y1001A1001A59C |
| Italy (North) | 10Y1001A1001A73I |
| Italy (South) | 10Y1001A1001A788 |
| Montenegro | 10YCS-CG-TSO---S |
| Netherlands | 10YNL----------L |
| North Macedonia | 10YMK-MEPSO----8 |
| Norway (NO1) | 10YNO-1--------2 |
| Poland | 10YPL-AREA-----S |
| Portugal | 10YPT-REN------W |
| Romania | 10YRO-TEL------P |
| Serbia | 10YCS-SERBIATSOV |
| Slovakia | 10YSK-SEPS-----K |
| Slovenia | 10YSI-ELES-----O |
| Spain | 10YES-REE------0 |
| Sweden (SE3) | 10Y1001A1001A46L |
| Switzerland | 10YCH-SWISSGRIDZ |
"""

def _load_menu_items() -> List[Tuple[str, str]]:
    """
    Parses examples_menu.md into a list of (endpoint_id, full_text_block).
    Returns list of ("E01", "## E01 - Title\n- Description..."), etc.
    """
    menu_path = DOCS_ROOT / "examples" / "examples_menu.md"
    if not menu_path.exists():
        return []
    
    text = menu_path.read_text(encoding="utf-8")
    items = []
    # Split by level 2 headers
    parts = re.split(r'(?=## E\d+)', text)
    
    for part in parts:
        part = part.strip()
        if not part.startswith("## E"):
            continue
        # Extract ID (E01, E12, etc.)
        match = re.search(r"## (E\d+)", part)
        if match:
            eid = match.group(1)
            items.append((eid, part))
    return items


def _get_relevant_examples(query_terms: set[str], limit: int = 3) -> str:
    """Finds top N relevant examples and loads their full content."""
    menu_items = _load_menu_items()
    if not menu_items:
        return ""

    scored = []
    for eid, text in menu_items:
        score = _score_snippet(query_terms, text)
        scored.append((score, eid, text))
    
    # Sort by score descending
    scored.sort(key=lambda x: x[0], reverse=True)
    
    # Keep top items if they have any relevance (>0 score)
    top_items = [item for item in scored if item[0] > 0][:limit]
    
    if not top_items:
        return ""

    selected_content = []
    selected_content.append("### RELEVANT EXAMPLES (Based on your query):")
    
    for score, eid, menu_text in top_items:
        # Load the actual full example file
        ex_file = DOCS_ROOT / "examples" / "endpoints" / f"{eid}.md"
        if ex_file.exists():
            full_content = ex_file.read_text(encoding="utf-8")
            selected_content.append(f"\n--- Example {eid} ---\n{full_content}")
        else:
            selected_content.append(f"\n--- Summary {eid} ---\n{menu_text}")

    return "\n\n".join(selected_content)

def build_context(message: str, history: Sequence[dict[str, str]] | None = None) -> str:
    from datetime import datetime, timezone
    
    # 1. Base Context
    context_prompts = _base_prompt_sections()
    
    # 2. Dynamic Example Retrieval
    history_text = "\n".join(msg.get("content", "") for msg in history or [])
    query = f"{message}\n{history_text}".strip()
    terms = set(_tokenize(query))
    
    # Limit to top 2 examples to save tokens
    relevant_examples = _get_relevant_examples(terms, limit=2)

    # Current Time Info
    now = datetime.now(timezone.utc)
    time_info = f"Current Date and Time (UTC): {now.strftime('%Y-%m-%d %H:%M')}"

    parts = [
        "You are an ENTSO-E request generator. Return only valid JSON.",
        time_info,
        "\n\n".join(context_prompts),
        COMMON_EIC_CODES,
        relevant_examples,
        "### USER REQUEST",
        "Output schema: {\"requests\": [{\"name\": \"...\", \"params\": { ... }}]}",
    ]
    
    return "\n\n".join(part for part in parts if part)
