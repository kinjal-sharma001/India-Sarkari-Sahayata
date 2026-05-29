from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

import requests
from django.conf import settings


@dataclass(frozen=True)
class ExternalJob:
    external_id: str
    title: str
    company: str
    location: str
    url: str
    source: str
    published_at: datetime | None


ADZUNA_API_URL = "https://api.adzuna.com/v1/api/jobs/in/search/1"


def fetch_jobs_from_adzuna(*, query: str | None, limit: int = 20) -> list[ExternalJob]:
    app_id = settings.ADZUNA_APP_ID
    app_key = settings.ADZUNA_APP_KEY
    if not app_id or not app_key:
        raise RuntimeError("Adzuna API credentials are not configured.")

    params: dict[str, Any] = {
        "app_id": app_id,
        "app_key": app_key,
    }
    if query:
        params["what"] = query

    resp = requests.get(ADZUNA_API_URL, params=params, timeout=20)
    resp.raise_for_status()
    payload = resp.json()

    jobs: list[ExternalJob] = []
    for raw in (payload.get("results") or [])[: max(1, min(limit, 50))]:
        published_at = None
        raw_date = raw.get("created")
        if isinstance(raw_date, str):
            try:
                published_at = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
            except ValueError:
                published_at = None

        company = raw.get("company") or {}
        location = raw.get("location") or {}
        jobs.append(
            ExternalJob(
                external_id=str(raw.get("id") or raw.get("__CLASS__") or ""),
                title=str(raw.get("title") or "").strip(),
                company=str(company.get("display_name") or "").strip(),
                location=str(location.get("display_name") or "").strip(),
                url=str(raw.get("redirect_url") or raw.get("adref") or "").strip(),
                source="adzuna",
                published_at=published_at,
            )
        )

    return jobs

