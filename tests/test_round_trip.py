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
