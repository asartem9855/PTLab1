"""Read the indented TXT format from the laboratory guide."""

from .DataReader import DataReader
from .Types import DataType
from .validation import validate


class TextDataReader(DataReader):
    def read(self, path: str) -> DataType:
        students: DataType = {}
        current = None
        with open(path, encoding="utf-8-sig") as source:
            for number, line in enumerate(source, 1):
                if not line.strip():
                    continue
                if not line[0].isspace():
                    current = line.strip()
                    if current in students:
                        raise ValueError(f"Повтор студента: {current}")
                    students[current] = []
                else:
                    if current is None:
                        raise ValueError("Дисциплина указана до имени студента")
                    try:
                        subject, score = line.strip().split(":", 1)
                        students[current].append((subject.strip(), int(score)))
                    except ValueError as error:
                        raise ValueError(
                            f"Некорректная строка {number}"
                        ) from error
        return validate(students)
