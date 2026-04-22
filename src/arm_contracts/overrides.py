"""Overrides models: the inner shape of the preset/transcode-config wire contract.

Scheme-specific advanced fields (x265_preset, nvenc_preset, qsv_preset, etc.)
pass through SharedOverrides and TierOverrides as extras (extra='allow').
The transcoder applies scheme-aware validation at the routers/presets.py
boundary against scheme.advanced_fields. Typing each scheme's advanced fields
with a discriminated union is a v2 enhancement.
"""
from pydantic import BaseModel, ConfigDict, Field


class SharedOverrides(BaseModel):
    """Fields that apply to every tier of a resolved preset."""
    model_config = ConfigDict(extra="allow")

    video_encoder: str | None = None
    audio_encoder: str | None = None
    subtitle_mode: str | None = None


class TierOverrides(BaseModel):
    """Fields for a single resolution tier (dvd/bluray/uhd)."""
    model_config = ConfigDict(extra="allow")

    handbrake_preset: str | None = None
    video_quality: int | None = Field(default=None, ge=0, le=51)
    handbrake_extra_args: list[str] | None = None
