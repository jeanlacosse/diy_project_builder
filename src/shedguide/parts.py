"""Parts engine: FramingPlan to PartsList."""

from shedguide.config import STOCK_CSV
from shedguide.spec import FramingPlan, PartsItem, PartsList
from shedguide.tables import read_csv_rows


class StockError(Exception):
    """No stock length covers the cut."""


def build_parts(plan: FramingPlan) -> PartsList:
    # PLACEHOLDER (assumption A1): cut length equals the span; replaced in 07a/07b.
    cut = plan.span_ft
    lengths = sorted(
        float(r["stock_length_ft"])
        for r in read_csv_rows(STOCK_CSV)
        if r["stock_size"] == plan.joist_size
    )
    stock = next((s for s in lengths if s >= cut), None)
    if stock is None:
        raise StockError(f"No {plan.joist_size} stock length covers a {cut} ft cut.")
    item = PartsItem(
        item="Floor joist",
        stock_size=plan.joist_size,
        stock_length_ft=stock,
        quantity=plan.joist_count,
        cut_length_ft=cut,
    )
    return PartsList(items=[item])
