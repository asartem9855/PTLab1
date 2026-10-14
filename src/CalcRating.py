"""Calculate arithmetic means for all students."""

from .Types import DataType, RatingType
from .validation import validate


class CalcRating:
    def __init__(self, data: DataType) -> None:
        self.data = validate(data)

    def calc(self) -> RatingType:
        return {
            name: sum(score for _, score in subjects) / len(subjects)
            for name, subjects in self.data.items()
        }
