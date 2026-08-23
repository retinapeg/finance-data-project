"""Backward-compatible entrypoint kept for historical script-based use."""

from finance_data_project.cli import run


def main() -> int:
    return run()


if __name__ == "__main__":
    raise SystemExit(main())

