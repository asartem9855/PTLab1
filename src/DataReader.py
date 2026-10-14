"""Common interface for file readers."""

from abc import ABC, abstractmethod

from .Types import DataType


class DataReader(ABC):
    @abstractmethod
    def read(self, path: str) -> DataType:
        """Read and validate a student data file."""
