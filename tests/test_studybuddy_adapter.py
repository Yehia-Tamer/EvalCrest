import httpx
import pytest
import respx

from evalcrest.config import Settings
from evalcrest.targets.studybuddy import StudyBuddyAdapter

BASE = "http://test"


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
