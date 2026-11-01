import time
from typing import Any

import httpx

from evalcrest.config import Settings
from evalcrest.graph.state import CaseInput, Citation, TargetResponse


class StudyBuddyAuthError(Exception):
    """Login failed or was rejected. The configuration is wrong; stop the run"""

    pass


class StudyBuddyAdapter:
    """Talks to StudyBuddy API and returns normalized TargetResponse objects."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = httpx.AsyncClient(
            base_url=settings.studybuddy_url,
            timeout=settings.studybuddy_timeout_s,
        )
        self._token: str | None = None

    async def __aenter__(self) -> "StudyBuddyAdapter":
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        await self._client.aclose()

    async def health(self) -> bool:
        try:
            response = await self._client.get("/", timeout=5)
        except httpx.HTTPError:
            return False
        return response.status_code == 200

    async def login(self) -> None:
        response = await self._client.post(
            "/auth/login",
            data={
                "username": self._settings.studybuddy_username,
                "password": self._settings.studybuddy_password.get_secret_value(),
            },
        )

        username = self._settings.studybuddy_username

        if response.status_code in (401, 403):
            raise StudyBuddyAuthError(
                f"login rejected for user '{username}' (HTTP {response.status_code})"
            )

        response.raise_for_status()
        self._token = response.json()["access_token"]

    async def ask(self, case_input: CaseInput) -> TargetResponse:
        if self._token is None:
            await self.login()

        headers = {"Authorization": f"Bearer {self._token}"}

        response = await self._client.post(
            "/conversations/",
            json={"document_id": self._settings.studybuddy_document_id},
            headers=headers,
        )

        conversation_id = response.json()["id"]

        start_time = time.perf_counter()
        response = await self._client.post(
            f"/conversations/{conversation_id}/messages",
            json={"content": case_input.question},
            headers=headers,
        )
        latency_ms = int((time.perf_counter() - start_time) * 1000)

        body = response.json()

        return TargetResponse(
            status="ok",
            http_status=response.status_code,
            answer=body["content"],
            citations=map_sources(body.get("sources", [])),
            latency_ms=latency_ms,
        )


def map_sources(sources: list[dict[str, Any]]) -> list[Citation]:
    citations: list[Citation] = []
    for source in sources:
        source_type = source.get("source_type")
        if source_type == "pdf":
            page = source.get("page")
            citations.append(Citation(source_id=f"{source.get('filename')}:p{page}", page=page))
        elif source_type == "pptx":
            citations.append(Citation(source_id=f"slide{source.get('slide')}"))
        else:
            source_id = source.get("link") or source.get("source_url") or f"{source_type}:unknown"
            citations.append(Citation(source_id=source_id))
    return citations
