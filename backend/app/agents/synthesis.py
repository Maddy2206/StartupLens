from app.agents.state import ValidationState
from app.agents.base import run_agent
from app.schemas.report import ValidationReport
from app.llm.prompts import SYNTHESIS_SYSTEM, SYNTHESIS_USER


def _safe(d: dict | None, key: str, fallback: str = "Not available.") -> str:
    return (d or {}).get(key, fallback) or fallback


async def synthesis_node(state: ValidationState) -> dict:
    idea = state["idea"]
    run_id = state["run_id"]

    market = state.get("market_research") or {}
    competitors = state.get("competitors") or {}
    community = state.get("community") or {}
    gap = state.get("gap") or {}
    personas = state.get("personas") or {}
    bm = state.get("business_model") or {}
    mvp = state.get("mvp") or {}
    risks = state.get("risks") or {}

    # Build concise summaries for each section
    personas_list = personas.get("personas", [])
    personas_summary = "\n".join(
        f"- {p.get('name')} ({p.get('role')}): {', '.join(p.get('pain_points', [])[:2])}"
        for p in personas_list[:3]
    ) or "No persona data."

    bm_tiers = bm.get("pricing_tiers", [])
    bm_summary = (
        f"Model: {bm.get('recommended_model', '?')}. "
        f"Tiers: {', '.join(t.get('name', '') + ' ' + t.get('price', '') for t in bm_tiers[:3])}. "
        f"{bm.get('summary', '')}"
    )

    mvp_features = [f.get("feature", "") for f in mvp.get("features", []) if f.get("priority") == "must-have"]
    mvp_summary = f"{mvp.get('mvp_description', '')} Must-haves: {', '.join(mvp_features[:5])}."

    risk_list = risks.get("risks", [])
    high_risks = [r.get("risk", "") for r in risk_list if r.get("severity") == "high"]
    risks_summary = f"High risks: {', '.join(high_risks[:3])}. Overall: {risks.get('overall_risk_level', '?')}."

    result = await run_agent(
        run_id=run_id,
        agent_name="synthesis",
        system=SYNTHESIS_SYSTEM,
        user=SYNTHESIS_USER.format(
            idea=idea,
            market_summary=_safe(market, "summary"),
            competitor_summary=_safe(competitors, "summary"),
            community_summary=_safe(community, "summary"),
            uvp=_safe(gap, "unique_value_proposition"),
            how_to_win="\n".join(gap.get("how_to_win", [])[:4]),
            personas_summary=personas_summary,
            business_model_summary=bm_summary,
            mvp_summary=mvp_summary,
            risks_summary=risks_summary,
        ),
        schema=ValidationReport,
    )

    if result:
        # Inject all sub-sections so the report is complete
        report_dict = result.model_dump()
        report_dict["market_research"] = market if market else report_dict.get("market_research")
        report_dict["competitors"] = competitors if competitors else report_dict.get("competitors")
        report_dict["community"] = community if community else report_dict.get("community")
        report_dict["gap"] = gap if gap else report_dict.get("gap")
        report_dict["personas"] = personas if personas else report_dict.get("personas")
        report_dict["business_model"] = bm if bm else report_dict.get("business_model")
        report_dict["mvp"] = mvp if mvp else report_dict.get("mvp")
        report_dict["risks"] = risks if risks else report_dict.get("risks")
        return {"report": report_dict, "raw_sources": [], "errors": []}

    return {"report": None, "errors": ["synthesis failed"]}
