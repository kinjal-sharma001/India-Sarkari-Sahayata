import json
import logging
import os
import re
from typing import Any

from google import genai

logger = logging.getLogger(__name__)


class GeminiServiceError(Exception):
    """Raised when Gemini request/configuration fails."""


class GeminiJsonService:
    def __init__(self, model_name: str = "gemini-2.0-flash"):
        self.model_name = model_name

    def _get_client(self):
        api_key = (os.getenv("GEMINI_API_KEY") or "").strip()
        if not api_key:
            raise GeminiServiceError("Gemini API key is not configured.")
        try:
            return genai.Client(api_key=api_key)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Failed to initialize Gemini client")
            raise GeminiServiceError("Failed to initialize Gemini client.") from exc

    def _extract_json(self, text: str) -> dict[str, Any]:
        cleaned = (text or "").strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
            if not match:
                raise GeminiServiceError("Gemini returned invalid JSON response.")
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError as exc:
                raise GeminiServiceError("Gemini returned malformed JSON data.") from exc

    def generate_json(self, prompt: str) -> dict[str, Any]:
        client = self._get_client()
        try:
            response = client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Gemini content generation failed")
            raise GeminiServiceError(f"Gemini request failed: {exc}") from exc
        text = getattr(response, "text", "") or ""
        if not text:
            raise GeminiServiceError("Gemini returned an empty response.")
        return self._extract_json(text)


def build_resume_analysis_prompt(resume_text: str) -> str:
    return f"""
You are an expert ATS resume reviewer.
Analyze the resume text and return ONLY valid JSON with this schema:
{{
  "ats_score": integer from 0 to 100,
  "summary": "2-3 line overall review",
  "strengths": ["strength 1", "strength 2"],
  "improvements": ["specific improvement 1", "specific improvement 2"],
  "missing_skills": ["skill 1", "skill 2"],
  "keyword_recommendations": ["keyword 1", "keyword 2"]
}}
No markdown, no code fences, no extra text.

Resume text:
{resume_text}
""".strip()


def build_scheme_recommendation_prompt(
    age: int,
    category: str,
    income: float,
    education: str,
    schemes: list[dict[str, Any]],
    scholarships: list[dict[str, Any]],
) -> str:
    return f"""
You are a government welfare and scholarship guidance assistant for India.
Using the user profile and opportunity catalog, recommend relevant schemes and scholarships.
Return ONLY valid JSON using this schema:
{{
  "profile_summary": "short summary of user eligibility profile",
  "recommendations": [
    {{
      "title": "scheme or scholarship name",
      "type": "scheme|scholarship",
      "recommendation_reason": "short reason for recommendation",
      "eligibility_match_score": integer from 0 to 100
    }}
  ],
  "notes": ["important caution or note"]
}}
Return 5-8 recommendations total.
No markdown, no code fences, no extra text.

User profile:
- age: {age}
- category: {category}
- annual_income: {income}
- education: {education}

Schemes catalog:
{json.dumps(schemes, ensure_ascii=True)}

Scholarships catalog:
{json.dumps(scholarships, ensure_ascii=True)}
""".strip()


def build_career_chat_prompt(
    question: str,
    education: str,
    age: int | None,
    category: str,
    income: float | None,
    history: list[dict[str, str]],
) -> str:
    return f"""
You are an India government opportunity and career assistant.
You answer about jobs, careers, scholarships, and schemes.
Be practical, concise, and avoid fabricated facts.
If uncertain, state assumptions and suggest verification on official portals.

Return ONLY valid JSON:
{{
  "answer": "direct helpful answer in 4-8 lines",
  "action_items": ["next step 1", "next step 2"],
  "related_topics": ["topic 1", "topic 2"]
}}
No markdown, no code fences, no extra text.

User context:
- education: {education or "not provided"}
- age: {age if age is not None else "not provided"}
- category: {category or "not provided"}
- annual_income: {income if income is not None else "not provided"}

Recent chat history:
{json.dumps(history[-6:], ensure_ascii=True)}

User question:
{question}
""".strip()
