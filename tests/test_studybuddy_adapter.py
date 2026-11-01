import json
from collections.abc import Iterator
from typing import Any

import httpx
import pytest
import respx

from evalcrest.config import Settings
from evalcrest.graph.state import CaseInput, Citation
from evalcrest.targets.studybuddy import StudyBuddyAdapter, StudyBuddyAuthError, map_sources

BASE = "http://test"

NEWTON_REPLY = {
    "id": 9,
    "role": "assistant",
    "content": "Newton's Second Law states that F = ma.",
    "timestamp": "2026-10-26T08:09:15.769638",
    "sources": [
        {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 2},
        {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 5},
        {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 1},
        {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 4},
        {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 3},
    ],
}


@pytest.fixture
def settings() -> Settings:
    """Return a valid Settings object."""
    return Settings(
        _env_file=None,
        studybuddy_url=BASE,
        studybuddy_username="test-user",
        studybuddy_password="not-a-real-password",
        studybuddy_document_id=4,
    )


@respx.mock
async def test_health_is_true_when_root_returns_200(settings: Settings) -> None:
    respx.get(f"{BASE}/").mock(return_value=httpx.Response(200))

    async with StudyBuddyAdapter(settings) as adapter:
        assert await adapter.health() is True


@respx.mock
async def test_health_is_false_when_root_returns_500(settings: Settings) -> None:
    respx.get(f"{BASE}/").mock(return_value=httpx.Response(500))

    async with StudyBuddyAdapter(settings) as adapter:
        assert await adapter.health() is False


@respx.mock
async def test_health_is_false_when_connection_refused(settings: Settings) -> None:
    respx.get(f"{BASE}/").mock(side_effect=httpx.ConnectError("connection refused"))

    async with StudyBuddyAdapter(settings) as adapter:
        assert await adapter.health() is False


@respx.mock
async def test_login_stores_token(settings: Settings) -> None:
    respx.post(f"{BASE}/auth/login").mock(
        return_value=httpx.Response(201, json={"access_token": "abc123"})
    )

    async with StudyBuddyAdapter(settings) as adapter:
        await adapter.login()
        assert adapter._token == "abc123"


@respx.mock
async def test_login_sends_form_data(settings: Settings) -> None:
    route = respx.post(f"{BASE}/auth/login").mock(
        return_value=httpx.Response(201, json={"access_token": "abc123"})
    )

    async with StudyBuddyAdapter(settings) as adapter:
        await adapter.login()

    request = route.calls.last.request
    assert request.headers["content-type"].startswith("application/x-www-form-urlencoded")
    assert b"username=test-user" in request.content


@respx.mock
async def test_login_rejected_raises_without_leaking_password(settings: Settings) -> None:
    respx.post(f"{BASE}/auth/login").mock(
        return_value=httpx.Response(401, json={"detail": "Incorrect username or password"})
    )

    async with StudyBuddyAdapter(settings) as adapter:
        with pytest.raises(
            StudyBuddyAuthError, match="login rejected for user 'test-user'"
        ) as exc_info:
            await adapter.login()
    assert "not-a-real-password" not in str(exc_info.value)


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        (
            {"source_type": "pdf", "filename": "physics_notes.pdf", "page": 2, "link": None},
            Citation(source_id="physics_notes.pdf:p2", page=2),
        ),
        (
            {"source_type": "pptx", "slide": 3, "filename": None, "page": None},
            Citation(source_id="slide3"),
        ),
        (
            {"source_type": "web", "link": "https://example.com/newton", "source_url": None},
            Citation(source_id="https://example.com/newton"),
        ),
        (
            {"source_type": "youtube", "link": None, "source_url": None},
            Citation(source_id="youtube:unknown"),
        ),
    ],
    ids=["pdf", "pptx", "web", "unknown-type-kept"],
)
def test_map_sources(source: dict[str, Any], expected: Citation) -> None:
    assert map_sources([source]) == [expected]


def test_map_sources_empty_list() -> None:
    assert map_sources([]) == []


@pytest.fixture
def studybuddy() -> Iterator[respx.MockRouter]:
    """A fake studybuddy that responds to requests"""

    with respx.mock(base_url=BASE) as mock:
        mock.post("/auth/login", name="login").mock(
            return_value=httpx.Response(
                201, json={"access_token": "abc123", "token_type": "bearer"}
            )
        )

        mock.post("/conversations/", name="conversation").mock(
            return_value=httpx.Response(201, json={"id": 17, "document_id": 4})
        )

        mock.post("/conversations/17/messages", name="message").mock(
            return_value=httpx.Response(201, json=NEWTON_REPLY)
        )

        yield mock


async def test_ask_returns_ok_with_answer_and_citations(
    settings: Settings, studybuddy: respx.MockRouter
) -> None:
    async with StudyBuddyAdapter(settings) as adapter:
        response = await adapter.ask(CaseInput(question="What is Newton's second law?"))

    assert response.status == "ok"
    assert response.http_status == 201
    assert response.answer == NEWTON_REPLY["content"]
    assert len(response.citations) == 5
    assert response.citations[0].source_id == "physics_notes.pdf:p2"
    assert response.latency_ms >= 0


async def test_ask_logs_in_only_once(settings: Settings, studybuddy: respx.MockRouter) -> None:
    async with StudyBuddyAdapter(settings) as adapter:
        await adapter.ask(CaseInput(question="What is Newton's second law?"))
        await adapter.ask(CaseInput(question="What is F=ma?"))

    assert studybuddy["login"].call_count == 1


async def test_ask_sends_token_and_document_id(
    settings: Settings, studybuddy: respx.MockRouter
) -> None:
    async with StudyBuddyAdapter(settings) as adapter:
        await adapter.ask(CaseInput(question="What is Newton's second law?"))

    conversation_request = studybuddy["conversation"].calls.last.request
    assert conversation_request.headers["Authorization"] == "Bearer abc123"
    assert json.loads(conversation_request.content) == {"document_id": 4}


async def test_ask_sends_question_unchanged(
    settings: Settings, studybuddy: respx.MockRouter
) -> None:
    question = "  what is F=ma?  "
    async with StudyBuddyAdapter(settings) as adapter:
        await adapter.ask(CaseInput(question=question))

    message_request = studybuddy["message"].calls.last.request
    assert json.loads(message_request.content) == {"content": question}
