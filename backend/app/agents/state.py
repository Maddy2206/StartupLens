from typing import Annotated, Optional, Any
from typing_extensions import TypedDict
import operator


def add(a: list, b: list) -> list:
    return a + b


class ValidationState(TypedDict, total=False):
    # Input
    idea: str
    run_id: str

    # Agent outputs (each agent writes its own key)
    plan: Optional[dict]
    market_research: Optional[dict]
    competitors: Optional[dict]
    community: Optional[dict]
    gap: Optional[dict]
    personas: Optional[dict]
    business_model: Optional[dict]
    mvp: Optional[dict]
    risks: Optional[dict]
    report: Optional[dict]

    # Accumulating lists — safe to merge in parallel
    raw_sources: Annotated[list, add]
    errors: Annotated[list, add]
