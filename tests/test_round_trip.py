"""Fixture-backed round-trip tests.

Each fixture represents a payload shape we've actually seen on the wire.
If the models grow, this is where we confirm legacy payloads still parse.
"""
import json
from pathlib import Path

import pytest

FIXTURES = Path(__file__).parent / "fixtures"


def test_legacy_webhook_parses():
    """A real webhook payload captured from the deployed transcoder must
    still deserialize into TranscodeJobConfig without ValidationError."""
    from arm_contracts import TranscodeJobConfig
    raw = json.loads((FIXTURES / "legacy_webhook.json").read_text())
    m = TranscodeJobConfig.model_validate(raw)
    assert m.preset_slug == "software-balanced"
    assert m.overrides.tiers.uhd.video_quality == 24


def test_legacy_webhook_round_trip():
    from arm_contracts import TranscodeJobConfig
    raw = json.loads((FIXTURES / "legacy_webhook.json").read_text())
    m = TranscodeJobConfig.model_validate(raw)
    dumped = json.loads(m.model_dump_json())
    reparsed = TranscodeJobConfig.model_validate(dumped)
    assert reparsed == m


def test_job_started_event_round_trip():
    from pydantic import TypeAdapter
    from arm_contracts import NotificationEvent
    from arm_contracts.notification_event import JobStartedEvent
    adapter = TypeAdapter(NotificationEvent)
    raw = json.loads((FIXTURES / "job_started_event.json").read_text())
    parsed = adapter.validate_python(raw)
    assert isinstance(parsed, JobStartedEvent)
    # Round-trip: dump and re-validate.
    again = adapter.validate_python(json.loads(parsed.model_dump_json()))
    assert again == parsed


def test_job_rip_complete_event_round_trip():
    from pydantic import TypeAdapter
    from arm_contracts import NotificationEvent
    from arm_contracts.notification_event import JobRipCompleteEvent
    adapter = TypeAdapter(NotificationEvent)
    raw = json.loads((FIXTURES / "job_rip_complete_event.json").read_text())
    parsed = adapter.validate_python(raw)
    assert isinstance(parsed, JobRipCompleteEvent)
    again = adapter.validate_python(json.loads(parsed.model_dump_json()))
    assert again == parsed


def test_job_transcode_complete_event_round_trip():
    from pydantic import TypeAdapter
    from arm_contracts import NotificationEvent
    from arm_contracts.notification_event import JobTranscodeCompleteEvent
    adapter = TypeAdapter(NotificationEvent)
    raw = json.loads((FIXTURES / "job_transcode_complete_event.json").read_text())
    parsed = adapter.validate_python(raw)
    assert isinstance(parsed, JobTranscodeCompleteEvent)
    again = adapter.validate_python(json.loads(parsed.model_dump_json()))
    assert again == parsed


def test_job_failed_event_round_trip():
    from pydantic import TypeAdapter
    from arm_contracts import NotificationEvent
    from arm_contracts.notification_event import JobFailedEvent
    adapter = TypeAdapter(NotificationEvent)
    raw = json.loads((FIXTURES / "job_failed_event.json").read_text())
    parsed = adapter.validate_python(raw)
    assert isinstance(parsed, JobFailedEvent)
    again = adapter.validate_python(json.loads(parsed.model_dump_json()))
    assert again == parsed
