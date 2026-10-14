"""Shared validation prevents ambiguous or incomplete student records."""

from .Types import DataType


def validate(data: DataType) -> DataType:
    for name, subjects in data.items():
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя студента должно быть непустой строкой")
        if not subjects:
            raise ValueError(f"У студента {name} нет дисциплин")
        seen = set()
        for subject, score in subjects:
            if not isinstance(subject, str) or not subject.strip():
                raise ValueError("Название дисциплины должно быть строкой")
            if subject in seen:
                raise ValueError(f"Повтор дисциплины: {subject}")
            seen.add(subject)
            if type(score) is not int or not 0 <= score <= 100:
                raise ValueError("Оценка должна быть целым числом от 0 до 100")
    return data
