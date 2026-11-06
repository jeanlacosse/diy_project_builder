import pytest

from shedguide.framing import plan_framing
from shedguide.spec import FramingPlan, ShedSpec
from shedguide.tables import OutOfRangeError

CANNED = ShedSpec(project_type="shed", width_ft=10.0, length_ft=12.0)


def test_T11_canned_spec_gives_expected_plan() -> None:
    assert plan_framing(CANNED) == FramingPlan(
        joist_size="2x8",
        spacing_in=16,
        joist_count=10,
        span_ft=10.0,
        length_ft=12.0,
        table_row_id="STUB-1",
    )


def test_T12_missing_or_too_wide_raises() -> None:
    with pytest.raises(OutOfRangeError):
        plan_framing(ShedSpec(length_ft=12.0))
    with pytest.raises(OutOfRangeError):
        plan_framing(ShedSpec(width_ft=20.0, length_ft=12.0))
