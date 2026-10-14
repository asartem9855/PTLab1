import pytest

from src.TextDataReader import TextDataReader
from src.YamlDataReader import YamlDataReader


def test_yaml_matches_text():
    assert YamlDataReader().read("data/data.yaml") == (
        TextDataReader().read("data/data.txt")
    )


@pytest.mark.parametrize("content, expected", [
    ("", {}), ("[]", {}), ("{}", {}),
    ("- Иван:\n    A: 90", {"Иван": [("A", 90)]}),
    ("Иван: {A: 90}", {"Иван": [("A", 90)]}),
])
def test_supported_yaml(tmp_path, content, expected):
    path = tmp_path / "data.yaml"
    path.write_text(content, encoding="utf-8-sig")
    assert YamlDataReader().read(str(path)) == expected


@pytest.mark.parametrize("content", [
    "hello", "123", "- hello", "- {}", "- Иван: []",
    "- Иван: {}", "- Иван: {A: true}", "- Иван: {A: 90.5}",
    "- Иван: {A: '90'}", "- Иван: {A: 101}", "- Иван: {A: -1}",
    "- Иван: {A: 90}\n- Иван: {B: 90}",
    "Иван: {A: 90, A: 80}", "Иван: {1: 90}", "[broken",
    "!!python/object/apply:os.system ['echo unsafe']",
    "'': {A: 90}", "Иван: {'': 90}",
])
def test_rejects_bad_yaml(tmp_path, content):
    path = tmp_path / "bad.yaml"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError):
        YamlDataReader().read(str(path))


def test_yaml_reader_does_not_accumulate_data(tmp_path):
    path = tmp_path / "data.yaml"
    reader = YamlDataReader()
    path.write_text("Иван: {A: 90}", encoding="utf-8")
    reader.read(str(path))
    path.write_text("Анна: {B: 80}", encoding="utf-8")
    assert reader.read(str(path)) == {"Анна": [("B", 80)]}


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        YamlDataReader().read("missing.yaml")
