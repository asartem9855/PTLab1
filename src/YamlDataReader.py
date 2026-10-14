"""Safe YAML reader for the list-of-mappings format in the guide."""

import yaml

from .DataReader import DataReader
from .Types import DataType
from .validation import validate


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate keys instead of silently losing source data."""


def unique_mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if not isinstance(key, str):
            raise ValueError("Ключи YAML должны быть строками")
        if key in result:
            raise ValueError(f"Повтор ключа YAML: {key}")
        result[key] = loader.construct_object(value_node)
    return result


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping
)


class YamlDataReader(DataReader):
    def read(self, path: str) -> DataType:
        with open(path, encoding="utf-8-sig") as source:
            try:
                raw = yaml.load(source, Loader=UniqueKeyLoader)
            except yaml.YAMLError as error:
                raise ValueError(f"Некорректный YAML: {error}") from error
        if raw is None or raw == {}:
            return {}
        # Also accept a single mapping, a common equivalent YAML structure.
        entries = [raw] if isinstance(raw, dict) else raw
        if not isinstance(entries, list):
            raise ValueError("YAML должен содержать список студентов")
        students: DataType = {}
        for entry in entries:
            if not isinstance(entry, dict) or not entry:
                raise ValueError("Запись студента должна быть словарём")
            for name, subjects in entry.items():
                if name in students:
                    raise ValueError(f"Повтор студента: {name}")
                if not isinstance(subjects, dict):
                    raise ValueError("Дисциплины должны быть словарём")
                students[name] = list(subjects.items())
        return validate(students)
