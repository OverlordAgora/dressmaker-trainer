# Security Policy

Dressmaker Trainer is a hobbyist Windows desktop tool. It reads screen
frames via `pywin32`/`opencv` and synthesizes input through the Win32
input APIs. It does **not** ship a kernel driver, does not patch game
binaries, and does not include any memory-reading component.

## Reporting a vulnerability

- Do not open a public issue for anything that allows arbitrary code
  execution, credential theft, or elevation of privilege.
- Email `security@dressmaker-trainer.invalid` with steps to reproduce.
- We aim to acknowledge within 72 hours.

## Scope

In scope:
- Input-injection handlers (`dressmaker_trainer/drivers/input_driver.py`)
- Config parsing for untrusted TOML profiles
- Overlay rendering surface

Out of scope:
- Third-party game anti-cheat behaviour
- Anything requiring a modified Windows kernel

## Responsible use

This repository is provided **for educational and hobbyist use only**.
Use at your own risk. Running automation against online games may violate
their terms of service; the maintainers take no responsibility for bans.