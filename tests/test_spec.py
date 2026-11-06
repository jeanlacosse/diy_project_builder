import pytest
from pydantic import ValidationError

from shedguide.spec import ShedSpec


def test_T2_empty_shedspec_has_every_field_none() -> None:
    spec = ShedSpec()
    assert all(v is None for v in spec.model_dump().values())


def test_T3_shedspec_rejects_wrong_type_and_negative_width() -> None:
    with pytest.raises(ValidationError):
        ShedSpec(width_ft="abc")  # type: ignore[arg-type]
    with pytest.raises(ValidationError):
        ShedSpec(width_ft=-4)
