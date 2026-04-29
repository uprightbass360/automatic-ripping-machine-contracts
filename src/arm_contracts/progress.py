"""JobProgressState: arm-neu -> arm-ui /jobs/{id}/progress-state.

A single-roundtrip bundle of "what's the rip doing right now" used by the
UI's per-job progress widget. Producer: `get_job_progress_state` in
arm-neu/arm/api/v1/jobs.py. Consumer: arm-ui's `/api/jobs/{id}/progress`
endpoint, which renames `track_counts.total/ripped` to
`tracks_total/tracks_ripped` for the frontend - that BFF rename stays put;
the contract preserves the ripper-side names.
"""
from pydantic import BaseModel, ConfigDict

from arm_contracts.track import TrackCounts


class JobProgressState(BaseModel):
    """Per-job progress snapshot.

    `track_counts` reflects the rippable-subset progress (same shape as
    /jobs/{id}/track-counts). `rip_progress` (0-100) and `rip_stage`
    come from MakeMKV PRGV log parsing; `tracks_ripped_realtime` is the
    live track count from the same source (may lead `track_counts.ripped`
    while a rip is in flight). `music_progress` and `music_stage` come
    from abcde log parsing for music CDs.
    """
    model_config = ConfigDict(extra="ignore")

    track_counts: TrackCounts
    disctype: str | None = None
    logfile: str | None = None
    no_of_titles: int | None = None

    # MakeMKV (video) progress.
    rip_progress: int | None = None
    rip_stage: str | None = None
    tracks_ripped_realtime: int | None = None

    # abcde (music) progress.
    music_progress: int | None = None
    music_stage: str | None = None
