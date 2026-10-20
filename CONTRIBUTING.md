# Contributing to Dressmaker Trainer

Thanks for helping improve the Dressmaker Trainer pipeline.

## Development environment

1. Windows 10/11, Python 3.11+ (3.12 recommended).
2. `python -m venv .venv && .venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. `python -m dressmaker_trainer.app --dry-run` to verify the pipeline wires up.

## Workflow

- Fork, branch from `main`, keep PRs focused on one stage
  (ingest / processor / driver).
- New processors go under `dressmaker_trainer/processors/` and must
  register themselves via `@register_processor("name")`.
- New output drivers go under `dressmaker_trainer/drivers/` and must
  implement `BaseDriver.emit(frame: Frame) -> bool`.
- Add a test under `tests/` using the `FakeCapture` fixture.

## Style

- `ruff` + `black` defaults, line length 100.
- No blocking calls in the ingest loop; use the worker queue.
- Log through `dressmaker_trainer.utils.logging_setup`, never `print`.

## Reporting

Open an issue with the pipeline stage, the profile TOML (redact paths),
and the tail of `logs/trainer.log`.