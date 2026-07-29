from agents.risk_assessment import execute, RiskAssessmentAgent

def test_risk_assessment_execute_success_str():
    input_str = "Develop an AI platform to reduce food waste in restaurants."
    res = execute(input_str)
    
    assert isinstance(res, dict)
    assert res.get("agent_name") == "Risk Assessment Agent"
    assert res.get("status") == "success"
    assert "overall_risk_score" in res
    assert 0 <= res["overall_risk_score"] <= 100
    assert "risk_level" in res
    assert isinstance(res.get("technical_risks"), list)
    assert isinstance(res.get("financial_risks"), list)
    assert isinstance(res.get("legal_risks"), list)
    assert isinstance(res.get("security_risks"), list)
    assert isinstance(res.get("mitigation"), list)
    assert isinstance(res.get("summary"), str)


def test_risk_assessment_execute_success_dict():
    input_dict = {"problem_statement": "Develop an AI platform to reduce food waste in restaurants."}
    res = execute(input_dict)
    
    assert isinstance(res, dict)
    assert res.get("status") == "success"


def test_risk_assessment_empty_input():
    res = execute("")
    assert res.get("status") == "failed"
    assert "error" in res


def test_risk_assessment_invalid_input():
    res = execute(None)
    assert res.get("status") == "failed"
    assert "error" in res


if __name__ == "__main__":
    test_risk_assessment_execute_success_str()
    test_risk_assessment_execute_success_dict()
    test_risk_assessment_empty_input()
    test_risk_assessment_invalid_input()
    print("SUCCESS: All Risk Assessment Agent unit tests passed!")
