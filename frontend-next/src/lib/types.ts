export type AgentStatus = "idle" | "waiting" | "running" | "completed" | "failed" | "Unavailable" | "Completed";

export interface AgentInfo {
  id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
}

export const AGENTS: AgentInfo[] = [
  { id: "solution_architect", name: "Solution Architect", description: "Technical architecture, stack, feasibility", icon: "🏗️", color: "#6366f1" },
  { id: "business_strategy", name: "Business Strategy", description: "Business model, TAM/SAM/SOM, GTM", icon: "📈", color: "#10b981" },
  { id: "research", name: "Research Discovery", description: "arXiv & Semantic Scholar paper synthesis", icon: "🔬", color: "#3b82f6" },
  { id: "patent_analysis", name: "Patent Intelligence", description: "USPTO prior art, novelty scoring", icon: "🛡️", color: "#06b6d4" },
  { id: "market_analysis", name: "Market Intelligence", description: "Target market, customer personas", icon: "📊", color: "#8b5cf6" },
  { id: "trend_analysis", name: "Trend Intelligence", description: "Tech hype cycle & adoption phase", icon: "⚡", color: "#f59e0b" },
  { id: "risk_assessment", name: "Risk Assessment", description: "Technical, financial, legal & security risks", icon: "⚠️", color: "#ef4444" },
  { id: "sustainability", name: "Sustainability", description: "ESG score, carbon footprint, SDGs", icon: "🌱", color: "#22c55e" },
  { id: "mvp_roadmap", name: "MVP & Roadmap Planner", description: "Features, timelines, team & budget", icon: "🗺️", color: "#ec4899" },
];

export interface AgentExplainability {
  why_selected: string;
  key_assumptions: string[];
  alternatives_considered: string[];
  decision_logic: string;
  confidence_score: number;
}

export interface ConflictResolutionItem {
  agents_involved: string[];
  conflict_description: string;
  comparison: string;
  resolution: string;
  reasoning: string;
}

export interface FinalRecommendation {
  build_recommendation: string;
  expected_success_probability?: string;
  implementation_strategy: string;
  suggested_deployment_phases?: string[];
  commercial_viability: string;
  investment_priority?: string;
  future_scope?: string[];
}

export interface Paper {
  title: string;
  authors?: string[] | string;
  year?: number | string;
  summary?: string;
  url?: string;
}

export interface InnovationReport {
  executive_summary: string;
  problem_understanding: string;
  agent_status?: Record<string, string>;
  technical_summary?: {
    architecture?: { type: string; rationale?: string; why_alternatives_were_not_selected?: string };
    estimated_complexity?: string;
    prototype_cost?: string;
    production_cost?: string;
    technology_recommendations?: Record<string, { technology?: string; reason?: string; why_alternatives_not_selected?: string } | string>;
    tech_stack?: string[];
    feasibility_score?: number;
    explainability?: AgentExplainability;
  };
  business_summary?: {
    business_model?: string;
    value_proposition?: string;
    pricing_model?: string;
    go_to_market?: string;
    market_size?: { tam?: string; sam?: string; som?: string; rationale?: string };
    swot?: { strengths?: string[]; weaknesses?: string[]; opportunities?: string[]; threats?: string[] };
    confidence?: number;
    explainability?: AgentExplainability;
  };
  research_summary?: {
    research_summary?: string;
    papers?: Paper[];
    research_gaps?: string[];
    explainability?: AgentExplainability;
  };
  patent_summary?: {
    novelty_score?: number;
    score?: number;
    analysis?: string;
    patent_summary?: string;
    whitespace_opportunities?: string[];
    explainability?: AgentExplainability;
  };
  market_summary?: {
    target_market?: string;
    customer_personas?: string[];
    market_growth_drivers?: string[];
    explainability?: AgentExplainability;
  };
  trend_summary?: {
    adoption_lifecycle_phase?: string;
    hype_cycle_position?: string;
    emerging_technologies?: string[];
    trend_score?: number;
    explainability?: AgentExplainability;
  };
  risk_summary?: {
    overall_risk_score?: number;
    risk_level?: string;
    technical_risks?: string[];
    financial_risks?: string[];
    legal_risks?: string[];
    security_risks?: string[];
    mitigation?: string[];
    summary?: string;
    explainability?: AgentExplainability;
  };
  sustainability_summary?: {
    esg_compliance_score?: number;
    sustainability_score?: number;
    carbon_footprint_impact?: string;
    sdg_alignment?: string[];
    sustainability_recommendations?: string[];
    explainability?: AgentExplainability;
  };
  roadmap_summary?: {
    timeline?: string;
    estimated_budget?: string;
    team_size?: string;
    mvp_features?: Array<{ feature: string; description: string; priority: string; complexity: string }>;
    explainability?: AgentExplainability;
  };
  conflict_resolution?: Array<ConflictResolutionItem | string>;
  overall_innovation_score?: number;
  feasibility_score?: number;
  confidence?: number;
  final_recommendation?: FinalRecommendation | { build_recommendation?: string; expected_success_probability?: string; implementation_strategy?: string; suggested_deployment_phases?: string[]; commercial_viability?: string };
  recommendation?: string;
}

export interface SavedAnalysis {
  id: string;
  problem_statement: string;
  created_at: string;
  score: number;
  recommendation: string;
  domain?: string;
  report?: InnovationReport;
}

export interface AnalysisOptions {
  industry?: string;
  budget?: string;
  expectedUsers?: string;
  timeline?: string;
  aiRequired?: boolean;
  realTimeProcessing?: boolean;
  iot?: boolean;
  analytics?: boolean;
  securityLevel?: string;
}

export interface ExecutionLog {
  timestamp: string;
  agentId: string;
  agentName: string;
  level: "info" | "warn" | "error" | "success";
  message: string;
}

export interface AgentMetrics {
  id: string;
  name: string;
  status: AgentStatus;
  executionTimeMs: number;
  confidenceScore: number;
  tokenUsage: { promptTokens: number; completionTokens: number; totalTokens: number };
  modelUsed: string;
  lastExecutionTime: string;
}

export interface ExecutionTimelineStep {
  step: string;
  description: string;
  timestamp: string;
  status: "completed" | "running" | "waiting";
}

export interface ChatMessage {
  id: string;
  sender: "user" | "assistant";
  content: string;
  timestamp: string;
}

export interface KnowledgeDocument {
  doc_id: string;
  filename: string;
  file_type: string;
  upload_date: string;
  total_chunks: number;
  content_preview: string;
}

export interface DocumentChunk {
  chunk_id: string;
  doc_id: string;
  doc_name: string;
  chunk_index: number;
  content: string;
  score: number;
}

export interface InterAgentMessage {
  sender_id: string;
  target_id: string;
  topic: string;
  content: string;
  timestamp: string;
}

export interface PitchDeckSlide {
  slide_number: number;
  title: string;
  subtitle: string;
  bullets: string[];
}

export interface SRSSection {
  section: string;
  content: string;
}
