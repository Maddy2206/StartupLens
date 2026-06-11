from langgraph.graph import StateGraph, END
from app.agents.state import ValidationState
from app.agents.planner import planner_node
from app.agents.market_research import market_research_node
from app.agents.competitor import competitor_node
from app.agents.community import community_node
from app.agents.gap_opportunity import gap_opportunity_node
from app.agents.persona import persona_node
from app.agents.business_model import business_model_node
from app.agents.mvp import mvp_node
from app.agents.risk import risk_node
from app.agents.synthesis import synthesis_node


def build_graph():
    builder = StateGraph(ValidationState)

    # Node names must not clash with ValidationState keys.
    # Conflicting keys: market_research, community, business_model, mvp → append _agent suffix.
    builder.add_node("planner", planner_node)
    builder.add_node("market_research_agent", market_research_node)
    builder.add_node("competitor_agent", competitor_node)
    builder.add_node("community_agent", community_node)
    builder.add_node("gap_opportunity", gap_opportunity_node)
    builder.add_node("persona_agent", persona_node)
    builder.add_node("business_model_agent", business_model_node)
    builder.add_node("mvp_agent", mvp_node)
    builder.add_node("risk_agent", risk_node)
    builder.add_node("synthesis", synthesis_node)

    # Entry point
    builder.set_entry_point("planner")

    # Planner → parallel fan-out
    builder.add_edge("planner", "market_research_agent")
    builder.add_edge("planner", "competitor_agent")
    builder.add_edge("planner", "community_agent")

    # All three → gap_opportunity (fan-in via distinct state keys)
    builder.add_edge("market_research_agent", "gap_opportunity")
    builder.add_edge("competitor_agent", "gap_opportunity")
    builder.add_edge("community_agent", "gap_opportunity")

    # gap_opportunity → parallel fan-out
    builder.add_edge("gap_opportunity", "persona_agent")
    builder.add_edge("gap_opportunity", "business_model_agent")
    builder.add_edge("gap_opportunity", "mvp_agent")

    # Three parallel → risk
    builder.add_edge("persona_agent", "risk_agent")
    builder.add_edge("business_model_agent", "risk_agent")
    builder.add_edge("mvp_agent", "risk_agent")

    # risk → synthesis → END
    builder.add_edge("risk_agent", "synthesis")
    builder.add_edge("synthesis", END)

    return builder.compile()


_graph = None


def get_graph():
    global _graph
    if _graph is None:
        _graph = build_graph()
    return _graph
