# 🏢 Business Strategy Agent

A **production-ready AI agent** that performs a complete **11-step business strategy analysis** for any business idea or problem statement. Built on **Groq's LLM API** (`llama-3.3-70b-versatile`) with async architecture, Pydantic schemas, structured logging, and full unit + integration test coverage.

---

## 📋 Responsibilities

| # | Responsibility | Output Field |
|---|---|---|
| 1 | Identify Customer Segments | `target_customers` |
| 2 | Define Value Proposition | `value_proposition` |
| 3 | Recommend Pricing Model | `pricing_model` |
| 4 | Generate Business Model | `business_model` |
| 5 | Create Revenue Streams | `revenue_streams` |
| 6 | Suggest Go-to-Market Strategy | `go_to_market` |
| 7 | Recommend Marketing Channels | `marketing_channels` |
| 8 | Estimate Market Size (TAM/SAM/SOM) | `market_size` |
| 9 | Identify Competitors | `competitors` |
| 10 | Perform SWOT Analysis | `swot` |
| 11 | Generate Business Model Canvas | `business_canvas` |

---

## 🗂 Project Structure

```
agents/business_strategy/
├── __init__.py                      # Public package API
├── agent.py                         # Main orchestrator (BusinessStrategyAgent)
├── config.py                        # Pydantic settings (Groq key, model, timeouts)
├── models/
│   ├── __init__.py
│   └── domain.py                    # ExecutionMetadata, BusinessStrategyResult
├── prompts/
│   ├── __init__.py
│   └── system_prompt.py             # 11-step expert system prompt + user prompt builder
├── schemas/
│   ├── __init__.py
│   └── strategy_schema.py           # All Pydantic input/output schemas
├── services/
│   ├── __init__.py
│   └── strategy_service.py          # Core reasoning engine (LLM call + parsing)
└── tests/
    ├── __init__.py
    ├── test_agent.py                 # Unit tests (mocked LLM, CI-safe)
    └── test_groq_integration.py     # Live Groq integration tests (real API calls)
```

---

## ⚡ Quick Start

### 1. Set up environment

```bash
# .env
GROQ_API_KEY="your-groq-api-key-here"
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the agent (Python)

```python
import asyncio
from agents.business_strategy import BusinessStrategyAgent

agent = BusinessStrategyAgent()

response = asyncio.run(agent.run(
    "Build an AI-powered platform that helps small restaurants manage "
    "inventory and reduce food waste using predictive analytics."
))

print(response.business_model)
print(response.value_proposition)
print(response.pricing_model)
print(response.market_size.tam)
print(response.swot.strengths)
```

### 4. With additional context

```python
response = asyncio.run(agent.run(
    problem_statement="Build a B2B SaaS for HR teams to automate onboarding.",
    context={
        "target_region": "North America",
        "company_stage": "Seed",
        "budget": "$750K",
        "team_size": "6 engineers",
    }
))
```

### 5. Full pipeline (with execution metadata)

```python
from agents.business_strategy.schemas.strategy_schema import BusinessStrategyRequest

request = BusinessStrategyRequest(
    problem_statement="Build a D2C subscription box for premium pet food."
)

result = asyncio.run(agent.execute_full_pipeline(request))

print(result.request_id)              # UUID
print(result.metadata.agent_name)    # BusinessStrategyAgent
print(result.metadata.execution_time_ms)
print(result.strategy_output)        # Full strategy dict
```

---

## 📥 Input Schema

```json
{
  "problem_statement": "A description of the business idea or problem to analyse.",
  "context": {
    "region": "North America",
    "stage": "Pre-seed",
    "budget": "$500K"
  }
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `problem_statement` | `str` (min 10 chars) | ✅ | The business idea or problem to analyse |
| `context` | `dict` (optional) | ❌ | Hints: region, stage, budget, team size, etc. |

---

## 📤 Output Schema

```json
{
  "target_customers": [
    {
      "segment_name": "SMB Restaurant Owners",
      "description": "Independent restaurant owners facing 10-15% food waste losses.",
      "size_estimate": "~1.5M restaurants in the US",
      "willingness_to_pay": "Medium"
    }
  ],
  "value_proposition": "We help SMB restaurant owners who...",
  "pricing_model": "Tiered SaaS: Starter $49/mo, Pro $149/mo, Enterprise custom",
  "business_model": "B2B SaaS — restaurants subscribe per location...",
  "revenue_streams": [
    {
      "stream_name": "SaaS Subscription",
      "description": "Monthly/annual plans billed per location.",
      "estimated_contribution": "75% of revenue"
    }
  ],
  "go_to_market": "Phase 1 (0-6mo): Target independent restaurants in 2 US metros...",
  "marketing_channels": ["Content Marketing / SEO", "LinkedIn Outbound"],
  "market_size": {
    "tam": "$12B — Global restaurant management software",
    "sam": "$3B — US SMB cloud SaaS adoption",
    "som": "$150M — Achievable in 5 years",
    "rationale": "Bottom-up: 1.5M restaurants × 40% SaaS adoption × $250 ARPU"
  },
  "competitors": [
    {
      "name": "MarketMan",
      "strengths": "Established brand, deep POS integrations.",
      "weaknesses": "Complex UX, no AI features.",
      "differentiation": "AI-first waste prediction vs. manual configuration."
    }
  ],
  "swot": {
    "strengths": ["AI-driven waste prediction as core differentiator"],
    "weaknesses": ["No brand awareness vs. incumbents"],
    "opportunities": ["Post-pandemic restaurant digitisation wave"],
    "threats": ["Toast/Square launching native AI features"]
  },
  "business_canvas": {
    "key_partners": ["POS vendors (Toast, Square)"],
    "key_activities": ["AI model development", "POS integration"],
    "key_resources": ["Proprietary ML model", "Engineering team"],
    "value_propositions": ["Reduce food waste by 40% using AI"],
    "customer_relationships": ["Self-service onboarding", "Dedicated CSM"],
    "channels": ["Direct website", "POS marketplace"],
    "customer_segments": ["SMB independent restaurants"],
    "cost_structure": ["Cloud infrastructure", "Engineering salaries"],
    "revenue_streams": ["Monthly SaaS subscription", "Marketplace commission"]
  },
  "reasoning": ["Step 1: ...", "Step 2: ...", "... Step 11: ..."],
  "confidence": 0.87
}
```

---

## 🧪 Running Tests

### Unit Tests (No API key needed — CI safe)

```bash
pytest agents/business_strategy/tests/test_agent.py -v
```

### Live Integration Tests (Requires GROQ_API_KEY)

```bash
pytest agents/business_strategy/tests/test_groq_integration.py -v -s
```

### All tests

```bash
pytest agents/business_strategy/tests/ -v -s
```

---

## ⚙️ Configuration

Configured via `.env` and `config.py`:

| Setting | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | — | Your Groq API key (required) |
| `model_name` | `llama-3.3-70b-versatile` | Groq model (best quality for business reasoning) |
| `temperature` | `0.3` | Slight creativity for strategy generation |
| `max_tokens` | `4000` | Sufficient for full 11-component output |
| `request_timeout` | `60.0s` | Extended timeout for complex reasoning |

---

## 🏛 Architecture

```
BusinessStrategyAgent          ← Orchestrator (agent.py)
        │
        ▼
BusinessStrategyService        ← Reasoning engine (services/strategy_service.py)
        │
        ├── validate_problem_statement()   ← Input validation
        ├── _call_llm()                    ← Async Groq API call
        └── _parse_json_response()         ← JSON parsing + cleanup
                │
                ▼
        BusinessStrategyResponse           ← Pydantic output model (schemas/)
                │
                ▼
        BusinessStrategyResult             ← Full pipeline result with metadata (models/)
```

---

## 🔒 Error Handling

| Scenario | HTTP Status | Detail |
|---|---|---|
| Missing/invalid problem statement | `400 Bad Request` | Validation error message |
| Missing GROQ_API_KEY | `503 Service Unavailable` | API key missing message |
| Groq API down or timeout | `503 Service Unavailable` | LLM unavailable message |
| JSON parse failure | `503 Service Unavailable` | Unexpected response message |

---

## 📦 Dependencies

```
groq>=0.11.0
fastapi>=0.110.0
pydantic>=2.6.0
pydantic-settings>=2.2.0
python-dotenv>=1.0.1
pytest>=8.0.0
pytest-asyncio>=0.23.0
```
