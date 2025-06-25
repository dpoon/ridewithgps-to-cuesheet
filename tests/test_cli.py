from unittest.mock import Mock, patch

import pytest
import typer
from typer.testing import CliRunner

from ridewithgps_to_cuesheet.cli import app


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_with_filename(runner, tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("Type,Notes,Distance (km) From Start,Elevation (m),Description\n")
    with open(csv_file, "a") as f:
        f.write("Start,Start of route,0,0,\n")

    with patch("ridewithgps_to_cuesheet.cli.Converter.generate_excel") as mock_generate:
        result = runner.invoke(app, ["--filename", str(csv_file)])

        assert result.exit_code == 0
        mock_generate.assert_called_once()


def test_cli_with_url(runner):
    test_url = "https://ridewithgps.com/routes/12345"

    with patch("ridewithgps_to_cuesheet.ridewithgps.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.text = "Type,Notes,Distance (km) From Start,Elevation (m),Description\nStart,Start,0,0,\n"
        mock_response.raise_for_status = Mock()
        mock_response.apparent_encoding = "utf-8"
        mock_get.return_value = mock_response

        with patch("ridewithgps_to_cuesheet.cli.Converter.generate_excel") as mock_generate:
            result = runner.invoke(app, ["--url", test_url])

            assert result.exit_code == 0
            mock_generate.assert_called_once()


def test_cli_no_args(runner):
    result = runner.invoke(app, [])

    assert result.exit_code != 0
    assert "Error" in result.stdout or "Usage" in result.stdout


def test_cli_both_filename_and_url(runner, tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("Type,Notes,Distance (km) From Start,Elevation (m),Description\n")

    result = runner.invoke(app, ["--filename", str(csv_file), "--url", "https://ridewithgps.com/routes/12345"])

    assert result.exit_code == 0  # CLI currently allows both, should succeed


def test_cli_invalid_url(runner):
    with patch("ridewithgps_to_cuesheet.ridewithgps.requests.get") as mock_get:
        mock_get.side_effect = Exception("Network error")

        result = runner.invoke(app, ["--url", "https://invalid-url.com"])

        assert result.exit_code != 0


def test_cli_nonexistent_file(runner):
    result = runner.invoke(app, ["--filename", "/nonexistent/file.csv"])

    assert result.exit_code != 0


def test_cli_with_options(runner, tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("Type,Notes,Distance (km) From Start,Elevation (m),Description\n")
    with open(csv_file, "a") as f:
        f.write("Start,Start of route,0,0,\n")

    with patch("ridewithgps_to_cuesheet.cli.Converter.generate_excel") as mock_generate:
        result = runner.invoke(app, ["--filename", str(csv_file), "--island", "--show-direction-column", "--verbose"])

        assert result.exit_code == 0
        mock_generate.assert_called_once()


def test_cli_with_custom_output(runner, tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("Type,Notes,Distance (km) From Start,Elevation (m),Description\n")
    with open(csv_file, "a") as f:
        f.write("Start,Start of route,0,0,\n")
    output_file = tmp_path / "custom_output.xlsx"

    with patch("ridewithgps_to_cuesheet.cli.Converter.generate_excel") as mock_generate:
        result = runner.invoke(app, ["--filename", str(csv_file), "--output", str(output_file)])

        assert result.exit_code == 0
        mock_generate.assert_called_once()


def test_validate_url_valid():
    from ridewithgps_to_cuesheet.cli import validate_ridewithgps_url

    valid_urls = [
        "https://ridewithgps.com/routes/12345",
        "https://ridewithgps.com/routes/67890",
    ]

    for url in valid_urls:
        result = validate_ridewithgps_url(url)

        assert result.url == url
        assert result.id in ["12345", "67890"]


def test_validate_url_invalid():
    from ridewithgps_to_cuesheet.cli import validate_ridewithgps_url

    with pytest.raises(typer.BadParameter):
        validate_ridewithgps_url("https://example.com/routes/12345")


def test_cli_help(runner):
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Convert RideWithGPS routes" in result.stdout
