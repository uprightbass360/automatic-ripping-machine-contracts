"""Tests for OutboundWebhookPayload — the v18 rich-payload wire shape
sent by arm-neu's notification dispatcher to webhook channels."""
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError


def _event_payload_dict():
    return {
        "event_key": "job.failed",
        "event_id": str(uuid4()),
        "occurred_at": datetime.now(timezone.utc).isoformat(),
        "job_id": 169,
        "job_title": "Mysterysuspense",
        "job_disc_type": "dvd",
        "job_imdb_id": None,
        "phase": "rip",
        "error_message": "makemkvcon failed",
        "error_code": "MAKEMKV_FAILED",
    }


def test_channel_ref_minimal():
    from arm_contracts.outbound_webhook_payload import ChannelRef
    r = ChannelRef(id=1, name="HA", type="webhook")
    assert r.id == 1


def test_outbound_webhook_payload_basic():
    from arm_contracts.outbound_webhook_payload import (
        OutboundWebhookPayload,
        ChannelRef,
    )
    p = OutboundWebhookPayload(
        event=_event_payload_dict(),
        title="Job failed",
        body="Job 169 failed during rip",
        channel=ChannelRef(id=1, name="HA", type="webhook"),
        arm_instance_name="hifi",
        sent_at=datetime.now(timezone.utc),
    )
    assert p.schema_version == 1
    assert p.event.event_key == "job.failed"
    assert p.title == "Job failed"
    assert p.channel.name == "HA"


def test_outbound_webhook_payload_schema_version_locked():
    """schema_version must be the literal 1; anything else is a wire
    incompatibility and must fail validation."""
    from arm_contracts.outbound_webhook_payload import (
        OutboundWebhookPayload,
        ChannelRef,
    )
    with pytest.raises(ValidationError):
        OutboundWebhookPayload(
            schema_version=2,  # type: ignore[arg-type]
            event=_event_payload_dict(),
            title="X",
            body="Y",
            channel=ChannelRef(id=1, name="HA", type="webhook"),
            arm_instance_name=None,
            sent_at=datetime.now(timezone.utc),
        )


def test_outbound_webhook_payload_arm_instance_name_optional():
    from arm_contracts.outbound_webhook_payload import (
        OutboundWebhookPayload,
        ChannelRef,
    )
    p = OutboundWebhookPayload(
        event=_event_payload_dict(),
        title="X",
        body="Y",
        channel=ChannelRef(id=1, name="HA", type="webhook"),
        arm_instance_name=None,
        sent_at=datetime.now(timezone.utc),
    )
    assert p.arm_instance_name is None


def test_outbound_webhook_payload_public_re_exports():
    from arm_contracts import OutboundWebhookPayload, ChannelRef
    assert OutboundWebhookPayload is not None
    assert ChannelRef is not None
