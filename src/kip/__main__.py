"""Entry point for `python -m kip`, so the CLI runs without installation."""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
