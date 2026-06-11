"""
End-to-end graph test with mocked LLM and no external API calls.
Proves the full orchestration works with zero external keys.
"""
import asyncio
import json
import pytest
from unittest.mock import AsyncMock, patch
from app.agents.state import ValidationState
from app.services.events import register_run, get_queue


_MARKET = {
    "market_size": {"tam": "$10B (estimated)", "sam": "$2B", "som": "$200M", "growth_rate": "15% CAGR"},
    "key_trends": ["AI adoption", "mobile-first"],
    "market_drivers": ["increasing data volume"],
    "market_barriers": ["regulation"],
    "supporting_stats": ["85% of SMBs lack unified financial tools"],
    "summary": "Large and growing market with fragmented solutions.",
}
_COMPETITORS = {
    "direct_competitors": [{"name": "FinanceApp X", "description": "UPI tracker", "pricing": "$5/mo",
                            "key_features": ["expense tracking"], "target_segment": "freelancers",
                            "weakness": "No multi-bank aggregation"}],
    "indirect_competitors": [],
    "market_leaders": ["FinanceApp X"],
    "summary": "Fragmented market, no multi-bank leader.",
}
_COMMUNITY = {
    "pain_points": [{"pain_point": "No multi-bank support", "frequency": "high", "source": "Reddit"}],
    "feature_requests": ["bank aggregation"],
    "emotional_language": ["frustrated", "annoyed"],
    "underserved_segments": ["gig workers"],
    "summary": "Users frustrated by single-bank apps.",
}
_GAP = {
    "incumbent_shortcomings": ["single bank only", "manual entry"],
    "market_gaps": ["unified multi-bank UPI view"],
    "underserved_segments": ["gig economy workers"],
    "how_to_win": ["auto-categorization", "multi-bank sync"],
    "unique_value_proposition": "The only app that unifies all UPI transactions across banks.",
    "differentiation_angle": "Zero-manual-entry, AI-first multi-bank aggregation",
}
_PERSONAS = {
    "personas": [{"name": "Ravi", "role": "Freelancer", "age_range": "25-35",
                  "pain_points": ["multiple apps"], "goals": ["one view"],
                  "willingness_to_pay": "$8/mo", "preferred_channels": ["ProductHunt"],
                  "quote": "I have 3 bank accounts and no idea where my money went."}],
    "primary_persona": "Ravi",
    "target_segment_summary": "Gig workers with multiple bank accounts.",
}
_BIZ = {
    "recommended_model": "SaaS freemium",
    "pricing_tiers": [{"name": "Free", "price": "$0", "features": ["1 bank"], "target_user": "casual"}],
    "monetization_strategies": ["premium tier"],
    "revenue_scenarios": [{"label": "base", "year_1_arr": "$500K", "year_3_arr": "$5M",
                           "assumptions": ["5000 paid users"]}],
    "unit_economics_notes": "LTV/CAC > 3x by month 18.",
    "summary": "Freemium SaaS with upsell to pro.",
}
_MVP = {
    "mvp_description": "A mobile app connecting 3+ banks showing unified UPI history with AI tags.",
    "features": [{"feature": "Multi-bank sync", "priority": "must-have", "effort": "high", "rationale": "core value"}],
    "tech_stack_recommendation": "React Native + FastAPI + Setu API",
    "architecture_notes": "Event-driven ingestion pipeline.",
    "roadmap": [{"phase": "Phase 1", "duration": "8 weeks", "goals": ["MVP launch"], "deliverables": ["app"]}],
    "launch_checklist": ["beta users", "app store listing"],
}
_RISKS = {
    "risks": [{"category": "market", "risk": "Low adoption", "severity": "medium", "mitigation": "focus on niche"}],
    "devils_advocate": ["What if banks block API access?"],
    "critical_assumptions": ["Bank APIs are accessible"],
    "failure_modes": ["API access revoked"],
    "overall_risk_level": "medium — manageable with right partnerships",
}


def _mock_structured_output(schema):
    """Return a minimal valid instance for any schema."""
    from app.schemas.report import (
        PlanOutput, MarketResearchOutput, CompetitorOutput, CommunityOutput,
        GapOutput, PersonaOutput, BusinessModelOutput, MvpOutput, RiskOutput, ValidationReport,
    )
    mapping = {
        PlanOutput: {"subtasks": ["research market"], "key_questions": ["Big market?"], "focus_areas": ["market"]},
        MarketResearchOutput: _MARKET,
        CompetitorOutput: _COMPETITORS,
        CommunityOutput: _COMMUNITY,
        GapOutput: _GAP,
        PersonaOutput: _PERSONAS,
        BusinessModelOutput: _BIZ,
        MvpOutput: _MVP,
        RiskOutput: _RISKS,
        ValidationReport: {
            "idea": "AI unified UPI tracker",
            "executive_summary": "Strong opportunity in fintech.",
            "problem_statement": "No unified UPI view.",
            "market_research": _MARKET,
            "competitors": _COMPETITORS,
            "community": _COMMUNITY,
            "gap": _GAP,
            "personas": _PERSONAS,
            "business_model": _BIZ,
            "mvp": _MVP,
            "risks": _RISKS,
            "go_to_market": ["Launch on ProductHunt"],
            "next_steps": ["Talk to 10 users"],
            "validation_score": 72,
            "validation_score_rationale": "Strong need, clear gap.",
            "differentiation_score": 68,
            "differentiation_score_rationale": "Unique multi-bank angle.",
            "score_breakdown": [{"label": "Market Opportunity", "score": 20, "rationale": "Large TAM"}],
        },
    }
    data = mapping.get(schema)
    if data is None:
        raise ValueError(f"No mock data for schema {schema}")
    return schema(**data)


@pytest.mark.asyncio
async def test_full_graph_mocked():
    """Full pipeline runs to completion with mocked LLM and no network calls."""
    run_id = "test-run-001"

    async def mock_structured(self, system, user, schema, temperature=0.4):
        return _mock_structured_output(schema)

    with (
        patch("app.llm.client.LLMClient.structured", new=mock_structured),
        patch("app.tools.tavily.tavily_search", new=AsyncMock(return_value=type("R", (), {"success": False, "data": None, "error": "no key"})())),
        patch("app.tools.reddit.reddit_search", new=AsyncMock(return_value=type("R", (), {"success": False, "data": None, "error": "no key"})())),
        patch("app.tools.reddit.hn_search", new=AsyncMock(return_value=type("R", (), {"success": False, "data": None, "error": "no key"})())),
    ):
        from app.graph.workflow import build_graph
        graph = build_graph()

        register_run(run_id)
        initial = {"idea": "AI unified UPI tracker across banks", "run_id": run_id, "raw_sources": [], "errors": []}
        final = await graph.ainvoke(initial)

    assert final.get("report") is not None, "Report must be populated"
    assert "executive_summary" in final["report"], "Report must have executive_summary"
    assert isinstance(final["report"].get("validation_score"), int)
    assert 0 <= final["report"]["validation_score"] <= 100

    print(f"✓ Graph completed. Validation score: {final['report']['validation_score']}")
