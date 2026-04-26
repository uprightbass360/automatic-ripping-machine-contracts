"""Tests for shared enums."""
import pytest


def test_job_status_members():
    from arm_contracts import JobStatus
    assert JobStatus.pending == "pending"
    assert JobStatus.processing == "processing"
    assert JobStatus.completed == "completed"
    assert JobStatus.failed == "failed"
    assert JobStatus.partial == "partial"
    assert JobStatus.transcoding == "transcoding"
    assert JobStatus.cancelled == "cancelled"


def test_job_status_wire_only_members_validate_in_callback_payload():
    """partial + transcoding both validate in TranscodeCallbackPayload.

    Both are wire-only members (the transcoder never persists them) but
    they are sent to arm-neu's transcode-callback endpoint, so the typed
    payload must accept them.
    """
    from arm_contracts import JobStatus, TranscodeCallbackPayload
    for status in (JobStatus.partial, JobStatus.transcoding):
        p = TranscodeCallbackPayload(status=status)
        assert p.status == status


def test_job_status_is_str_enum():
    """JobStatus members must be usable as plain strings (StrEnum semantics)."""
    from arm_contracts import JobStatus
    assert isinstance(JobStatus.pending, str)
    assert JobStatus.pending == "pending"
    assert f"status={JobStatus.completed}" == "status=completed"


def test_disctype_members():
    from arm_contracts import Disctype
    assert set(Disctype) == {
        Disctype.dvd, Disctype.bluray, Disctype.bluray4k,
        Disctype.music, Disctype.data, Disctype.unknown,
    }
    assert Disctype.dvd == "dvd"
    assert Disctype.bluray4k == "bluray4k"
    assert Disctype.unknown == "unknown"


def test_video_type_members():
    from arm_contracts import VideoType
    assert set(VideoType) == {VideoType.movie, VideoType.series, VideoType.unknown}
    assert VideoType.movie == "movie"


def test_tier_name_members():
    from arm_contracts import TierName
    assert set(TierName) == {TierName.dvd, TierName.bluray, TierName.uhd}
    # Value assertions: the preset system uses these exact strings as dict keys
    assert TierName.dvd == "dvd"
    assert TierName.bluray == "bluray"
    assert TierName.uhd == "uhd"


def test_scheme_slug_members():
    from arm_contracts import SchemeSlug
    assert set(SchemeSlug) == {
        SchemeSlug.software, SchemeSlug.nvidia, SchemeSlug.intel, SchemeSlug.amd,
    }
    # Value assertions: these drive GPU_VENDOR routing in the transcoder
    assert SchemeSlug.software == "software"
    assert SchemeSlug.nvidia == "nvidia"
