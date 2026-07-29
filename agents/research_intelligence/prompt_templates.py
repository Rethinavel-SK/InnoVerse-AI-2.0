"""Prompt templates for Research Intelligence Agent LLM operations."""

KEYWORD_EXTRACTION_PROMPT = """
You are an expert AI Research Assistant.
Given the following problem statement, extract 2-4 search queries/keywords optimized for academic search engines (arXiv, Semantic Scholar, CrossRef).

Problem Statement: "{problem_statement}"

Output your response as a JSON array of strings only.
Example format:
["food waste reduction AI", "restaurant waste management machine learning", "computer vision food waste prediction"]
"""

PAPER_ANALYSIS_PROMPT = """
You are an AI Research Analyst. Analyze the following collected research paper abstracts based on the user's problem statement: "{problem_statement}".

Collected Papers:
{papers_text}

Provide a detailed structured analysis matching the exact JSON schema requested:

Output schema requirement:
{{
   "research_summary": "<A comprehensive overall summary synthesizing key findings from all papers regarding the problem statement>",
   "papers": [
      {{
         "title": "<Paper Title>",
         "authors": "<Comma-separated authors>",
         "year": "<Publication Year>",
         "summary": "<Concise summary of paper>",
         "methodology": "<Methodology or technical approach used>",
         "dataset": "<Dataset used or mentioned in paper>",
         "results": "<Key results, metrics, or performance outcomes>"
      }}
   ],
   "research_gaps": [
      "<Identified research gap 1>",
      "<Identified research gap 2>"
   ],
   "recommended_datasets": [
      "<Recommended dataset name or source 1>",
      "<Recommended dataset name or source 2>"
   ],
   "confidence_score": <Float value between 0.0 and 1.0 estimating confidence/completeness of available literature>
}}

Return ONLY valid JSON.
"""
