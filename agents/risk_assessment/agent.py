import logging
from typing import Dict, Any, Union
from .schemas import RiskAssessmentRequest, RiskAssessmentResponse, ErrorResponse
from .prompts import RISK_ASSESSMENT_PROMPT
from .tools import call_llm, generate_heuristic_risk_assessment

logger = logging.getLogger("RiskAssessmentAgent")


class RiskAssessmentAgent:
    """Production-Ready Independent Risk Assessment Agent.

    Analyzes startup problem statements across Technical, Financial, Legal, and Security risks,
    providing actionable mitigations, an overall risk score, and risk level.
    """

    def analyze(self, problem_statement: Union[str, Dict[str, Any], RiskAssessmentRequest]) -> Dict[str, Any]:
        """Execute risk assessment given a problem statement."""
        # 1. Input Validation & Parsing
        raw_statement = ""
        if isinstance(problem_statement, str):
            raw_statement = problem_statement
        elif isinstance(problem_statement, dict):
            raw_statement = problem_statement.get("problem_statement", "")
        elif isinstance(problem_statement, RiskAssessmentRequest):
            raw_statement = problem_statement.problem_statement

        if not raw_statement or not isinstance(raw_statement, str) or not raw_statement.strip():
            return ErrorResponse(status="failed", error="Invalid or empty problem statement provided.").model_dump()

        raw_statement = raw_statement.strip()

        try:
            # 2. Try LLM Call
            prompt = RISK_ASSESSMENT_PROMPT.format(problem_statement=raw_statement)
            llm_result = call_llm(prompt)

            if llm_result and isinstance(llm_result, dict):
                # Ensure structure integrity
                if "overall_risk_score" in llm_result:
                    # Enforce strict field presence & schema validation
                    validated = RiskAssessmentResponse(
                        agent_name="Risk Assessment Agent",
                        status="success",
                        overall_risk_score=int(llm_result.get("overall_risk_score", 65)),
                        risk_level=str(llm_result.get("risk_level", "Medium")),
                        technical_risks=llm_result.get("technical_risks", []),
                        financial_risks=llm_result.get("financial_risks", []),
                        legal_risks=llm_result.get("legal_risks", []),
                        security_risks=llm_result.get("security_risks", []),
                        mitigation=llm_result.get("mitigation", []),
                        summary=str(llm_result.get("summary", "Risk assessment completed successfully."))
                    )
                    return validated.model_dump()

            # 3. Fallback to analytical heuristic model
            heuristic_result = generate_heuristic_risk_assessment(raw_statement)
            validated = RiskAssessmentResponse(**heuristic_result)
            return validated.model_dump()

        except Exception as e:
            logger.error(f"Error executing risk assessment: {e}")
            return ErrorResponse(status="failed", error=f"LLM failure or execution error: {str(e)}").model_dump()


# Singleton instance
risk_assessment_agent = RiskAssessmentAgent()


def execute(problem_statement: Any) -> Dict[str, Any]:
    """Exposed single public function as required by specification.

    Accepts problem statement input and returns ONLY the structured JSON response dictionary.
    Do not print anything.
    """
    return risk_assessment_agent.analyze(problem_statement)
