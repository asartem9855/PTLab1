"""Variant 9: exactly 90 points in every discipline."""

from .Types import DataType
from .validation import validate


class StudentFinder:
    def __init__(self, data: DataType) -> None:
        self.data = validate(data)

    def find(self) -> str | None:
        for name, subjects in self.data.items():
            if all(score == 90 for _, score in subjects):
                return name
        return None
