"""CLI interface for ridewithgps-to-cuesheet converter.

This module provides a command-line interface for converting RideWithGPS route files
to BC Randonneurs style cue sheets. It supports both local CSV files and direct URL downloads.
"""

from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import requests
import typer
from rich.console import Console

from . import ridewithgps as Converter
from .utils import read_csv_to_array

console = Console()
app = typer.Typer(
    name="ridewithgps-to-cuesheet",
    help="Convert RideWithGPS maps to BC Randonneurs style cuesheets",
    no_args_is_help=True,
)


@app.command()
def main(
    filename: Optional[str] = typer.Option(
        None,
        "--filename",
        "-f",
        help="CSV file to convert locally",
        callback=lambda v: validate_csv_file(v) if v else None,
    ),
    url: Optional[str] = typer.Option(
        None,
        "--url",
        "-u",
        help="RideWithGPS URL (e.g., https://ridewithgps.com/routes/1234)",
    ),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Override output filename"),
    csv_directory: str = typer.Option("files", "--csv-directory", "-c", help="Directory for CSV files"),
    xlsx_directory: str = typer.Option("outputs", "--xlsx-directory", "-x", help="Directory for XLSX files"),
    island: bool = typer.Option(
        False, "--island", "-i", help="Vancouver Island style: show distance from last control"
    ),
    hidedir: bool = typer.Option(False, "--hidedir", "-d", help="Hide the direction column"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    debugging: bool = typer.Option(False, "--debugging", help="Enable debug mode"),
) -> None:
    """Convert RideWithGPS routes to BC Randonneurs style cuesheets.

    You must provide either a CSV file (--filename) or a RideWithGPS URL (--url).
    """
    filename, url_info = validate_inputs(filename, url)
    inputs_path, outputs_path = Path(csv_directory), Path(xlsx_directory)

    options = {"island": island, "hidedir": hidedir, "verbose": verbose, "debugging": debugging}

    print_options(options)

    excel_filename = generate_output_filename(url_info, filename, output)
    console.print(f"[blue]Output file:[/blue] {excel_filename}")

    try:
        inputs_path.mkdir(parents=True, exist_ok=True)
        outputs_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        console.print(f"[red]Error creating directories:[/red] {e}")
        raise typer.Exit(1)

    csv_filename = prepare_csv_file(filename, url_info, verbose)
    run_conversion(csv_filename, excel_filename, options)
    organize_output_files(excel_filename, inputs_path, outputs_path, filename)

    console.print("[green]🎉 Process completed successfully![/green]")


def validate_csv_file(value: str) -> str:
    if not value.endswith(".csv"):
        raise typer.BadParameter(f"File must be a CSV file, got: {value}")

    path = Path(value)
    if not path.exists():
        raise typer.BadParameter(f"File does not exist: {value}")

    return value


def validate_ridewithgps_url(value: str) -> dict:
    RIDE_WITH_GPS_URL_PREFIX = "https://ridewithgps.com/routes/"
    if not value.startswith(RIDE_WITH_GPS_URL_PREFIX) or value[len(RIDE_WITH_GPS_URL_PREFIX) :] == "":
        raise typer.BadParameter(f"Not a valid RideWithGPS URL. Must start with {RIDE_WITH_GPS_URL_PREFIX}")

    parsed = urlparse(value)
    route_id = parsed.path.split("/")[-1]

    if not route_id or not route_id.isdigit():
        raise typer.BadParameter("URL must contain a valid route ID")

    return {"url": value, "parsed": parsed, "id": route_id}


def download_route(url_info: dict, verbose: bool = False) -> str:
    """Download route data from RideWithGPS URL."""
    download_url = url_info["url"].replace(url_info["id"], f"{url_info['id']}.csv")
    output_file = f"downloaded_cues_for_{url_info['id']}"

    if verbose:
        console.print(f"[blue]Downloading from:[/blue] {download_url}")
        console.print(f"[blue]Saving to:[/blue] {output_file}")

    try:
        response = requests.get(download_url, timeout=30)
        response.raise_for_status()

        with open(output_file, "wb") as tmp_file:
            tmp_file.write(response.content)

        if verbose:
            console.print("[green]✓[/green] Download completed successfully")

        return output_file

    except requests.RequestException as e:
        console.print(f"[red]Error downloading route:[/red] {e}")
        raise typer.Exit(1)


def run_conversion(input_csv: str, output_xlsx: str, options: dict) -> None:
    console.print("[blue]Reading CSV file...[/blue]")

    try:
        values_array = read_csv_to_array(input_csv)
        turns = Converter.parse_to_turns(values_array, options.get("verbose", False))

        console.print("[blue]Generating Excel file...[/blue]")
        Converter.generate_excel(
            filename=output_xlsx,
            turns=turns,
            opts=Converter.GenerationOptions(
                include_distance_from_last=options.get("island", False),
                hide_direction=options.get("hidedir", False),
                verbose=options.get("verbose", False),
            ),
        )

        console.print("[green]✓[/green] Conversion completed successfully!")

    except Exception as e:
        console.print(f"[red]Error during conversion:[/red] {e}")
        raise typer.Exit(1)


def organize_output_files(
    excel_filename: str, inputs_path: Path, outputs_path: Path, csv_filename: Optional[str] = None
) -> None:
    """Move generated files to appropriate directories."""
    try:
        # Move Excel file to outputs directory
        output_path = outputs_path / excel_filename
        if Path(excel_filename).exists():
            Path(excel_filename).rename(output_path)
            console.print(f"[green]✓[/green] Output saved to: {output_path}")

        if csv_filename:
            is_csv_in_input_dir = Path(csv_filename).name not in [p.name for p in inputs_path.iterdir()]
            if not is_csv_in_input_dir:
                csv_path = inputs_path / Path(csv_filename).name
                if Path(csv_filename).exists():
                    Path(csv_filename).rename(csv_path)
                console.print(f"[green]✓[/green] Input CSV moved to: {csv_path}")

    except OSError as e:
        console.print(f"[yellow]Warning:[/yellow] Could not organize files: {e}")


def generate_output_filename(
    url_info: Optional[dict] = None, csv_filename: Optional[str] = None, custom_output: Optional[str] = None
) -> str:
    if custom_output:
        return custom_output
    elif url_info:
        return f"{url_info['id']}_cues.xlsx"
    elif csv_filename:
        stem = Path(csv_filename).stem
        return f"{stem}_cues.xlsx"
    return "output_cues.xlsx"


def validate_inputs(filename: Optional[str], url: Optional[str]) -> tuple[Optional[str], Optional[dict]]:
    # Input validation
    if not filename and not url:
        console.print("[red]Error:[/red] You must provide either a filename or a URL!")
        raise typer.Exit(1)

    if filename and url:
        console.print("[yellow]Warning:[/yellow] Both filename and URL provided. Using URL and ignoring filename.")
        filename = None

    # Parse URL if provided
    url_info = None
    if url:
        url_info = validate_ridewithgps_url(url)
        console.print(
            "[yellow]Note:[/yellow] URL downloading is experimental and may not work "
            "with updated routes due to API restrictions."
        )

    return filename, url_info


def print_options(options: dict) -> None:
    if options["verbose"]:
        console.print("[blue]Running in verbose mode[/blue]")
    if options["debugging"]:
        console.print("[blue]DEBUG MODE[/blue]")

    features = []
    if options["island"]:
        features.append("include distance from last control")
    if options["hidedir"]:
        features.append("omit direction column")

    if features:
        console.print(f"[blue]Cuesheet will:[/blue] {', '.join(features)}")


def prepare_csv_file(filename: Optional[str], url_info: Optional[dict], verbose: bool) -> str:
    csv_filename = filename
    if url_info:
        csv_filename = download_route(url_info, verbose)

    # Ensure we have a valid CSV filename at this point
    if not csv_filename:
        console.print("[red]Error:[/red] No valid input file available")
        raise typer.Exit(1)

    return csv_filename


def cli():
    """Entry point for the CLI application."""
    app()


if __name__ == "__main__":
    app()
