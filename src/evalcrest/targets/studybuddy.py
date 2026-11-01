import httpx

from evalcrest.config import Settings


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
