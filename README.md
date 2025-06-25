# ridewithgps-to-cuesheet
A converter for RideWithGPS Maps to Cuesheets for the BC Randonneurs

This converter was primarily written to save me time in creating routes, and eventually became popular enough that people started asking for it...

## Setup

You need uv to install dependencies. See [uv documentation](https://docs.astral.sh/uv/)

```bash
uv sync
```

## Usage

### Command Line Interface

```bash
# Get help with all options
uv run ridewithgps-to-cuesheet --help

# Convert a local CSV file
uv run ridewithgps-to-cuesheet --filename files/route.csv

# Download and convert from RideWithGPS URL
uv run ridewithgps-to-cuesheet --url https://ridewithgps.com/routes/12345
```

### Using as a Python Module

```python
import csv
from ridewithgps_to_cuesheet import generate_excel, GenerationOptions

# Read CSV data manually
def read_csv_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        return list(reader)

# Convert CSV data to Excel cuesheet
csv_data = read_csv_data("files/route.csv")
options = GenerationOptions(include_distance_from_last=True)
generate_excel("output.xlsx", csv_data, options)
```

### Common Options

- `--island` / `-i`: Show distance from last control (Vancouver Island style)
- `--show-direction-column`: show the direction column

## Configuration

### RideWithGPS Authentication

To download routes directly from URLs, copy `sample.env` to `.env` and add your credentials:

```bash
cp sample.env .env
# Edit .env with your RideWithGPS username and password
```

See `sample.env` for all configuration options.

## Output

- CSV files are organized in `files/` directory
- Generated Excel cuesheets are saved to `outputs/` directory
- Default output format: `{route_id}_cues.xlsx` or `{filename}_cues.xlsx`

## Testing

```bash
poe test
```
