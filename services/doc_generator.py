from typing import Dict, List, Any

class DocumentGenerator:
    """
    Automated Pitch Deck, Software Requirements Specification (SRS),
    and Technical Documentation Generator based on Innovation Director outputs.
    """

    @staticmethod
    def generate_pitch_deck(report: Dict[str, Any], problem_statement: str) -> List[Dict[str, Any]]:
        score = report.get("overall_innovation_score", 85)
        rec = report.get("recommendation", "GO")
        tech_arch = report.get("technical_summary", {}).get("architecture", {}).get("type", "Microservices Architecture")
        biz_model = report.get("business_summary", {}).get("business_model", "B2B Tiered SaaS")
        tam = report.get("business_summary", {}).get("market_size", {}).get("tam", "$4.8 Billion")
        timeline = report.get("roadmap_summary", {}).get("timeline", "24 Weeks")
        budget = report.get("roadmap_summary", {}).get("estimated_budget", "$140,000 - $180,000")

        return [
          {
            "slide_number": 1,
            "title": "Title & Vision",
            "subtitle": "AI-Powered Enterprise Innovation Platform",
            "bullets": [
              f"Project Problem: {problem_statement[:60]}...",
              f"Master Innovation Score: {score}/100",
              f"Investment Decision: {rec}"
            ]
          },
          {
            "slide_number": 2,
            "title": "The Problem",
            "subtitle": "Market Pain Point & Challenges",
            "bullets": [
              "High operational inefficiency & delayed prototype discovery cycles",
              "Fragmented market insights across patents, technology, and compliance",
              "Manual R&D evaluation takes months without automated AI synthesis"
            ]
          },
          {
            "slide_number": 3,
            "title": "The AI-Driven Solution",
            "subtitle": "Orchestrated Multi-Agent Discovery Engine",
            "bullets": [
              "Autonomous 9-Specialist AI Agent orchestration pipeline",
              "Sub-second analysis of architecture, market TAM, and legal risks",
              "Real-time RAG context retrieval from internal enterprise documents"
            ]
          },
          {
            "slide_number": 4,
            "title": "Market Opportunity",
            "subtitle": "Addressable Market Size (TAM/SAM/SOM)",
            "bullets": [
              f"Total Addressable Market (TAM): {tam}",
              "Serviceable Addressable Market (SAM): $650 Million",
              "Serviceable Obtainable Market (SOM): $45 Million (Phase 1)"
            ]
          },
          {
            "slide_number": 5,
            "title": "Business Model",
            "subtitle": "Monetization & Commercial Strategy",
            "bullets": [
              f"Primary Revenue Model: {biz_model}",
              "Enterprise Annual Recurring Revenue (ARR) seat licensing",
              "High gross margins (>82%) driven by optimized cloud LLM endpoints"
            ]
          },
          {
            "slide_number": 6,
            "title": "Technology Architecture",
            "subtitle": "Scalable Cloud Stack & Microservices",
            "bullets": [
              f"Architecture Pattern: {tech_arch}",
              "Next.js 15 App Router + Tailwind CSS frontend interface",
              "FastAPI AsyncIO gateway paired with Groq LLaMA-3 70B inference"
            ]
          },
          {
            "slide_number": 7,
            "title": "Competitive Analysis",
            "subtitle": "Unfair Advantages & Defensive Moats",
            "bullets": [
              "Proprietary inter-agent collaboration protocol & DAG consensus",
              "USPTO prior art patent clearance integrated at discovery time",
              "10x faster iteration speed vs traditional management consulting"
            ]
          },
          {
            "slide_number": 8,
            "title": "Go-To-Market Strategy",
            "subtitle": "Customer Acquisition & PLG",
            "bullets": [
              "Developer-led Product Led Growth (PLG) self-serve sandbox",
              "Direct sales outreach to Fortune 500 VP R&D and Innovation leads",
              "Strategic cloud marketplace co-selling partnerships"
            ]
          },
          {
            "slide_number": 9,
            "title": "Implementation Roadmap",
            "subtitle": "Phased Execution Plan",
            "bullets": [
              f"Estimated Development Horizon: {timeline}",
              "Phase 1 (W1-W8): Core API Gateway, RAG Ingestion & MVP UI",
              "Phase 2 (W9-W16): Enterprise SSO, Custom Agent Workflows & Pilot"
            ]
          },
          {
            "slide_number": 10,
            "title": "Financial Projections",
            "subtitle": "Capital Efficiency & Unit Economics",
            "bullets": [
              f"Estimated MVP Prototype Capital: {budget}",
              "Year 1 ARR Target: $1.2 Million across 25 enterprise accounts",
              "Break-even timeline: Month 14 post-commercial launch"
            ]
          },
          {
            "slide_number": 11,
            "title": "Team Recommendation",
            "subtitle": "Required Core Execution Squad",
            "bullets": [
              "1x Lead AI System Architect & Machine Learning Engineer",
              "2x Full-Stack Engineers (Next.js & FastAPI)",
              "1x Product Strategy & Enterprise Customer Success Lead"
            ]
          },
          {
            "slide_number": 12,
            "title": "The Investment Ask",
            "subtitle": "Seed Round Funding Request",
            "bullets": [
              "Seeking $1.5M Seed Capital for 18-month execution runway",
              "Use of Funds: 60% Engineering & R&D, 25% Go-To-Market, 15% Ops",
              "Join us in transforming enterprise R&D with autonomous AI agents"
            ]
          }
        ]

    @staticmethod
    def generate_srs_document(report: Dict[str, Any], problem_statement: str) -> List[Dict[str, Any]]:
        return [
          {"section": "1. Introduction", "content": f"This Software Requirements Specification (SRS) details functional requirements for solving: '{problem_statement}'."},
          {"section": "2. Purpose", "content": "Defines the system boundaries, target users, interfaces, and non-functional security constraints for enterprise deployment."},
          {"section": "3. Scope", "content": "Covers Next.js 15 UI, FastAPI Async backend, RAG Knowledge Base, and 9 Specialist AI Agent orchestrations."},
          {"section": "4. Product Overview", "content": "An autonomous AI platform that analyzes complex business problems and produces technical, business, and patent feasibility reports."},
          {"section": "5. Functional Requirements", "content": "REQ-1: User problem input submission.\nREQ-2: Real-time agent status polling.\nREQ-3: RAG document chunking & vector search.\nREQ-4: Inter-agent collaboration message logging."},
          {"section": "6. Non-Functional Requirements", "content": "NFR-1: API response latency < 500ms.\nNFR-2: 99.9% uptime SLA.\nNFR-3: End-to-end TLS 1.3 encryption and RBAC tenant isolation."},
          {"section": "7. User Stories", "content": "US-1: As an Innovation Lead, I want a 7-axis radar chart so I can visually pitch project feasibility to executives."},
          {"section": "8. Use Cases", "content": "UC-1: Execute Full Discovery Pipeline.\nUC-2: Upload RAG Knowledge PDF.\nUC-3: Export Investor Pitch Deck."},
          {"section": "9. System Architecture", "content": "Next.js 15 App Router ➔ FastAPI Gateway ➔ Groq LLaMA-3.3 70B & In-Memory Vector Store."},
          {"section": "10. Database Design", "content": "PostgreSQL relational tables for report histories + Vector store collections for chunk embeddings."},
          {"section": "11. API Specifications", "content": "RESTful endpoints for `/api/v1/agents/innovation-director/analyze`, `/api/v1/rag/upload`, `/api/v1/collaboration/logs`."},
          {"section": "12. Security Requirements", "content": "API key authentication, rate limiting (30 RPM cap), and sanitized prompt inputs against prompt injection."},
          {"section": "13. Deployment Requirements", "content": "Containerized via Docker, deployed on AWS ECS / Vercel with automated CI/CD pipelines."},
          {"section": "14. Testing Strategy", "content": "Unit testing with Pytest (100% pass), end-to-end integration tests, and Next.js build validation."},
          {"section": "15. Future Enhancements", "content": "Fine-tuned domain models, automated patent filing integrations, and voice-assisted agent pitch interactions."}
        ]

doc_generator = DocumentGenerator()
