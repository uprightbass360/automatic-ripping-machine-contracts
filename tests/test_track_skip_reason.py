"""Track contract: process and skip_reason fields."""

import pytest
from pydantic import ValidationError

from arm_contracts import Track


def test_track_default_process_true():
    t = Track(track_id=1, job_id=1)
    assert t.process is True
    assert t.skip_reason is None


def test_track_skip_reason_too_short():
    t = Track(track_id=1, job_id=1, process=False, skip_reason="too_short")
    assert t.process is False
    assert t.skip_reason == "too_short"


def test_track_skip_reason_makemkv_skipped():
    t = Track(track_id=1, job_id=1, process=False, skip_reason="makemkv_skipped")
    assert t.skip_reason == "makemkv_skipped"


def test_track_invalid_skip_reason_rejected():
    with pytest.raises(ValidationError):
        Track(track_id=1, job_id=1, skip_reason="bogus_reason")
