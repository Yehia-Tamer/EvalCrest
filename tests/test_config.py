import pytest
from pydantic import ValidationError

from evalcrest.config import Settings


@pytest.fixture
def studybuddy_env(monkeypatch: pytest.MonkeyPatch) -> pytest.MonkeyPatch:
    """Set a valid StudyBuddy configuration for one test."""
    monkeypatch.setenv("STUDYBUDDY_URL", "http://test:8000")
    monkeypatch.setenv("STUDYBUDDY_USERNAME", "eval-user-a")
    monkeypatch.setenv("STUDYBUDDY_PASSWORD", "s3cret-pass")
    monkeypatch.setenv("STUDYBUDDY_DOCUMENT_ID", "4")
    return monkeypatch


def test_settings_are_read_from_environment(studybuddy_env: pytest.MonkeyPatch) -> None:
    settings = Settings(_env_file=None)

    assert settings.studybuddy_url == "http://test:8000"
    assert settings.studybuddy_document_id == 4
    assert settings.studybuddy_username == "eval-user-a"
    assert isinstance(settings.studybuddy_document_id, int)
    assert settings.studybuddy_timeout_s == 60.0


def test_url_defaults_to_localhost(studybuddy_env: pytest.MonkeyPatch) -> None:
    studybuddy_env.delenv("STUDYBUDDY_URL")

    settings = Settings(_env_file=None)

    assert settings.studybuddy_url == "http://127.0.0.1:8000"


def test_missing_document_id_is_rejected(studybuddy_env: pytest.MonkeyPatch) -> None:
    studybuddy_env.delenv("STUDYBUDDY_DOCUMENT_ID")

    with pytest.raises(ValidationError, match="Field required"):
        Settings(_env_file=None)


def test_non_numeric_document_id_is_rejected(studybuddy_env: pytest.MonkeyPatch) -> None:
    studybuddy_env.setenv("STUDYBUDDY_DOCUMENT_ID", "abc")

    with pytest.raises(ValidationError, match="valid integer"):
        Settings(_env_file=None)


def test_password_is_hidden(studybuddy_env: pytest.MonkeyPatch) -> None:
    settings = Settings(_env_file=None)

    assert "s3cret-pass" not in str(settings.studybuddy_password)
    assert "s3cret-pass" not in repr(settings)
    assert settings.studybuddy_password.get_secret_value() == "s3cret-pass"


def test_document_id_below_one_is_rejected(studybuddy_env: pytest.MonkeyPatch) -> None:
    studybuddy_env.setenv("STUDYBUDDY_DOCUMENT_ID", "0")

    with pytest.raises(ValidationError, match="greater than or equal to 1"):
        Settings(_env_file=None)


def test_non_positive_timeout_is_rejected(studybuddy_env: pytest.MonkeyPatch) -> None:
    studybuddy_env.setenv("STUDYBUDDY_TIMEOUT_S", "0")

    with pytest.raises(ValidationError, match="greater than 0"):
        Settings(_env_file=None)
