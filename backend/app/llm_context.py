"""Context builder for Two-Pass LLM request generation.

Pass 1 (Router): LLM selects the relevant endpoint(s) from the menu.
Pass 2 (Generator): LLM generates JSON using the selected endpoint's examples.
"""

from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Dict, List
import re


DOCS_ROOT = Path(__file__).resolve().parents[2] / "docs"

# Prompt files
ROUTER_PROMPT = DOCS_ROOT / "prompts" / "router_prompt.md"
GENERATOR_PROMPT = DOCS_ROOT / "prompts" / "generator_prompt.md"
# Router now uses the lighter menu to reduce prompt size.
EXAMPLES_MENU = DOCS_ROOT / "examples" / "examples_menu_1.md"
EXAMPLES_DIR = DOCS_ROOT / "examples" / "endpoints"
TRANSPARENCY_DOC = DOCS_ROOT / "api" / "ENTSOE_Transparency_API_Documentation.md"
REQUEST_EXAMPLES = DOCS_ROOT / "examples" / "request_examples.md"


# ============================================================================
# COMMON EIC CODES (hardcoded for quick reference)
# ============================================================================

COMMON_EIC_CODES = """
## EIC Codes Reference

| Country | EIC Code |
|---------|----------|
| Austria | 10YAT-APG------L |
| Belgium | 10YBE----------2 |
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
| Netherlands | 10YNL----------L |
| Norway (NO1) | 10YNO-1--------2 |
| Poland | 10YPL-AREA-----S |
| Portugal | 10YPT-REN------W |
| Romania | 10YRO-TEL------P |
| Spain | 10YES-REE------0 |
| Sweden (SE3) | 10Y1001A1001A46L |
| Switzerland | 10YCH-SWISSGRIDZ |
"""

# ============================================================================
# PASS 1: ROUTER
# ============================================================================

@lru_cache(maxsize=1)
def _load_router_prompt() -> str:
    """Load the router prompt template."""
    if ROUTER_PROMPT.exists():
        return ROUTER_PROMPT.read_text(encoding="utf-8")
    return "Select the endpoint for this request. Return JSON: {\"endpoints\": [\"E10\"]}"


@lru_cache(maxsize=1)
def _load_examples_menu() -> str:
    """Load the examples menu."""
    if EXAMPLES_MENU.exists():
        return EXAMPLES_MENU.read_text(encoding="utf-8")
    return ""


@lru_cache(maxsize=1)
def load_endpoint_titles() -> Dict[str, str]:
    """Load endpoint titles from the examples menu."""
    menu = _load_examples_menu()
    titles: Dict[str, str] = {}
    article_map: Dict[str, str] = {}
    for line in menu.splitlines():
        line = line.strip()
        if not line.startswith("## "):
            continue
        # Supported formats:
        # - ## E11 — Actual Total Load (6.1.A)
        # - ## 6.1.A — Actual Total Load
        # - ## Endpoint 11: Actual Total Load (6.1.A)
        code = None
        article = None
        title = None

        # Try E-codes at start
        match_e = re.match(r"^##\s+(E\d+)\s+(?:—|-)\s+(.+)$", line)
        if match_e:
            code, title = match_e.groups()
        else:
            # Try article code at start
            match_article = re.match(r"^##\s+(\d+\.\d+(?:\.[A-Z0-9]+)?)\s+(?:—|-)\s+(.+)$", line)
            if match_article:
                code, title = match_article.groups()
                article = code
        # If still not found, search for article code in parentheses
        if not code:
            paren_match = re.search(r"\((\d+\.\d+(?:\.[A-Z0-9]+)?)\)", line)
            if paren_match:
                article = paren_match.group(1)
                code = article
                title = re.sub(r"\s*\(.*?\)", "", line.replace("##", "")).strip()

        if code and title:
            titles[code] = title.strip()
        if code and article:
            article_map[code] = article
            article_map[article] = article
    return titles


@lru_cache(maxsize=1)
def load_endpoint_article_map() -> Dict[str, str]:
    """Map E-codes to article codes (and identity for article codes)."""
    menu = _load_examples_menu()
    mapping: Dict[str, str] = {}
    for line in menu.splitlines():
        line = line.strip()
        if not line.startswith("## "):
            continue
        # Capture E-code and article code in parentheses
        e_match = re.match(r"^##\s+(E\d+)", line)
        paren_match = re.search(r"\((\d+\.\d+(?:\.[A-Z0-9]+)?)\)", line)
        if e_match and paren_match:
            e_code = e_match.group(1)
            article = paren_match.group(1)
            mapping[e_code] = article
            mapping[article] = article
        else:
            # If only article is present, map to itself
            match_article = re.match(r"^##\s+(\d+\.\d+(?:\.[A-Z0-9]+)?)", line)
            if match_article:
                article = match_article.group(1)
                mapping[article] = article
    return mapping


def build_router_context(user_query: str, filtered_menu: str | None = None) -> str:
    """
    Build context for Pass 1: Router.
    
    The LLM will see:
    1. Router prompt (instructions)
    2. Examples menu (all endpoints)
    
    The LLM should return: {"endpoints": ["E10"]}
    """
    router_prompt = _load_router_prompt()
    examples_menu = filtered_menu if filtered_menu is not None else _load_examples_menu()
    
    parts = [
        router_prompt,
        "## Endpoint Menu\n" + examples_menu,
        "## Output\nReturn only JSON: { \"endpoint\": \"<ARTICLE_CODE>\" }"
    ]
    
    return "\n\n".join(parts)


# ============================================================================
# PASS 2: GENERATOR
# ============================================================================

@lru_cache(maxsize=1)
def _load_generator_prompt() -> str:
    """Load the generator prompt template."""
    if GENERATOR_PROMPT.exists():
        return GENERATOR_PROMPT.read_text(encoding="utf-8")
    return "Generate the ENTSO-E API request as JSON."


@lru_cache(maxsize=1)
def _load_transparency_doc() -> str:
    if TRANSPARENCY_DOC.exists():
        return TRANSPARENCY_DOC.read_text(encoding="utf-8")
    return ""


@lru_cache(maxsize=1)
def _load_request_examples() -> str:
    if REQUEST_EXAMPLES.exists():
        return REQUEST_EXAMPLES.read_text(encoding="utf-8")
    return ""


def _extract_sections_by_article(doc_text: str, article_codes: List[str], heading_prefix: str) -> str:
    """Extract sections with headings containing any of the article codes."""
    if not doc_text or not article_codes:
        return ""

    lines = doc_text.splitlines()
    matches = []
    for idx, line in enumerate(lines):
        if line.startswith(heading_prefix):
            for code in article_codes:
                # match "(<code>...)" to allow combined headings like (16.1.B&C)
                import re
                pattern = r"\(" + re.escape(code) + r"[^)]*\)"
                if re.search(pattern, line):
                    matches.append(idx)
                    break

    if not matches:
        return ""

    sections: List[str] = []
    for start_idx in matches:
        end_idx = len(lines)
        for j in range(start_idx + 1, len(lines)):
            if lines[j].startswith(heading_prefix):
                end_idx = j
                break
        sections.append("\n".join(lines[start_idx:end_idx]).strip())

    return "\n\n".join(sections)


def _load_doc_sections_for_articles(article_codes: List[str]) -> str:
    doc_text = _load_transparency_doc()
    return _extract_sections_by_article(doc_text, article_codes, "#### ")


def _load_example_sections_for_articles(article_codes: List[str]) -> str:
    examples_text = _load_request_examples()
    return _extract_sections_by_article(examples_text, article_codes, "## ")


def _load_endpoint_examples(endpoint_ids: List[str]) -> str:
    """Load the full example files for selected endpoints (legacy E-based; optional)."""
    content_parts = []
    for eid in endpoint_ids:
        example_file = EXAMPLES_DIR / f"{eid}.md"
        if example_file.exists():
            content_parts.append(f"## Examples for {eid}\n" + example_file.read_text(encoding="utf-8"))
    if content_parts:
        return "\n\n".join(content_parts)
    return ""


def build_generator_context(user_query: str, endpoint_ids: List[str]) -> str:
    """
    Build context for Pass 2: Generator.
    
    The LLM will see:
    1. Generator prompt (instructions + output format)
    2. Current UTC time
    3. EIC codes reference
    4. Selected technical documentation (article-based)
    5. Selected request examples (article-based)
    6. Selected endpoint examples (legacy E-based, if present)
    7. User query
    """
    generator_prompt = _load_generator_prompt()
    # Treat endpoint_ids as article codes for extraction, but keep E-based examples if available.
    article_codes = endpoint_ids
    examples = _load_endpoint_examples(endpoint_ids)
    technical_docs = _load_doc_sections_for_articles(article_codes)
    request_examples = _load_example_sections_for_articles(article_codes)
    
    # Current time
    now = datetime.now(timezone.utc)
    current_time = now.strftime('%Y%m%d%H%M')
    
    parts = [
        generator_prompt,
        f"## Current UTC Time\n{current_time}",
        COMMON_EIC_CODES.strip(),
    ]
    
    if technical_docs:
        parts.append(technical_docs)

    if request_examples:
        parts.append(request_examples)
        
    if examples:
        parts.append(examples)
    
    parts.extend([
        f"## User Request\n{user_query}",
        "## Generate the JSON:"
    ])
    
    return "\n\n".join(parts)


# ============================================================================
# LEGACY COMPATIBILITY (single-pass, deprecated)
# ============================================================================

def build_context(message: str, history=None) -> str:
    """
    Legacy single-pass context builder.
    DEPRECATED: Use build_router_context + build_generator_context instead.
    """
    # Fallback to generator context with a default endpoint
    return build_generator_context(message, ["E10", "E11", "E17"])
