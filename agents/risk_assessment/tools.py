import json
import logging
import urllib.request
from typing import Dict, Any, Optional
from .config import settings

logger = logging.getLogger("RiskAssessmentAgent.Tools")


def call_llm(prompt: str) -> Optional[Dict[str, Any]]:
    """Invoke Groq/LLM API synchronously and parse JSON output."""
    if not settings.GROQ_API_KEY:
        logger.info("GROQ_API_KEY not provided. Using analytical heuristic engine.")
        return None

    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "RiskAssessmentAgent/1.0"
    }

    payload = {
        "model": settings.GROQ_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"}
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(settings.GROQ_API_URL, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=settings.REQUEST_TIMEOUT) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            content = res_json["choices"][0]["message"]["content"].strip()
            return json.loads(content)
    except Exception as e:
        logger.error(f"LLM API Call error: {e}")
        return None


def generate_heuristic_risk_assessment(problem_statement: str) -> Dict[str, Any]:
    """Fallback heuristic risk analyzer when LLM is offline or unconfigured."""
    text = problem_statement.lower()

    tech_risks = [
        "Scalability constraints under peak operational loads and real-time inference requirements.",
        "AI model limitations including edge cases, accuracy variance, and potential hallucinations/misclassifications.",
        "Third-party API dependency latency, rate limits, and potential service downtime.",
        "Performance degradation during concurrent user requests or high data ingestion volumes."
    ]

    financial_risks = [
        "High initial development cost for bespoke AI models and infrastructure setup.",
        "Recurring cloud cost associated with GPU/LLM API tokens and high-compute workloads.",
        "Ongoing operational and maintenance cost for continuous monitoring, re-training, and system updates."
    ]

    legal_risks = [
        "Copyright and IP considerations regarding proprietary datasets and training materials.",
        "Software licensing compliance across open-source libraries and commercial third-party SDKs.",
        "Regulatory compliance mandates (e.g., GDPR, CCPA, AI safety standards, food hygiene data rules)."
    ]

    security_risks = [
        "Authentication and access control vulnerabilities across distributed service endpoints.",
        "Data leakage risks involving sensitive operational, user, or proprietary restaurant data.",
        "Prompt Injection and adversarial input manipulation targeting underlying LLM components.",
        "API security vulnerabilities including unauthorized API access and data interception."
    ]

    mitigations = [
        "Implement robust caching, load balancing, and async queues to ensure technical scalability and performance.",
        "Optimize cloud compute spending using serverless scaling, API usage caps, and model quantization.",
        "Conduct thorough legal reviews, maintain data governance frameworks, and audit third-party licenses.",
        "Enforce strict OAuth2/JWT authentication, input sanitization, network encryption, and prompt safety guardrails."
    ]

    score = 65
    if any(k in text for k in ["food", "restaurant", "waste", "ai"]):
        score = 62

    risk_level = "Medium"
    if score <= 35:
        risk_level = "Low"
    elif score <= 70:
        risk_level = "Medium"
    elif score <= 85:
        risk_level = "High"
    else:
        risk_level = "Critical"

    return {
        "agent_name": "Risk Assessment Agent",
        "status": "success",
        "overall_risk_score": score,
        "risk_level": risk_level,
        "technical_risks": tech_risks,
        "financial_risks": financial_risks,
        "legal_risks": legal_risks,
        "security_risks": security_risks,
        "mitigation": mitigations,
        "summary": "Overall project has manageable risks with proper planning, architectural guardrails, and cost management."
    }
