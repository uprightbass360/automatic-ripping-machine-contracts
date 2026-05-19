"""Tests for NotificationEvent (the discriminated event union published
by arm-neu's notification module to its outbox)."""
from datetime import datetime, timezone
from uuid import uuid4

import pytest
from pydantic import ValidationError


def test_job_event_base_is_abstract_in_spirit():
    """JobEventBase carries the fields all events share. It's not a
    discriminator target on its own; the four concrete subclasses are."""
    from arm_contracts.notification_event import JobEventBase
    # Construct via a concrete subclass test below; here we just confirm
    # the import works and the field set is what we expect.
    assert set(JobEventBase.model_fields.keys()) == {
        "event_id", "occurred_at", "job_id", "job_title",
        "job_disc_type", "job_imdb_id",
    }
