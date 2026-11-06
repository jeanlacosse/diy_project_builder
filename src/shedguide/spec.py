"""Pydantic contract between the LLM and deterministic code."""

from pydantic import BaseModel, ConfigDict, Field


class ShedSpec(BaseModel):
    """Placeholder fields only; slice 04 replaces them with the real envelope.

    Every field is Optional with default None, so a missing value is never a guess.
    """

    model_config = ConfigDict(extra="forbid")

    project_type: str | None = None
    width_ft: float | None = Field(default=None, gt=0)
    length_ft: float | None = Field(default=None, gt=0)


class FramingPlan(BaseModel):
    """Joist size, spacing and count, plus the table row they came from."""

    joist_size: str
    spacing_in: float
    joist_count: int
    span_ft: float
    length_ft: float
    table_row_id: str


class PartsItem(BaseModel):
    item: str
    stock_size: str
    stock_length_ft: float
    quantity: int
    cut_length_ft: float


class PartsList(BaseModel):
    items: list[PartsItem]
