import pytest

from shedguide.framing import plan_framing
from shedguide.parts import StockError, build_parts
from shedguide.spec import FramingPlan, ShedSpec


def test_T13_plan_gives_expected_parts() -> None:
    plan = plan_framing(ShedSpec(width_ft=9.0, length_ft=12.0))
    (item,) = build_parts(plan).items
    assert (item.stock_size, item.stock_length_ft, item.quantity) == ("2x8", 10.0, 10)
    assert item.cut_length_ft == 9.0


def test_T14_too_long_raises_and_exact_fit_uses_that_length() -> None:
    base = {"joist_size": "2x8", "spacing_in": 16, "joist_count": 3, "length_ft": 4.0}
    with pytest.raises(StockError):
        build_parts(FramingPlan(span_ft=17.0, table_row_id="X", **base))  # type: ignore[arg-type]
    (item,) = build_parts(FramingPlan(span_ft=12.0, table_row_id="X", **base)).items  # type: ignore[arg-type]
    assert item.stock_length_ft == item.cut_length_ft == 12.0
