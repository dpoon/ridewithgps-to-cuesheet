from pathlib import Path

import pytest

from ridewithgps_to_cuesheet.utils import read_csv_to_array


def test_read_valid_csv():
    test_file = Path(__file__).parent / "data" / "test_route.csv"

    result = read_csv_to_array(str(test_file))

    assert len(result) == 7
    assert result[0] == ["Start", "Start of route", "0", "0", ""]
    assert result[1] == ["Right", "Right on Test St", "0.5", "10.0", ""]
    assert result[-1] == ["End", "End of route", "20.0", "30.0", ""]


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        read_csv_to_array("nonexistent_file.csv")


def test_path_is_not_file(tmp_path):
    directory = tmp_path / "test_dir"
    directory.mkdir()

    with pytest.raises(ValueError, match="Path is not a file"):
        read_csv_to_array(str(directory))


def test_empty_csv(tmp_path):
    empty_file = tmp_path / "empty.csv"
    empty_file.write_text("header1,header2\n")

    result = read_csv_to_array(str(empty_file))

    assert result == []


def test_csv_with_quotes_and_commas(tmp_path):
    csv_content = """Type,Notes,Distance
Start,"Start of route, here",0
Right,"Turn right, carefully",1.5"""
    test_file = tmp_path / "test_quotes.csv"
    test_file.write_text(csv_content)

    result = read_csv_to_array(str(test_file))

    assert len(result) == 2
    assert result[0] == ["Start", "Start of route, here", "0"]
    assert result[1] == ["Right", "Turn right, carefully", "1.5"]
