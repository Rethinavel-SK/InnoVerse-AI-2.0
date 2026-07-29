# Risk Assessment Agent

Independent, modular AI agent built for the AI Innovation Discovery Platform.

## Features

- **Technical Risks**: Analyzes scalability, AI model limitations, API dependencies, and performance issues.
- **Financial Risks**: Evaluates development cost, cloud cost, and maintenance cost.
- **Legal Risks**: Assesses copyright, licensing, and regulatory compliance requirements.
- **Security Risks**: Identifies authentication, data leakage, prompt injection, and API security vulnerabilities.
- **Mitigation Suggestions**: Provides actionable, practical solutions for identified risks.
- **Overall Risk Score & Level**: Computes an aggregate score (0–100) and risk level (Low/Medium/High/Critical).

## Usage

```python
from agents.risk_assessment import execute

problem_statement = "Develop an AI platform to reduce food waste in restaurants."
result = execute(problem_statement)

print(result)
```

## Input Format

`problem_statement`: A string or dictionary `{"problem_statement": "..."}`.

## Output Format

Returns a dictionary matching the specified JSON schema:

```json
{
    "agent_name": "Risk Assessment Agent",
    "status": "success",
    "overall_risk_score": 62,
    "risk_level": "Medium",
    "technical_risks": [...],
    "financial_risks": [...],
    "legal_risks": [...],
    "security_risks": [...],
    "mitigation": [...],
    "summary": "..."
}
```
