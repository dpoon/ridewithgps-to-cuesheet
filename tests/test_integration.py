import tempfile
from pathlib import Path

import pytest

from ridewithgps_to_cuesheet import conversion
from ridewithgps_to_cuesheet.utils import read_csv_to_array


def test_full_workflow_with_test_data():
    test_file = Path(__file__).parent / "data" / "test_route.csv"
    csv_data = read_csv_to_array(str(test_file))

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
        output_file = temp_file.name

    try:
        opts = conversion.GenerationOptions(verbose=True)
        conversion.generate_excel(output_file, csv_data, opts)

        output_path = Path(output_file)
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    finally:
        Path(output_file).unlink(missing_ok=True)


def test_workflow_with_controls():
    csv_data = [
        ["Type", "Notes", "Distance (km) From Start", "Elevation (m)", "Description"],
        ["Start", "Start of route", "0", "0", ""],
        ["Right", "Right on Test St", "1.0", "10.0", ""],
        ["Food", "Food stop", "5.0", "20.0", ""],
        ["Control", "Control point", "10.0", "30.0", ""],
        ["Summit", "Summit finish", "15.0", "100.0", ""],
    ]

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
        output_file = temp_file.name

    try:
        opts = conversion.GenerationOptions(include_distance_from_last=True, hide_direction=False, verbose=False)
        conversion.generate_excel(output_file, csv_data[1:], opts)

        output_path = Path(output_file)
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    finally:
        Path(output_file).unlink(missing_ok=True)


def test_workflow_with_custom_options():
    csv_data = [["Start", "Start of route", "0", "0", ""], ["End", "End of route", "10.0", "50.0", ""]]

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
        output_file = temp_file.name

    try:
        opts = conversion.GenerationOptions(
            include_distance_from_last=True, hide_direction=True, page_break_row_interval=20
        )
        conversion.generate_excel(output_file, csv_data, opts)

        output_path = Path(output_file)
        assert output_path.exists()
        assert output_path.stat().st_size > 0

    finally:
        Path(output_file).unlink(missing_ok=True)


def test_empty_route_handling():
    csv_data = []

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
        output_file = temp_file.name

    try:
        opts = conversion.GenerationOptions()

        # Empty CSV data should raise an assertion error
        with pytest.raises(AssertionError, match="No turns found in the provided CSV data"):
            conversion.generate_excel(output_file, csv_data, opts)

    finally:
        Path(output_file).unlink(missing_ok=True)
