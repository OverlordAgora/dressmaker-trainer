"""Entry point for the Dressmaker Trainer pipeline."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from loguru import logger

from dressmaker_trainer.config.loader import load_config
from dressmaker_trainer.utils.logging_setup import setup_logging
from dressmaker_trainer.pipeline.runner import PipelineRunner


def parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="dressmaker-trainer")
    p.add_argument("--config", type=Path, default=Path("trainer_config.toml"))
    p.add_argument("--profile", type=str, default="default")
    p.add_argument("--dry-run", action="store_true", help="wire pipeline, no input emission")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    setup_logging()
    cfg = load_config(args.config, profile=args.profile)
    logger.info("starting dressmaker-trainer profile={} dry_run={}", args.profile, args.dry_run)

    runner = PipelineRunner.from_config(cfg, dry_run=args.dry_run)
    try:
        runner.run_forever()
    except KeyboardInterrupt:
        logger.info("shutdown requested")
        runner.stop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())