# Agent instructions

Demo copy of the LaunchDarkly Python server-side SDK, used for a Warp Factories demo.

## Setup and checks
- Install: `make install` (uses `uv`)
- Unit tests: `make test` (skips Redis/Consul/DynamoDB tests; takes ~3 minutes)
- Run a subset: `LD_SKIP_DATABASE_TESTS=1 uv run pytest ldclient/testing/<path>`
- Lint and types: `make lint` (mypy, isort, pycodestyle). Must pass before opening a PR.

## Conventions
- Source is in `ldclient/`, tests in `ldclient/testing/`, mirroring the source layout.
- Add or update tests for every behavior change.
- Keep changes small and focused on the issue. Don't touch unrelated files.
- PR descriptions: what changed, why, and how it was tested (include test output).
- Never push to `main`; always open a PR.
