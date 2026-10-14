import pytest

from src.StudentFinder import StudentFinder
from src.main import main


@pytest.mark.parametrize("data, expected", [
    ({}, None),
    ({"Иван": [("A", 90)]}, "Иван"),
    ({"Иван": [("A", 90), ("B", 90)]}, "Иван"),
    ({"Иван": [("A", 100), ("B", 80)]}, None),
    ({"Иван": [("A", 91), ("B", 90)]}, None),
    ({"Иван": [("A", 89), ("B", 90)]}, None),
    ({"Иван": [("A", 90)], "Анна": [("B", 90)]}, "Иван"),
    ({"Иван": [("A", 100)], "Анна": [("B", 90)]}, "Анна"),
])
def test_exact_ninety(data, expected):
    assert StudentFinder(data).find() == expected


def test_no_disciplines_is_invalid():
    with pytest.raises(ValueError):
        StudentFinder({"Иван": []})


def test_yaml_cli(capsys):
    assert main(["-p", "data/data.yaml"]) == 0
    output = capsys.readouterr().out
    assert "Студент с 90 баллами по всем дисциплинам: Иванов" in output


def test_cli_no_candidate(tmp_path, capsys):
    path = tmp_path / "data.yml"
    path.write_text("Иван: {A: 91}", encoding="utf-8")
    assert main(["-p", str(path)]) == 0
    assert "Студентов с 90 баллами по всем дисциплинам нет." in (
        capsys.readouterr().out
    )
