import pytest

from src.CalcRating import CalcRating
from src.DataReader import DataReader
from src.TextDataReader import TextDataReader
from src.main import get_path_from_arguments, main


def test_abstract_reader():
    with pytest.raises(TypeError):
        DataReader()


def test_average_and_empty_input():
    assert CalcRating({"Иван": [("A", 80), ("B", 91)]}).calc() == {
        "Иван": 85.5
    }
    assert CalcRating({}).calc() == {}


def test_text_reader_reuse(tmp_path):
    path = tmp_path / "students.txt"
    path.write_text("Иван\n    A:90\n\n    B:80\n", encoding="utf-8")
    reader = TextDataReader()
    assert reader.read(str(path)) == {"Иван": [("A", 90), ("B", 80)]}
    path.write_text("Анна\n    C:100\n", encoding="utf-8")
    assert reader.read(str(path)) == {"Анна": [("C", 100)]}


@pytest.mark.parametrize("content", [
    "    A:90", "Иван\n", "Иван\n A:101", "Иван\n A:no",
    "Иван\n A:1\n A:2", "Иван\n A:1\nИван\n B:2",
    "Иван\n no-colon", "Иван\n :90", "Иван\n A:-1",
])
def test_invalid_text(tmp_path, content):
    path = tmp_path / "bad.txt"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError):
        TextDataReader().read(str(path))


def test_arguments():
    assert get_path_from_arguments(["-p", "file.txt"]) == "file.txt"
    with pytest.raises(SystemExit):
        get_path_from_arguments([])


def test_main_text(capsys):
    assert main(["-p", "data/data.txt"]) == 0
    assert "90.00" in capsys.readouterr().out


@pytest.mark.parametrize("path", ["missing.txt", "bad.json"])
def test_main_errors(path, capsys):
    assert main(["-p", path]) == 1
    assert "Ошибка" in capsys.readouterr().err


@pytest.mark.parametrize("data", [
    {"": [("A", 90)]}, {1: [("A", 90)]}, {"Иван": []},
    {"Иван": [(1, 90)]}, {"Иван": [("A", True)]},
])
def test_invalid_data(data):
    with pytest.raises(ValueError):
        CalcRating(data)
