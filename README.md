# arm-contracts

Shared Pydantic models for the cross-service wire contract between arm-neu,
automatic-ripping-machine-transcoder, and automatic-ripping-machine-ui.

Consumers include this repo as a git submodule at `components/contracts`
and install it editable via `pip install -e components/contracts`. A CI
gate in each consumer repo enforces that the submodule points at this
repo's main tip; an auto-bump workflow opens a PR on each consumer when
main advances here.

Design doc: `../ai/arm-neu/docs/superpowers/specs/2026-04-22-shared-contracts-and-submodule-lockstep-design.md`

