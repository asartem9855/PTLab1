"""Command-line entry point: python -m src.main -p data/data.txt."""

import argparse
from pathlib import Path

from .CalcRating import CalcRating
from .TextDataReader import TextDataReader
from .YamlDataReader import YamlDataReader
from .StudentFinder import StudentFinder


def get_path_from_arguments(args: list[str]) -> str:
    parser = argparse.ArgumentParser(description="Рейтинг студентов")
    parser.add_argument("-p", "--path", required=True, help="Путь к данным")
    return parser.parse_args(args).path


def main(args=None) -> int:
    import sys

    path = get_path_from_arguments(sys.argv[1:] if args is None else args)
    try:
        readers = {".txt": TextDataReader, ".yaml": YamlDataReader,
                   ".yml": YamlDataReader}
        suffix = Path(path).suffix.lower()
        if suffix not in readers:
            raise ValueError("Поддерживаются форматы .txt, .yaml, .yml")
        students = readers[suffix]().read(path)
        for name, rating in CalcRating(students).calc().items():
            print(f"{name}: {rating:.2f}")
        found = StudentFinder(students).find()
        if found is None:
            print("Студентов с 90 баллами по всем дисциплинам нет.")
        else:
            print(f"Студент с 90 баллами по всем дисциплинам: {found}")
    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
