"""Framing planner: table lookup only, never the LLM."""

import math

from shedguide.spec import FramingPlan, ShedSpec
from shedguide.tables import OutOfRangeError, lookup_joist


def plan_framing(spec: ShedSpec) -> FramingPlan:
    # PLACEHOLDER (assumption A1): joists run across the width; replaced in slices 07a/07b.
    if spec.width_ft is None or spec.length_ft is None:
        raise OutOfRangeError("Width and length are both needed to plan the floor.")
    row = lookup_joist(spec.width_ft)
    # PLACEHOLDER formula, not a framing rule.
    count = math.ceil(spec.length_ft * 12 / row.spacing_in) + 1
    return FramingPlan(
        joist_size=row.joist_size,
        spacing_in=row.spacing_in,
        joist_count=count,
        span_ft=spec.width_ft,
        length_ft=spec.length_ft,
        table_row_id=row.row_id,
    )
