import json
import logging
import os

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.schemes.models import Scheme
from apps.scholarships.models import Scholarship

from .gemini_client import ask_gemini
from .ai_serializers import (
    CareerChatSerializer,
    ResumeAnalyzerSerializer,
    SchemeRecommendationSerializer,
)
from .ai_services import (
    GeminiJsonService,
    GeminiServiceError,
    build_career_chat_prompt,
    build_resume_analysis_prompt,
    build_scheme_recommendation_prompt,
)

logger = logging.getLogger(__name__)


def get_mock_resume_analysis():
    """Mock response for resume analyzer when API is unavailable."""
    return {
        "ats_score": 72,
        "summary": "Good structure and relevant experience. Consider adding more quantifiable achievements and technical keywords.",
        "strengths": [
            "Clear chronological format",
            "Relevant work experience",
            "Good educational background"
        ],
        "improvements": [
            "Add more action verbs and quantifiable metrics",
            "Include technical skills and certifications",
            "Optimize for ATS with standard formatting"
        ],
        "missing_skills": [
            "Industry-specific technical skills",
            "Soft skills documentation",
            "Certifications and achievements"
        ],
        "keyword_recommendations": [
            "Project Management",
            "Data Analysis",
            "Team Leadership",
            "Problem Solving"
        ],
        "note": "[DEVELOPMENT MODE] Using mock response - Gemini API quota exceeded"
    }


def get_mock_career_chat():
    """Mock response for career chatbot when API is unavailable."""
    return {
        "answer": "Based on your profile, explore roles in your field that align with government schemes. Consider checking official portals like naukri.gov.in for government job opportunities and NSFDC for scholarship programs.",
        "action_items": [
            "Visit official government job portals",
            "Check eligibility for government schemes",
            "Prepare for competitive exams if applicable",
            "Network with mentors in your field"
        ],
        "related_topics": [
            "Government Job Preparation",
            "Scholarship Programs",
            "Skill Development",
            "Career Guidance"
        ],
        "note": "[DEVELOPMENT MODE] Using mock response - Gemini API quota exceeded"
    }


def use_mock_responses():
    """Check if we should use mock responses (for development)."""
    return os.getenv('USE_MOCK_AI_RESPONSES', 'False').lower() == 'true'


class AIResumeAnalyzerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResumeAnalyzerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        resume_text = serializer.validated_data["resume_text"]
        prompt = f"""
Analyze this resume.

Give:
1. ATS Score
2. Missing skills
3. Improvements
4. Strengths

Resume:
{resume_text}
"""
        try:
            reply = ask_gemini(prompt)
            return Response({"success": True, "data": {"reply": reply}}, status=status.HTTP_200_OK)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Resume analyzer API failed: %s", exc)
            
            # Use mock response in development mode
            if use_mock_responses():
                mock_data = get_mock_resume_analysis()
                return Response({"success": True, "data": mock_data}, status=status.HTTP_200_OK)
            
            return Response(
                {"success": False, "message": "AI service unavailable. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class AISchemeRecommendationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SchemeRecommendationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data
        age = payload["age"]
        category = payload["category"]
        income = payload["income"]
        education = payload["education"]

        prompt = f"""
Suggest Indian government schemes and scholarships.

User:
- Age: {age}
- Category: {category}
- Income: {income}
- Education: {education}

Give recommendations with reasons.
"""
        try:
            reply = ask_gemini(prompt)
            return Response({"success": True, "data": {"reply": reply}}, status=status.HTTP_200_OK)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Scheme recommendation API failed: %s", exc)
            
            # Use mock response in development mode
            if use_mock_responses():
                mock_data = get_mock_career_chat()  # Reusing similar format
                return Response({"success": True, "data": mock_data}, status=status.HTTP_200_OK)
            
            return Response(
                {"success": False, "message": "Recommendation service unavailable. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class AICareerChatbotAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CareerChatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payload = serializer.validated_data

        prompt = build_career_chat_prompt(
            question=payload["question"],
            education=payload.get("education", ""),
            age=payload.get("age"),
            category=payload.get("category", ""),
            income=payload.get("income"),
            history=payload.get("history", []),
        )
        service = GeminiJsonService()
        try:
            result = service.generate_json(prompt)
            return Response({"success": True, "data": result}, status=status.HTTP_200_OK)
        except GeminiServiceError as exc:
            logger.warning("Career chat API failed: %s", exc)
            
            # Use mock response in development mode
            if use_mock_responses():
                mock_data = get_mock_career_chat()
                return Response({"success": True, "data": mock_data}, status=status.HTTP_200_OK)
            
            return Response(
                {"success": False, "message": "Chat service unavailable. Please try again later."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Unexpected career chat error")
            
            # Use mock response in development mode
            if use_mock_responses():
                mock_data = get_mock_career_chat()
                return Response({"success": True, "data": mock_data}, status=status.HTTP_200_OK)
            
            return Response(
                {"success": False, "message": "Chat service encountered an error. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
