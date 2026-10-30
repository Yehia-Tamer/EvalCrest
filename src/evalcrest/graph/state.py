from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class CaseInput(BaseModel):
    """What gets sent to the target for one test case."""

    model_config = ConfigDict(extra="forbid")

    question: str
    as_user: str | None = None

    @field_validator("question")
    @classmethod
    def question_not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("question must not be empty nor a whitespace.")
        return value


class Citation(BaseModel):
    """One source the target says it used."""

    model_config = ConfigDict(extra="forbid")

    source_id: str
    title: str | None = None
    page: int | None = Field(default=None, ge=1)


class TargetResponse(BaseModel):
    """The normalized target’s reply to one case"""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok", "timeout", "http_error", "transport_error"]
    http_status: int | None = None
    answer: str | None = None
    citations: list[Citation] = Field(default_factory=list)
    latency_ms: int = Field(ge=0)
    attempts: int = Field(default=1, ge=1)
    error: str | None = None

    @model_validator(mode="after")
    def verify_status_fields(self) -> Self:
        if self.status == "ok" and self.answer is None:
            raise ValueError("answer is required when status is 'ok'")
        if self.status != "ok" and self.error is None:
            raise ValueError("error is required when status is not 'ok'")
        return self
