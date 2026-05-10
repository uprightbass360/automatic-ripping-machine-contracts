# components/contracts/tests/test_media_metadata.py
"""Tests for the MediaMetadata contract."""
from datetime import date

import pytest
from pydantic import ValidationError

from arm_contracts.enums import VideoType
from arm_contracts.media_metadata import MediaMetadata


def test_minimal_construction_accepts_all_optional():
    """Empty MediaMetadata should construct cleanly - every field is optional."""
    m = MediaMetadata()
    assert m.title is None
    assert m.year is None
    assert m.video_type is None
    assert m.imdb_id is None
    assert m.genres == []
    assert m.directors == []
    assert m.actors == []


def test_full_movie_payload_round_trips():
    """A typical movie payload from OMDb survives serialization."""
    m = MediaMetadata(
        title="Annihilation",
        year="2018",
        video_type=VideoType.movie,
        imdb_id="tt2798920",
        runtime_seconds=6900,
        plot="A biologist signs up for a mission...",
        genres=["Sci-Fi", "Drama", "Adventure"],
        directors=["Alex Garland"],
        mpaa_rating="R",
        released_date=date(2018, 2, 23),
        language="en",
        country="USA",
        imdb_rating=6.8,
    )
    blob = m.model_dump_json()
    restored = MediaMetadata.model_validate_json(blob)
    assert restored.title == "Annihilation"
    assert restored.runtime_seconds == 6900
    assert restored.released_date == date(2018, 2, 23)
    assert restored.imdb_rating == pytest.approx(6.8)


def test_imdb_id_pattern_rejects_garbage():
    """imdb_id must match tt\\d+ or be empty/None."""
    with pytest.raises(ValidationError):
        MediaMetadata(imdb_id="not-an-imdb-id")


def test_year_pattern_rejects_two_digit():
    """year must be a 4-digit string or empty."""
    with pytest.raises(ValidationError):
        MediaMetadata(year="18")


def test_imdb_rating_bounds():
    """imdb_rating is bounded 0.0..10.0."""
    with pytest.raises(ValidationError):
        MediaMetadata(imdb_rating=11.0)
    with pytest.raises(ValidationError):
        MediaMetadata(imdb_rating=-0.1)
    # Boundary values pass
    MediaMetadata(imdb_rating=0.0)
    MediaMetadata(imdb_rating=10.0)


def test_runtime_seconds_non_negative():
    """runtime_seconds cannot be negative."""
    with pytest.raises(ValidationError):
        MediaMetadata(runtime_seconds=-1)


def test_audio_payload_round_trips():
    """Music CD payload from MusicBrainz uses artist/album/album_artist."""
    m = MediaMetadata(
        video_type=VideoType.music,
        artist="Pink Floyd",
        album="The Dark Side of the Moon",
        album_artist="Pink Floyd",
        released_date=date(1973, 3, 1),
        genres=["Progressive Rock"],
    )
    restored = MediaMetadata.model_validate_json(m.model_dump_json())
    assert restored.album == "The Dark Side of the Moon"
    assert restored.album_artist == "Pink Floyd"


def test_extra_fields_ignored():
    """Provider quirks that smuggle extra keys must not break validation."""
    payload = {
        "title": "Annihilation",
        "year": "2018",
        "some_provider_specific_key": "ignored",
    }
    m = MediaMetadata.model_validate(payload)
    assert m.title == "Annihilation"
    assert not hasattr(m, "some_provider_specific_key")


def test_re_exported_from_package_root():
    """Consumers should be able to `from arm_contracts import MediaMetadata`."""
    from arm_contracts import MediaMetadata as M  # noqa: F401
    from arm_contracts import PATTERN_TOKENS as T  # noqa: F401
    assert isinstance(T, dict)
    assert "title" in T
    assert "director" in T
