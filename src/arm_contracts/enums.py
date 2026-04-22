"""Shared enums for the ARM fork cross-service wire contract."""
from enum import StrEnum


class JobStatus(StrEnum):
    """Unified transcode job status.

    Members that persist to transcoder TranscodeJobDB.status:
      pending, processing, completed, failed, cancelled.

    Callback-only member (sent to arm-neu's transcode-callback endpoint
    but NEVER persisted in the transcoder's own JobStatus column):
      partial - emitted when some tracks succeeded and others failed;
      the transcoder always stores COMPLETED for that outcome and lets
      arm-neu decide how to represent it.
    """
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    partial = "partial"          # callback wire only
    cancelled = "cancelled"


class Disctype(StrEnum):
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


class VideoType(StrEnum):
    """High-level content classification used for folder layout."""
    movie = "movie"
    series = "series"
    unknown = "unknown"


class TierName(StrEnum):
    """Closed set of resolution tiers known to the preset system."""
    dvd = "dvd"
    bluray = "bluray"
    uhd = "uhd"


class SchemeSlug(StrEnum):
    """Transcoder encoder scheme. Selected at transcoder boot from GPU probe."""
    software = "software"
    nvidia = "nvidia"
    intel = "intel"
    amd = "amd"
