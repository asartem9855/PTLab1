"""Command-line entry point: python -m src.main -p data/data.txt."""

import argparse
from pathlib import Path

from .CalcRating import CalcRating
from .TextDataReader import TextDataReader


def get_path_from_arguments(args: list[str]) -> str:
    parser = argparse.ArgumentParser(description="Рейтинг студентов")
    parser.add_argument("-p", "--path", required=True, help="Путь к данным")
    return parser.parse_args(args).path


def main(args=None) -> int:
    import sys

    path = get_path_from_arguments(sys.argv[1:] if args is None else args)
    try:
        if Path(path).suffix.lower() != ".txt":
            raise ValueError("Поддерживается формат .txt")
        students = TextDataReader().read(path)
        for name, rating in CalcRating(students).calc().items():
            print(f"{name}: {rating:.2f}")
    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
