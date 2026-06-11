from pydantic import BaseModel, Field
from typing import Optional


class PlanOutput(BaseModel):
    subtasks: list[str] = Field(description="List of research subtasks the agents should tackle")
    key_questions: list[str] = Field(description="Core questions this startup needs to answer")
    focus_areas: list[str] = Field(description="Key areas to investigate (market, tech, regulation, etc.)")


class MarketSize(BaseModel):
    tam: str = Field(description="Total Addressable Market estimate with source/reasoning")
    sam: str = Field(description="Serviceable Addressable Market")
    som: str = Field(description="Serviceable Obtainable Market (realistic first 3 years)")
    growth_rate: str = Field(description="Annual market growth rate and trend")


class MarketResearchOutput(BaseModel):
    market_size: MarketSize
    key_trends: list[str] = Field(description="3-5 major industry trends")
    market_drivers: list[str] = Field(description="Forces driving market growth")
    market_barriers: list[str] = Field(description="Factors slowing market adoption")
    supporting_stats: list[str] = Field(description="Key statistics and data points with sources")
    summary: str = Field(description="2-3 sentence market overview")


class Competitor(BaseModel):
    name: str
    description: str
    pricing: str
    key_features: list[str]
    target_segment: str
    funding: Optional[str] = None
    weakness: str = Field(description="Primary weakness or gap in their offering")


class CompetitorOutput(BaseModel):
    direct_competitors: list[Competitor]
    indirect_competitors: list[Competitor]
    market_leaders: list[str] = Field(description="Names of 1-3 dominant players")
    summary: str


class CommunityPainPoint(BaseModel):
    pain_point: str
    frequency: str = Field(description="How often this comes up: high/medium/low")
    source: str = Field(description="Reddit/HN/ProductHunt/etc")
    example_quote: Optional[str] = None


class CommunityOutput(BaseModel):
    pain_points: list[CommunityPainPoint]
    feature_requests: list[str] = Field(description="Most requested features users want")
    emotional_language: list[str] = Field(description="Phrases users use when expressing frustration")
    underserved_segments: list[str] = Field(description="Groups that feel ignored by current solutions")
    summary: str


class GapOutput(BaseModel):
    incumbent_shortcomings: list[str] = Field(description="Specific things existing products do poorly")
    market_gaps: list[str] = Field(description="Unmet needs or underserved niches")
    underserved_segments: list[str] = Field(description="Customer groups with no good solution today")
    how_to_win: list[str] = Field(description="Concrete strategies to beat incumbents")
    unique_value_proposition: str = Field(description="The single most compelling UVP (1-2 sentences)")
    differentiation_angle: str = Field(description="The core 10x differentiator vs. the market")


class Persona(BaseModel):
    name: str = Field(description="Fictional persona name")
    role: str
    age_range: str
    pain_points: list[str]
    goals: list[str]
    willingness_to_pay: str
    preferred_channels: list[str] = Field(description="Where they discover / buy products")
    quote: str = Field(description="One sentence in their voice expressing their frustration")


class PersonaOutput(BaseModel):
    personas: list[Persona] = Field(description="3-5 ICP personas")
    primary_persona: str = Field(description="Name of the highest-priority persona")
    target_segment_summary: str


class PricingTier(BaseModel):
    name: str
    price: str
    features: list[str]
    target_user: str


class RevenueScenario(BaseModel):
    label: str = Field(description="conservative / base / optimistic")
    year_1_arr: str
    year_3_arr: str
    assumptions: list[str]


class BusinessModelOutput(BaseModel):
    recommended_model: str = Field(description="SaaS / marketplace / freemium / etc.")
    pricing_tiers: list[PricingTier]
    monetization_strategies: list[str]
    revenue_scenarios: list[RevenueScenario]
    unit_economics_notes: str
    summary: str


class MvpFeature(BaseModel):
    feature: str
    priority: str = Field(description="must-have / nice-to-have / future")
    effort: str = Field(description="low / medium / high")
    rationale: str


class RoadmapPhase(BaseModel):
    phase: str = Field(description="Phase 1 / Phase 2 / Phase 3")
    duration: str
    goals: list[str]
    deliverables: list[str]


class MvpOutput(BaseModel):
    mvp_description: str = Field(description="One paragraph describing the minimal viable product")
    features: list[MvpFeature]
    tech_stack_recommendation: str
    architecture_notes: str
    roadmap: list[RoadmapPhase]
    launch_checklist: list[str]


class Risk(BaseModel):
    category: str = Field(description="market / technical / legal / competitive / execution")
    risk: str
    severity: str = Field(description="high / medium / low")
    mitigation: str


class RiskOutput(BaseModel):
    risks: list[Risk]
    devils_advocate: list[str] = Field(description="Hardest questions investors will ask")
    critical_assumptions: list[str] = Field(description="Assumptions the business model depends on")
    failure_modes: list[str] = Field(description="Most likely ways this startup fails")
    overall_risk_level: str = Field(description="high / medium / low with one-sentence justification")


class ScoreBreakdown(BaseModel):
    label: str
    score: int = Field(ge=0, le=25)
    rationale: str


class ValidationReport(BaseModel):
    idea: str
    executive_summary: str = Field(description="3-5 sentence VC-style executive summary")
    problem_statement: str
    market_research: MarketResearchOutput
    competitors: CompetitorOutput
    community: CommunityOutput
    gap: GapOutput
    personas: PersonaOutput
    business_model: BusinessModelOutput
    mvp: MvpOutput
    risks: RiskOutput
    go_to_market: list[str] = Field(description="Top 5-7 actionable GTM steps")
    next_steps: list[str] = Field(description="Immediate 30-day action items")
    validation_score: int = Field(ge=0, le=100, description="Overall opportunity score 0-100")
    validation_score_rationale: str
    differentiation_score: int = Field(ge=0, le=100, description="How differentiated vs. existing players 0-100")
    differentiation_score_rationale: str
    score_breakdown: list[ScoreBreakdown]
