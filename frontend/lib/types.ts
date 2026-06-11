export interface MarketSize {
  tam: string;
  sam: string;
  som: string;
  growth_rate: string;
}

export interface MarketResearchOutput {
  market_size: MarketSize;
  key_trends: string[];
  market_drivers: string[];
  market_barriers: string[];
  supporting_stats: string[];
  summary: string;
}

export interface Competitor {
  name: string;
  description: string;
  pricing: string;
  key_features: string[];
  target_segment: string;
  funding?: string;
  weakness: string;
}

export interface CompetitorOutput {
  direct_competitors: Competitor[];
  indirect_competitors: Competitor[];
  market_leaders: string[];
  summary: string;
}

export interface CommunityPainPoint {
  pain_point: string;
  frequency: string;
  source: string;
  example_quote?: string;
}

export interface CommunityOutput {
  pain_points: CommunityPainPoint[];
  feature_requests: string[];
  emotional_language: string[];
  underserved_segments: string[];
  summary: string;
}

export interface GapOutput {
  incumbent_shortcomings: string[];
  market_gaps: string[];
  underserved_segments: string[];
  how_to_win: string[];
  unique_value_proposition: string;
  differentiation_angle: string;
}

export interface Persona {
  name: string;
  role: string;
  age_range: string;
  pain_points: string[];
  goals: string[];
  willingness_to_pay: string;
  preferred_channels: string[];
  quote: string;
}

export interface PersonaOutput {
  personas: Persona[];
  primary_persona: string;
  target_segment_summary: string;
}

export interface PricingTier {
  name: string;
  price: string;
  features: string[];
  target_user: string;
}

export interface RevenueScenario {
  label: string;
  year_1_arr: string;
  year_3_arr: string;
  assumptions: string[];
}

export interface BusinessModelOutput {
  recommended_model: string;
  pricing_tiers: PricingTier[];
  monetization_strategies: string[];
  revenue_scenarios: RevenueScenario[];
  unit_economics_notes: string;
  summary: string;
}

export interface MvpFeature {
  feature: string;
  priority: string;
  effort: string;
  rationale: string;
}

export interface RoadmapPhase {
  phase: string;
  duration: string;
  goals: string[];
  deliverables: string[];
}

export interface MvpOutput {
  mvp_description: string;
  features: MvpFeature[];
  tech_stack_recommendation: string;
  architecture_notes: string;
  roadmap: RoadmapPhase[];
  launch_checklist: string[];
}

export interface Risk {
  category: string;
  risk: string;
  severity: string;
  mitigation: string;
}

export interface RiskOutput {
  risks: Risk[];
  devils_advocate: string[];
  critical_assumptions: string[];
  failure_modes: string[];
  overall_risk_level: string;
}

export interface ScoreBreakdown {
  label: string;
  score: number;
  rationale: string;
}

export interface ValidationReport {
  idea: string;
  executive_summary: string;
  problem_statement: string;
  market_research: MarketResearchOutput;
  competitors: CompetitorOutput;
  community: CommunityOutput;
  gap: GapOutput;
  personas: PersonaOutput;
  business_model: BusinessModelOutput;
  mvp: MvpOutput;
  risks: RiskOutput;
  go_to_market: string[];
  next_steps: string[];
  validation_score: number;
  validation_score_rationale: string;
  differentiation_score: number;
  differentiation_score_rationale: string;
  score_breakdown: ScoreBreakdown[];
}

export interface ProjectResponse {
  id: string;
  idea: string;
  status: "pending" | "running" | "completed" | "failed";
  created_at: string;
}

export type SSEEventType =
  | "agent_started"
  | "agent_completed"
  | "agent_failed"
  | "run_completed"
  | "run_not_found"
  | "error"
  | "keepalive";

export interface SSEEvent {
  event: SSEEventType;
  run_id: string;
  agent?: string;
  data?: unknown;
  error?: string;
}

export const AGENT_LABELS: Record<string, string> = {
  planner: "Planner",
  market_research: "Market Research",
  competitor: "Competitor Analysis",
  community: "Community Discovery",
  gap_opportunity: "Gap & Opportunity",
  persona: "Customer Personas",
  business_model: "Business Model",
  mvp: "MVP Planner",
  risk: "Risk Analysis",
  synthesis: "Report Synthesis",
};

export const AGENT_ORDER = Object.keys(AGENT_LABELS);
