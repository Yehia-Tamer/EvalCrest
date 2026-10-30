import pytest
from pydantic import BaseModel, ValidationError

from evalcrest.graph.state import CaseInput, Citation, TargetResponse


@pytest.mark.parametrize(
    ("model", "kwargs"),
    [
        (CaseInput, {"question": "What is F?", "as_usr": "eval-user-a"}),
        (Citation, {"source_id": "physics_notes.pdf:p2", "pgae": 2}),
        (TargetResponse, {"status": "ok", "answer": "a", "latency_ms": 0, "http_stauts": 201}),
    ],
    ids=["CaseInput", "Citation", "TargetResponse"],
)
def test_misspelled_field_is_rejected(model: type[BaseModel], kwargs: dict[str, object]) -> None:
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        model(**kwargs)


def test_valid_studybuddy_response_is_accepted() -> None:
    response = TargetResponse(
        status="ok",
        http_status=201,
        answer="Newton's Second Law is F=ma",
        citations=[
            Citation(source_id="physics_notes.pdf:p2", page=2),
            Citation(source_id="physics_notes.pdf:p5", page=5),
        ],
        latency_ms=18300,
    )

    assert response.attempts == 1
    assert len(response.citations) == 2


@pytest.mark.parametrize(
    ("status", "http_status", "error"),
    [
        ("http_error", 400, "HTTP 400: bad request"),
        ("timeout", None, "timed out after 30s"),
        ("transport_error", None, "connection refused"),
    ],
)
def test_valid_failure_response_is_accepted(
    status: str, http_status: int | None, error: str
) -> None:
    response = TargetResponse(status=status, http_status=http_status, latency_ms=0, error=error)

    assert response.answer is None
    assert response.citations == []
    assert response.error == error


def test_ok_status_with_empty_answer_is_accepted() -> None:
    response = TargetResponse(status="ok", http_status=201, answer="", latency_ms=0)

    assert response.answer == ""


def test_unknown_status_is_rejected() -> None:
    with pytest.raises(ValidationError):
        TargetResponse(status="maybe", latency_ms=0, error="x")


def test_ok_status_requires_answer() -> None:
    with pytest.raises(ValidationError, match="answer is required"):
        TargetResponse(status="ok", latency_ms=0)


def test_failed_status_requires_error() -> None:
    with pytest.raises(ValidationError, match="error is required"):
        TargetResponse(status="http_error", answer="xyz", latency_ms=0)


def test_negative_latency_is_rejected() -> None:
    with pytest.raises(ValidationError, match="greater than or equal to 0"):
        TargetResponse(status="ok", answer="xyz", latency_ms=-1)


@pytest.mark.parametrize("attempts", [0, -2])
def test_attempt_below_1_is_rejected(attempts: int) -> None:
    with pytest.raises(ValidationError, match="greater than or equal to 1"):
        TargetResponse(status="ok", answer="abc", latency_ms=0, attempts=attempts)


def test_citations_are_not_shared() -> None:
    first = TargetResponse(status="ok", answer="a", latency_ms=0)
    second = TargetResponse(status="ok", answer="b", latency_ms=0)

    first.citations.append(Citation(source_id="physics_notes.pdf:p2", page=2))

    assert len(first.citations) == 1
    assert second.citations == []


@pytest.mark.parametrize("page", [0, -3])
def test_invalid_page_numbers_are_rejected(page: int) -> None:
    with pytest.raises(ValidationError, match="greater than or equal to 1"):
        Citation(source_id=f"physics_notes.pdf:p{page}", page=page)


@pytest.mark.parametrize("question", ["", " "])
def test_blank_question_is_rejected(question: str) -> None:
    with pytest.raises(ValidationError, match="question must not be empty"):
        CaseInput(question=question)


def test_question_whitespace_is_preserved() -> None:
    assert CaseInput(question="  What is F?  ").question == "  What is F?  "


def test_citation_without_page_is_accepted() -> None:
    assert Citation(source_id="Youtube Video @ehjbwejb21").page is None
