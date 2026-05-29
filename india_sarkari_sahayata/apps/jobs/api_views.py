import logging

import requests
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .external import fetch_jobs_from_adzuna
from .serializers import ExternalJobSerializer


class JobSearchAPIView(APIView):
    """
    Real external API integration (Adzuna).

    Query params:
    - q: search query
    - limit: 1..50
    """

    authentication_classes: list = []
    permission_classes: list = []
    logger = logging.getLogger(__name__)

    def get(self, request):
        q = (request.query_params.get("q") or "").strip() or None
        try:
            limit = int(request.query_params.get("limit") or 20)
        except ValueError:
            return Response(
                {"detail": "limit must be an integer"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        limit = max(1, min(limit, 50))

        cache_key = f"jobs:adzuna:{(q or '').lower()}:{limit}"
        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return Response(cached_response)

        try:
            jobs = fetch_jobs_from_adzuna(query=q, limit=limit)
        except RuntimeError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except requests.RequestException:
            self.logger.exception("Adzuna request failed for query='%s', limit=%s", q, limit)
            return Response(
                {"detail": "Unable to fetch jobs from upstream provider right now."},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        data = [
            {
                "external_id": j.external_id,
                "title": j.title,
                "company": j.company,
                "location": j.location,
                "url": j.url,
                "source": j.source,
                "published_at": j.published_at,
            }
            for j in jobs
        ]

        payload = {
            "query": q or "",
            "count": len(data),
            "results": ExternalJobSerializer(data, many=True).data,
        }
        cache.set(cache_key, payload, timeout=120)
        return Response(payload)

