"""Webhook payload: arm-neu -> transcoder POST /webhook/arm.

This is the wire shape for the in-bound webhook the transcoder accepts when
arm-neu finishes ripping a disc. arm-neu's `_build_webhook_payload`
(arm/ripper/utils.py) is the producer; the transcoder's webhook router is
the consumer. Both sides should import these models so a field rename or
type change becomes a CI failure (via the lockstep workflow), not a 422
discovered in production.

Field length caps (`_MAX_*`) intentionally match the transcoder's
`src/constants.py` values so existing transcoder validators that bound
free-text fields keep their semantics after the migration.
"""
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from arm_contracts.enums import WebhookEventType
from arm_contracts.job_config import TranscodeJobConfig

# Field-length bounds. Match transcoder src/constants.py at v17.3.0.
_MAX_TITLE_LENGTH = 500
_MAX_BODY_LENGTH = 2000
_MAX_PATH_LENGTH = 1000
_MAX_NAME_LENGTH = 500


def _strip_controls(value: str, *, keep_newlines_tabs: bool = False) -> str:
    """Remove ASCII control characters (and the null byte) from *value*."""
    cleaned = value.replace("\x00", "")
    if keep_newlines_tabs:
        return "".join(c for c in cleaned if c in "\n\t" or ord(c) >= 32)
    return "".join(c for c in cleaned if ord(c) >= 32)


class WebhookTrackMeta(BaseModel):
    """Per-track metadata included in WebhookPayload.tracks.

    arm-neu pre-renders folder/title names from arm.yaml patterns so the
    transcoder doesn't need its own naming engine. All string fields are
    stringified at the producer (e.g. ``str(track.year or '')``) so empty
    values arrive as ``""`` rather than null.
    """
    model_config = ConfigDict(extra="ignore")

    track_number: str = ""
    title: str = ""
    year: str = ""
    video_type: str = ""
    filename: str = ""
    has_custom_title: bool = False
    folder_name: str = ""
    title_name: str = ""
    episode_number: str = ""
    episode_name: str = ""


class WebhookPayload(BaseModel):
    """Top-level payload for POST /webhook/arm.

    The transcoder accepts both Apprise-shaped POSTs (which use ``message``
    instead of ``body``) and direct curl-shaped POSTs from arm-neu (which
    use ``body``). Both fields are kept; consumers should prefer
    :py:meth:`effective_body` to read whichever is set.
    """
    model_config = ConfigDict(extra="ignore")

    title: str = Field(..., max_length=_MAX_TITLE_LENGTH)
    body: str | None = Field(None, max_length=_MAX_BODY_LENGTH)
    message: str | None = Field(None, max_length=_MAX_BODY_LENGTH)
    path: str | None = Field(None, max_length=_MAX_PATH_LENGTH)
    job_id: int
    status: str | None = Field(None, max_length=50)
    type: WebhookEventType | None = None

    # Disc/content classification - free strings so the contract doesn't
    # break if either side adds a new disctype before the enum is updated.
    video_type: str | None = Field(None, max_length=50)
    year: str | None = Field(None, max_length=10)
    disctype: str | None = Field(None, max_length=50)
    poster_url: str | None = Field(None, max_length=_MAX_PATH_LENGTH)

    # Pre-rendered names from arm-neu's naming engine.
    folder_name: str | None = Field(None, max_length=_MAX_NAME_LENGTH)
    title_name: str | None = Field(None, max_length=_MAX_NAME_LENGTH)

    # Per-job overrides; reuses the existing TranscodeJobConfig envelope
    # rather than duplicating the preset_slug/overrides shape here.
    config_overrides: TranscodeJobConfig | None = None

    multi_title: bool | None = None
    tracks: list[WebhookTrackMeta] | None = None

    @property
    def effective_body(self) -> str | None:
        """Return whichever of body/message is set (body wins if both)."""
        return self.body or self.message

    @field_validator("title")
    @classmethod
    def _validate_title(cls, value: str) -> str:
        """Title is required, non-blank, and stripped of control characters."""
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        return _strip_controls(value).strip()

    @field_validator("body", "message")
    @classmethod
    def _validate_body(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _strip_controls(value, keep_newlines_tabs=True).strip()

    @field_validator("path")
    @classmethod
    def _validate_path(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return _strip_controls(value).strip()

    @field_validator("job_id", mode="before")
    @classmethod
    def _coerce_job_id(cls, value: Any) -> int:
        """arm-neu sends job_id as a string ("123"); accept both forms."""
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("job_id must be a valid integer") from exc
