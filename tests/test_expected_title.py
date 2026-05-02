"""ExpectedTitle pydantic contract tests."""

import pytest
from pydantic import ValidationError

from arm_contracts import ExpectedTitle, Job


def test_expected_title_movie_shape():
    et = ExpectedTitle(
        source="omdb",
        title="Inception",
        external_id="tt1375666",
        runtime_seconds=8880,
    )
    assert et.season is None
    assert et.episode_number is None


def test_expected_title_tv_shape():
    et = ExpectedTitle(
        source="tvdb",
        title="Pilot",
        season=1,
        episode_number=1,
        runtime_seconds=3300,
    )
    assert et.season == 1
    assert et.episode_number == 1


def test_expected_title_runtime_can_be_null():
    et = ExpectedTitle(source="omdb", title="Obscure", runtime_seconds=None)
    assert et.runtime_seconds is None


def test_expected_title_invalid_source_rejected():
    with pytest.raises(ValidationError):
        ExpectedTitle(source="bogus", title="x")


def test_job_default_expected_titles_empty():
    j = Job(job_id=1)
    assert j.expected_titles == []


def test_job_round_trip_with_expected_titles():
    j = Job(
        job_id=1,
        expected_titles=[
            ExpectedTitle(source="omdb", title="Inception", runtime_seconds=8880),
        ],
    )
    dumped = j.model_dump()
    rebuilt = Job.model_validate(dumped)
    assert len(rebuilt.expected_titles) == 1
    assert rebuilt.expected_titles[0].runtime_seconds == 8880
