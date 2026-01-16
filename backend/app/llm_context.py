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
EXAMPLES_MENU = DOCS_ROOT / "examples" / "examples_menu.md"
EXAMPLES_DIR = DOCS_ROOT / "examples" / "endpoints"
API_DOCS_DIR = DOCS_ROOT / "api" / "endpoints_doc"


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

# Mapping from Endpoint ID to documentation filename
ENDPOINT_TO_DOC = {
    "E01": "total_nominated_capacity.md",
    "E02": "implicit_allocations_offered_transfer_capacity.md",
    "E03": "transfer_capacities_with_third_countries.md",
    "E04": "total_capacity_already_allocated.md",
    "E05": "explicit_allocations_offered_transfer_capacity.md",
    "E06": "explicit_allocations_use_of_transfer_capacity.md",
    "E07": "explicit_allocations_auction_revenue.md",
    "E08": "implicit_auction_net_positions.md",
    "E09": "continuous_allocations_offered_transfer_capacity.md",
    "E10": "energy_prices.md",
    "E11": "actual_total_load_6_1_a_get_method.md",
    "E12": "day_ahead_total_load_forecast.md",
    "E13": "week_ahead_total_load_forecast.md",
    "E14": "installed_capacity_per_production_type.md",
    "E15": "year_ahead_total_load_forecast.md",
    "E16": "actual_generation_per_generation_unit.md",
    "E17": "actual_generation_per_production_type.md",
    "E18": "generation_forecast_day_ahead.md",
    "E19": "generation_forecasts_for_wind_and_solar.md",
    "E20": "cross_border_physical_flows.md",
    "E21": "forecasted_transfer_capacities.md",
    "E22": "commercial_schedules.md",
    "E23": "cross_border_capacity_of_dc_links_intraday_transfer_limits.md",
    "E24": "unavailability_of_generation_units.md",
    "E25": "unavailability_of_transmission_infrastructure.md",
    "E26": "imbalance_prices.md",
    "E27": "total_imbalance_volumes.md",
    "E28": "current_balancing_state_area_control_error.md",
    "E29": "fcr_total_capacity.md",
    "E30": "prices_of_activated_balancing_energy.md",
    "E37": "unavailability_of_production_units.md",
    "E41": "cross_border_marginal_prices.md",
    "E43": "aggregated_balancing_energy_bids.md",
    "E44": "volumes_and_prices_of_contracted_reserves.md",
    "E45": "procured_balancing_capacity.md",
    "E46": "energy_prices.md",
    "E47": "energy_prices.md",
    "E48": "imbalance_prices.md",
    "E49": "cross_border_physical_flows.md",
    "E50": "congestion_income.md",
    "E51": "actual_total_load_6_1_a_get_method.md",
    "E52": "actual_generation_per_production_type.md",
    "E53": "generation_forecasts_for_wind_and_solar.md",
    "E54": "forecasted_transfer_capacities.md",
    "E55": "total_imbalance_volumes.md",
    "E56": "energy_prices.md",
    "E57": "energy_prices.md",
    "E58": "energy_prices.md",
    "E59": "cross_border_physical_flows.md",
    "E60": "cross_border_physical_flows.md",
    "E61": "installed_capacity_per_production_type.md",
    "E62": "unavailability_of_generation_units.md",
    "E63": "unavailability_of_transmission_infrastructure.md",
    "E64": "current_balancing_state_area_control_error.md",
    "E65": "prices_of_activated_balancing_energy.md",
}


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
    for line in menu.splitlines():
        line = line.strip()
        if not line.startswith("## "):
            continue
        # Format: ## E11 — Actual Total Load (6.1.A)
        match = re.match(r"^##\s+(E\d+)\s+(?:—|-)\s+(.+)$", line)
        if match:
            code, title = match.groups()
            titles[code] = title.strip()
    return titles


def build_router_context(user_query: str) -> str:
    """
    Build context for Pass 1: Router.
    
    The LLM will see:
    1. Router prompt (instructions)
    2. Examples menu (all endpoints)
    3. User query
    
    The LLM should return: {"endpoints": ["E10"]}
    """
    router_prompt = _load_router_prompt()
    examples_menu = _load_examples_menu()
    
    parts = [
        router_prompt,
        "## Endpoint Menu\n" + examples_menu,
        f"## User Request\n{user_query}",
        "## Your Response (JSON only):"
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


def _load_endpoint_examples(endpoint_ids: List[str]) -> str:
    """Load the full example files for selected endpoints."""
    content_parts = []
    
    for eid in endpoint_ids:
        example_file = EXAMPLES_DIR / f"{eid}.md"
        if example_file.exists():
            content_parts.append(f"## Examples for {eid}\n" + example_file.read_text(encoding="utf-8"))
    
    if content_parts:
        return "\n\n".join(content_parts)
    return ""


def _load_endpoint_documentation(endpoint_ids: List[str]) -> str:
    """Load matching API documentation files for selected endpoints."""
    content_parts = []
    seen_docs = set()
    
    for eid in endpoint_ids:
        doc_filename = ENDPOINT_TO_DOC.get(eid)
        if doc_filename and doc_filename not in seen_docs:
            doc_file = API_DOCS_DIR / doc_filename
            if doc_file.exists():
                content_parts.append(f"### TECHNICAL DOC: {doc_filename}\n" + doc_file.read_text(encoding="utf-8"))
                seen_docs.add(doc_filename)
                
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
    4. Selected endpoint examples
    5. Selected technical documentation
    6. User query
    """
    generator_prompt = _load_generator_prompt()
    examples = _load_endpoint_examples(endpoint_ids)
    technical_docs = _load_endpoint_documentation(endpoint_ids)
    
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
