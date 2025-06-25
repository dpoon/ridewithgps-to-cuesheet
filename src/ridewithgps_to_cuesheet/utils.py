import csv
from pathlib import Path
from typing import List


def read_csv_to_array(filename: str) -> List[List[str]]:
    """
    Read a UTF-8 CSV file and return its contents as a list of lists, skipping the header row.

    Args:
        filename: Path to the CSV file

    Returns:
        List of lists representing CSV rows (excluding header)

    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        PermissionError: If the file cannot be read due to permissions
        UnicodeDecodeError: If the file is not valid UTF-8
        csv.Error: If there's an error parsing the CSV
    """
    file_path = Path(filename)

    if not file_path.exists():
        raise FileNotFoundError(f"CSV file not found: {filename}")

    if not file_path.is_file():
        raise ValueError(f"Path is not a file: {filename}")

    values: List[List[str]] = []
    try:
        with open(file_path, "r", encoding="utf-8", newline="") as csvfile:
            reader = csv.reader(csvfile)
            # Skip header row if file is not empty
            try:
                next(reader)
            except StopIteration:
                # File is empty or only has header
                return values

            values = list(reader)

    except PermissionError:
        raise PermissionError(f"Permission denied reading file: {filename}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(e.encoding, e.object, e.start, e.end, f"File is not valid UTF-8: {filename}")
    except csv.Error as e:
        raise csv.Error(f"Error parsing CSV file {filename}: {e}")

    return values
