"""Tests for WebhookPayload (arm-neu -> transcoder POST /webhook/arm)."""
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from arm_contracts import (
    TranscodeJobConfig,
    WebhookPayload,
    WebhookTrackMeta,
)


_FIXTURE = Path(__file__).parent / "fixtures" / "webhook_payload.json"


def _load_fixture() -> dict:
    return json.loads(_FIXTURE.read_text())


def test_real_world_payload_round_trips():
    src = _load_fixture()
    p = WebhookPayload.model_validate(src)
    assert p.job_id == 169
    assert p.title == "ARM rip complete"
    assert p.disctype == "dvd"
    assert p.tracks is not None and len(p.tracks) == 2
    assert isinstance(p.config_overrides, TranscodeJobConfig)
    assert p.config_overrides.preset_slug == "software-balanced"
    # Round-trip: fixture is the canonical wire shape; dump should match
    # at least on every key the fixture sets.
    dumped = p.model_dump(exclude_none=True, mode="json")
    for key, value in src.items():
        if key == "config_overrides":
            # Pydantic re-serializes nested models; just spot-check preset_slug.
            assert dumped[key]["preset_slug"] == value["preset_slug"]
        elif key == "job_id":
            # Wire form is string; model is int; round-trip dumps as int.
            assert dumped[key] == int(value)
        else:
            assert dumped[key] == value


def test_minimal_payload():
    p = WebhookPayload(title="Done", job_id=42)
    assert p.title == "Done"
    assert p.job_id == 42
    assert p.body is None and p.message is None
    assert p.tracks is None
    assert p.effective_body is None


def test_job_id_accepts_string_or_int():
    """arm-neu sends str(job.job_id); transcoder uses int paths."""
    assert WebhookPayload(title="x", job_id="123").job_id == 123
    assert WebhookPayload(title="x", job_id=123).job_id == 123


def test_job_id_rejects_non_numeric():
    with pytest.raises(ValidationError, match="job_id must be a valid integer"):
        WebhookPayload(title="x", job_id="not-a-number")


def test_title_rejects_blank():
    with pytest.raises(ValidationError, match="Title cannot be empty"):
        WebhookPayload(title="   ", job_id=1)


def test_title_strips_control_characters():
    p = WebhookPayload(title="Hello\x07World\x00", job_id=1)
    assert p.title == "HelloWorld"


def test_body_keeps_newlines_and_tabs():
    p = WebhookPayload(title="x", job_id=1, body="line1\nline2\tend\x07")
    assert p.body == "line1\nline2\tend"


def test_path_strips_nulls_and_controls():
    p = WebhookPayload(title="x", job_id=1, path="ok/path\x00\x07")
    assert p.path == "ok/path"


def test_body_message_path_explicit_none_round_trip():
    """Explicit None in the input survives as None (validator early-exit branch)."""
    p = WebhookPayload.model_validate(
        {"title": "x", "job_id": 1, "body": None, "message": None, "path": None}
    )
    assert p.body is None
    assert p.message is None
    assert p.path is None


def test_effective_body_prefers_body_over_message():
    p = WebhookPayload(title="x", job_id=1, body="from-body", message="from-message")
    assert p.effective_body == "from-body"


def test_effective_body_falls_back_to_message():
    """Apprise json:// posts use 'message', not 'body'."""
    p = WebhookPayload(title="x", job_id=1, message="from-apprise")
    assert p.effective_body == "from-apprise"


def test_unknown_top_level_field_ignored():
    """Producer may add fields ahead of consumer upgrades; extras are dropped."""
    p = WebhookPayload.model_validate(
        {"title": "x", "job_id": 1, "unknown_field": "ignored"}
    )
    assert "unknown_field" not in p.model_dump()


def test_tracks_validate_as_typed_models():
    """Inner track dicts are coerced to WebhookTrackMeta, not dropped."""
    src = {
        "title": "x",
        "job_id": 1,
        "tracks": [{"track_number": "0", "filename": "t00.mkv"}],
    }
    p = WebhookPayload.model_validate(src)
    assert isinstance(p.tracks[0], WebhookTrackMeta)
    assert p.tracks[0].track_number == "0"
    assert p.tracks[0].filename == "t00.mkv"
    # Defaults fill the rest as empty strings.
    assert p.tracks[0].episode_name == ""


def test_config_overrides_invalid_preset_slug_rejected():
    """preset_slug pattern is enforced through the nested TranscodeJobConfig."""
    bad = {
        "title": "x",
        "job_id": 1,
        "config_overrides": {"preset_slug": "Has Capitals"},
    }
    with pytest.raises(ValidationError):
        WebhookPayload.model_validate(bad)


def test_title_length_cap_enforced():
    long_title = "x" * 600
    with pytest.raises(ValidationError):
        WebhookPayload(title=long_title, job_id=1)


def test_webhook_type_accepts_enum_member():
    from arm_contracts import WebhookPayload
    from arm_contracts.enums import WebhookEventType
    p = WebhookPayload(title="t", body="b", job_id=1, type=WebhookEventType.info)
    assert p.type is WebhookEventType.info


def test_webhook_type_accepts_valid_string():
    from arm_contracts import WebhookPayload
    from arm_contracts.enums import WebhookEventType
    p = WebhookPayload(title="t", body="b", job_id=1, type="info")
    assert p.type is WebhookEventType.info


def test_webhook_type_rejects_invalid_string():
    import pytest
    from pydantic import ValidationError
    from arm_contracts import WebhookPayload
    with pytest.raises(ValidationError):
        WebhookPayload(title="t", body="b", job_id=1, type="bogus")


def test_webhook_type_allows_none():
    from arm_contracts import WebhookPayload
    p = WebhookPayload(title="t", body="b", job_id=1, type=None)
    assert p.type is None
