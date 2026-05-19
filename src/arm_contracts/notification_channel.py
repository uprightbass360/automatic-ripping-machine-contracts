"""Notification channel models.

A "channel" is one user-configured destination (a Discord webhook URL,
an outbound HTTPS endpoint with optional HMAC, a local bash script).
The channel-config discriminated union encodes the type-specific shape;
the ``Channel`` model wraps it with lifecycle metadata exposed via the
neu API.

The four valid event keys come from ``notification_event.NotificationEvent``;
they are duplicated here as a ``Literal`` so the dependency only runs in
one direction. If a fifth event is ever added, both lists must update —
the round-trip tests guard the constraint.
"""
from datetime import datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, SecretStr


class AppriseChannelConfig(BaseModel):
    """An Apprise URL such as ``discord://id/token`` or
    ``pover://user@token``. neu's compose-url endpoint assembles the
    final string from the catalog form; the user may also paste a raw
    URL directly."""
    model_config = ConfigDict(extra="ignore")
    type: Literal["apprise"] = "apprise"
    url: str


class WebhookChannelConfig(BaseModel):
    """Rich-payload HTTPS webhook. If ``shared_secret`` is set, the
    dispatcher computes HMAC-SHA256 over the canonical JSON body and
    sends it in ``X-ARM-Signature: sha256=<hex>``. ``headers`` is a
    flat map of extra static headers (e.g. ``Authorization: Bearer …``)
    that the user wants on every send."""
    model_config = ConfigDict(extra="ignore")
    type: Literal["webhook"] = "webhook"
    url: HttpUrl
    shared_secret: SecretStr | None = None
    headers: dict[str, str] | None = None


class BashChannelConfig(BaseModel):
    """Local script run as a subprocess. Job context is passed via
    ``ARM_*`` env vars; the exact list is pinned in sub-spec 2."""
    model_config = ConfigDict(extra="ignore")
    type: Literal["bash"] = "bash"
    script_path: str


ChannelConfig = Annotated[
    AppriseChannelConfig | WebhookChannelConfig | BashChannelConfig,
    Field(discriminator="type"),
]
"""Discriminated union of channel configs. Stored as JSON in the
``notification_channel.config`` column."""
