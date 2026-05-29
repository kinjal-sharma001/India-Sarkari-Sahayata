import logging
import os

import requests
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.scholarships.models import Scholarship
from apps.schemes.models import Scheme

from .serializers import ScholarshipSerializer, SchemeSerializer
from .ai_services import GeminiJsonService, GeminiServiceError

logger = logging.getLogger(__name__)

APP_ID = os.getenv("ADZUNA_APP_ID", os.getenv("APP_ID", "")).strip()
APP_KEY = os.getenv("ADZUNA_APP_KEY", os.getenv("APP_KEY", "")).strip()


class GovernmentJobListAPIView(APIView):
    """
    Fetch government-like jobs dynamically from Adzuna India API.
    Env vars required for live API:
    - ADZUNA_APP_ID
    - ADZUNA_APP_KEY
    """

    permission_classes = [AllowAny]
    authentication_classes: list = []

    def get(self, request):
        query = (request.query_params.get("search") or "government").strip()
        category = (request.query_params.get("category") or "").strip()

        try:
            page = int(request.query_params.get("page") or 1)
            page = max(1, page)
        except ValueError:
            return Response(
                {
                    "success": False,
                    "message": "Invalid page value. Page must be an integer >= 1.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        app_id = APP_ID
        app_key = APP_KEY
        if not app_id or not app_key:
            return Response(
                {
                    "success": False,
                    "message": "Adzuna credentials are not configured.",
                    "details": "Set ADZUNA_APP_ID/ADZUNA_APP_KEY or APP_ID/APP_KEY environment variables.",
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        url = f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"
        params = {
            "app_id": app_id,
            "app_key": app_key,
            "results_per_page": 20,
            "what": query,
            "content-type": "application/json",
        }
        if category:
            params["category"] = category

        try:
            upstream_resp = requests.get(url, params=params, timeout=20)
            upstream_resp.raise_for_status()
            upstream_data = upstream_resp.json()
        except requests.exceptions.Timeout:
            return Response(
                {
                    "success": False,
                    "message": "Adzuna API timeout. Please try again.",
                },
                status=status.HTTP_504_GATEWAY_TIMEOUT,
            )
        except requests.exceptions.RequestException as exc:
            return Response(
                {
                    "success": False,
                    "message": "Failed to fetch jobs from Adzuna API.",
                    "details": str(exc),
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )

        results = []
        for item in upstream_data.get("results", []):
            results.append(
                {
                    "title": item.get("title", ""),
                    "company": (item.get("company") or {}).get("display_name", ""),
                    "location": (item.get("location") or {}).get("display_name", ""),
                    "apply_link": item.get("redirect_url", ""),
                    "category": (item.get("category") or {}).get("label", ""),
                    "created_at": item.get("created", ""),
                }
            )

        return Response(
            {
                "success": True,
                "message": "Government jobs fetched successfully.",
                "count": len(results),
                "page": page,
                "results": results,
            },
            status=status.HTTP_200_OK,
        )


class SchemeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Database-backed schemes endpoint.
    Supports:
    - search: name/category/description/eligibility
    - category: exact, case-insensitive
    - eligibility: partial match
    """

    serializer_class = SchemeSerializer
    permission_classes = [AllowAny]
    queryset = Scheme.objects.all()
    search_fields = ["name", "category", "description", "eligibility"]
    ordering_fields = ["name", "category"]
    ordering = ["name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = (self.request.query_params.get("category") or "").strip()
        eligibility = (self.request.query_params.get("eligibility") or "").strip()
        search = (self.request.query_params.get("search") or "").strip()

        if category:
            queryset = queryset.filter(category__iexact=category)
        if eligibility:
            queryset = queryset.filter(eligibility__icontains=eligibility)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(category__icontains=search)
                | Q(description__icontains=search)
                | Q(eligibility__icontains=search)
            )
        return queryset


class ScholarshipViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Database-backed scholarships endpoint.
    Supports:
    - search: name/eligibility/amount
    - eligibility: partial match
    """

    serializer_class = ScholarshipSerializer
    permission_classes = [AllowAny]
    queryset = Scholarship.objects.all()
    search_fields = ["name", "eligibility", "amount"]
    ordering_fields = ["deadline", "name"]
    ordering = ["deadline", "name"]

    def get_queryset(self):
        queryset = super().get_queryset()
        eligibility = (self.request.query_params.get("eligibility") or "").strip()
        search = (self.request.query_params.get("search") or "").strip()

        if eligibility:
            queryset = queryset.filter(eligibility__icontains=eligibility)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search)
                | Q(eligibility__icontains=search)
                | Q(amount__icontains=search)
            )
        return queryset


@api_view(['POST'])
def ai_chat(request):
    """Chat endpoint for AI-powered government career assistance."""
    message = request.data.get("message", "").strip()

    if not message:
        return Response(
            {"error": "Message cannot be empty."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    prompt = f"""You are an AI-powered Indian government career assistant.

Help users with:
- Government jobs and employment opportunities
- Government schemes and welfare programs
- Scholarships and educational funding
- Resume guidance and career advice

Provide helpful, accurate information based on Indian government resources.

User Question:
{message}"""

    try:
        service = GeminiJsonService()
        reply = service.generate_json(prompt)
        return Response({"reply": reply})
    except GeminiServiceError as e:
        logger.error("Gemini service error: %s", str(e))
        return Response(
            {"error": "AI service is currently unavailable."},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    except Exception as e:
        logger.exception("Unexpected error in ai_chat: %s", str(e))
        return Response(
            {"error": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
