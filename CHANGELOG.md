# Changelog

## [2.0.0](https://github.com/uprightbass360/automatic-ripping-machine-contracts/compare/v1.0.0...v2.0.0) (2026-05-02)


### ⚠ BREAKING CHANGES

* **enums:** JobState members previously aliased onto shared wire strings are now distinct. Renames:   VIDEO_RIPPING       'ripping'  -> 'video_ripping'   AUDIO_RIPPING       'ripping'  -> 'audio_ripping'   MANUAL_WAIT_STARTED 'waiting'  -> 'manual_paused' (member renamed to MANUAL_PAUSED)   VIDEO_WAITING       'waiting'  -> 'makemkv_throttled' (member renamed to MAKEMKV_THROTTLED)

### Features

* **enums:** disambiguate JobState aliases; add TrackStatus.failed ([f25f31e](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/f25f31e8d1b7a0a70ead226eb2598c4eee6d9b40))

## [1.0.0](https://github.com/uprightbass360/automatic-ripping-machine-contracts/compare/v0.6.0...v1.0.0) (2026-05-02)


### ⚠ BREAKING CHANGES

* **webhook:** WebhookPayload.type is now WebhookEventType | None rather than free str. Producers must send 'info' (only current member); the enum closes the contract so future event types are explicit breaking changes rather than silent typos.

### Features

* **enums:** add JobState, SourceType, TrackStatus, WebhookEventType, SkipReason ([a499c9a](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/a499c9ab168cd56195b1a4cf45a9ba9ef4f0bafb))
* **webhook:** type field is now WebhookEventType enum ([6ee32b6](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/6ee32b68d3c6bdd0cce5e9e6d76827d0909a1820))

## [0.6.0](https://github.com/uprightbass360/automatic-ripping-machine-contracts/compare/v0.5.1...v0.6.0) (2026-05-02)


### Features

* **enums:** add TranscodePhase enum ([230a4a8](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/230a4a8b6b9566d17a48b13a57a97188aac96bb9))
* ExpectedTitle pydantic contract + Job.expected_titles field ([1bc0e99](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/1bc0e9922fb93874be19b632dd07687d17bbfb32))
* Track contract adds process and skip_reason fields ([497da3c](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/497da3c5f9dfdb8e84b0cf3cc90a1bf1c46cc40e))


### Bug Fixes

* **progress:** rip_progress/music_progress are floats not ints ([67eba7b](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/67eba7b74318faf9e430c9cc67522b2ba890d6b3))

## [0.5.1](https://github.com/uprightbass360/automatic-ripping-machine-contracts/compare/v0.5.0...v0.5.1) (2026-04-29)


### Bug Fixes

* **job:** allow JobSummary to validate ORM rows ([c326774](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/c3267741bcd9e3cf47be8b85066adbd929d9d754))

## [0.5.0](https://github.com/uprightbass360/automatic-ripping-machine-contracts/compare/v0.4.0...v0.5.0) (2026-04-29)


### Features

* add Job, JobSummary, Track, TrackCounts, JobProgressState contracts ([ece12c0](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/ece12c08f7ce77042d7693d8c89ab81c0650b6d6))

## [0.4.0](https://github.com/uprightbass360/automatic-ripping-machine-contracts/compare/v0.3.0...v0.4.0) (2026-04-26)


### Features

* **enums:** add JobStatus.transcoding wire-only callback member ([4dc451b](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/4dc451b8bbd333ab33a24bd913e20fb047246df9))

## [0.3.0](https://github.com/uprightbass360/automatic-ripping-machine-contracts/compare/v0.2.1...v0.3.0) (2026-04-26)


### Features

* **webhook:** add WebhookPayload + TranscodeCallbackPayload contracts ([f47df4a](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/f47df4a23f91f909f3ce66b9c4016ee3551cfcf4))

## [0.2.1](https://github.com/uprightbass360/automatic-ripping-machine-contracts/compare/v0.2.0...v0.2.1) (2026-04-23)


### Bug Fixes

* drop Python 3.11 requirement for arm-neu 3.10 base-image compat ([461f5c3](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/461f5c36ae2828767eb10442cecb4afe4a91d162))

## [0.2.0](https://github.com/uprightbass360/automatic-ripping-machine-contracts/compare/v0.1.0...v0.2.0) (2026-04-22)


### Features

* add shared enums (JobStatus, Disctype, VideoType, TierName, SchemeSlug) ([c0a3a11](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/c0a3a115ff0e9794fcb92ed9b9082db43130ce16))
* add SharedOverrides and TierOverrides models ([6442a98](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/6442a987eb2d8361c569a31c97cda55fa3db87c8))
* add TierOverridesByName and TranscodeOverrides envelope ([7393402](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/73934023d2571aa8d184f049d6235c7e2b654822))
* add TranscodeJobConfig wire envelope ([9c8fea2](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/9c8fea2dfd8542f13fd566b1c8d5acaf0e538a48))


### Bug Fixes

* correct Disctype wire values and harden enum tests ([d41cadf](https://github.com/uprightbass360/automatic-ripping-machine-contracts/commit/d41cadf8999fca954d2714b59f48ed843789226d))

## Changelog
