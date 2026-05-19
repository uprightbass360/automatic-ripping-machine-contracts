"""NotificationEvent: events published by arm-neu's notification module
to its persistent outbox, then rendered into outbound messages per
subscribed channel.

The four event types (started, rip_complete, transcode_complete, failed)
form a closed discriminated union on ``event_key``. Adding a new event
type is intentionally a contracts change — consumers (neu, ui) re-pin
the contracts submodule and pick up the new variant together.

Each event carries enough job context that templates can render without
round-tripping back to neu for additional fields.
"""
from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from arm_contracts.enums import Disctype


class JobEventBase(BaseModel):
    """Fields common to every notification event.

    ``event_id`` is the idempotency key used by the outbox to de-dupe
    accidental double-publishes (e.g. if a ripper retries the same
    code path). ``occurred_at`` is the producer's clock at publish time;
    consumers should not rely on monotonicity across events.
    """
    model_config = ConfigDict(extra="ignore")

    event_id: UUID
    occurred_at: datetime
    job_id: int
    job_title: str | None = None
    job_disc_type: Disctype
    job_imdb_id: str | None = None
