"""Shared enums for the ARM fork cross-service wire contract.

Enums inherit from ``_StrValueEnum`` (str + Enum with __str__ override)
rather than ``StrEnum`` for Python 3.10 compatibility (arm-neu's base
image still ships 3.10.12). The __str__ override matches StrEnum's
behavior: ``str(Member)`` and f-string interpolation produce the value,
not ``ClassName.member``.
"""
from enum import Enum


class _StrValueEnum(str, Enum):
    """Base for string-valued enums, behaves like Python 3.11's StrEnum."""

    def __str__(self) -> str:
        return self.value

    def __format__(self, format_spec: str) -> str:
        return self.value.__format__(format_spec)


class JobStatus(_StrValueEnum):
    """Unified transcode job status.

    Members that persist to transcoder TranscodeJobDB.status:
      pending, processing, completed, failed, cancelled.

    Callback-only members (sent to arm-neu's transcode-callback endpoint
    but NEVER persisted in the transcoder's own JobStatus column):
      partial - emitted when some tracks succeeded and others failed;
        the transcoder always stores COMPLETED for that outcome and lets
        arm-neu decide how to represent it.
      transcoding - informational fire-and-forget heartbeat sent when a
        job leaves the queue and starts processing. The transcoder stores
        PROCESSING for that state; arm-neu maps the wire string to its
        own JobState.TRANSCODE_ACTIVE so the dashboard reflects the
        active phase.
    """
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    partial = "partial"              # callback wire only
    transcoding = "transcoding"      # callback wire only (informational)
    cancelled = "cancelled"


class Disctype(_StrValueEnum):
    """Disc media type as emitted by arm-neu on the wire.

    Note: UHD Blu-ray is 'bluray4k' here (see arm-neu
    arm/models/job.py:286 where get_disc_type sets disctype='bluray4k'
    for INDX0300 headers). The string 'uhd' is the preset tier name
    (see TierName), NOT a disctype value. These are separate concepts
    that happen to collide in natural English.
    """
    dvd = "dvd"
    bluray = "bluray"
    bluray4k = "bluray4k"
    music = "music"
    data = "data"
    unknown = "unknown"


class VideoType(_StrValueEnum):
    """High-level content classification used for folder layout."""
    movie = "movie"
    series = "series"
    unknown = "unknown"


class TierName(_StrValueEnum):
    """Closed set of resolution tiers known to the preset system."""
    dvd = "dvd"
    bluray = "bluray"
    uhd = "uhd"


class SchemeSlug(_StrValueEnum):
    """Transcoder encoder scheme. Selected at transcoder boot from GPU probe."""
    software = "software"
    nvidia = "nvidia"
    intel = "intel"
    amd = "amd"
