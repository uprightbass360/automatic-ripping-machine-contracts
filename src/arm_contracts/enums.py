"""Shared enums for the ARM fork cross-service wire contract."""
from enum import StrEnum


class JobStatus(StrEnum):
    """Unified transcode job status used on the wire and in DBs.

    Additional in-flight states the transcoder reports in callbacks
    (e.g. 'transcoding') map to 'processing' at the wire boundary.
    """
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"
    partial = "partial"
    cancelled = "cancelled"


class Disctype(StrEnum):
    """Disc media type reported by ARM at webhook time."""
    dvd = "dvd"
    bluray = "bluray"
    uhd = "uhd"
    music = "music"
    data = "data"


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
