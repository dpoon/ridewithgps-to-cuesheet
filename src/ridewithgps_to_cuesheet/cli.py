"""CLI interface for ridewithgps-to-cuesheet converter.

This module provides a command-line interface for converting RideWithGPS route files
to BC Randonneurs style cue sheets. It supports both local CSV files and direct URL downloads.
"""

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.parse import ParseResult, urlparse

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
logger = logging.getLogger("ridewithgps-to-cuesheet")


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
    show_direction_column: bool = typer.Option(
        False, "--show-direction-column", "-sdc", help="Hide the direction column"
    ),
    two_decimals_precision: bool = typer.Option(
        False, "--two-decimals-precision", "-tdp", help="Use two decimal places for distances"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    """Convert RideWithGPS routes to BC Randonneurs style cuesheets.

    You must provide either a CSV file (--filename) or a RideWithGPS URL (--url).
    """
    file_path, url_info = validate_inputs(filename, url)
    inputs_path, outputs_path = Path(csv_directory), Path(xlsx_directory)

    if verbose:
        console.print("[cyan]Running in verbose mode[/cyan]")

        class ConsoleHandler(logging.Handler):
            def emit(self, record: logging.LogRecord) -> None:
                # colours from https://rich.readthedocs.io/en/stable/appendix/colors.html?highlight=color
                if record.levelno <= logging.DEBUG:
                    console.print(f"[medium_purple4]{record.msg}[/medium_purple4]")
                elif record.levelno <= logging.WARNING:
                    console.print(f"[slate_blue3]{record.msg}[/slate_blue3]")

        console_handler = ConsoleHandler()
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)
        logger.setLevel(logging.DEBUG)

    features = []
    if island:
        features.append("include distance from last control")
    if show_direction_column:
        features.append("show direction column")

    if features:
        console.print(f"[cyan]Cuesheet will:[/cyan] {', '.join(features)}")

    excel_filename = generate_output_filename(url_info, file_path, output)
    console.print(f"[cyan]Output file:[/cyan] {excel_filename}")

    try:
        inputs_path.mkdir(parents=True, exist_ok=True)
        outputs_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        console.print(f"[red]Error creating directories:[/red] {e}")
        raise typer.Exit(1)

    csv_filename = prepare_csv_file(file_path, url_info, outputs_path, verbose)
    run_conversion(
        input_csv=str(csv_filename),
        output_xlsx=excel_filename,
        options=Converter.GenerationOptions(
            include_distance_from_last=island,
            two_decimals_precision=two_decimals_precision,
            hide_direction=not show_direction_column,
            verbose=verbose,
        ),
    )
    organize_output_files(excel_filename, inputs_path, outputs_path, file_path)

    console.print("[green]🎉 Process completed successfully![/green]")


def validate_csv_file(value: str) -> str:
    if not value.endswith(".csv"):
        raise typer.BadParameter(f"File must be a CSV file, got: {value}")

    path = Path(value)
    if not path.exists():
        raise typer.BadParameter(f"File does not exist: {value}")

    return value


@dataclass(frozen=True)
class RideWithGpsUrl:
    url: str
    parsed: ParseResult
    id: str


def validate_ridewithgps_url(value: str) -> RideWithGpsUrl:
    RIDE_WITH_GPS_URL_PREFIX = "https://ridewithgps.com/routes/"
    if not value.startswith(RIDE_WITH_GPS_URL_PREFIX) or value[len(RIDE_WITH_GPS_URL_PREFIX) :] == "":
        raise typer.BadParameter(f"Not a valid RideWithGPS URL. Must start with {RIDE_WITH_GPS_URL_PREFIX}")

    parsed = urlparse(value)
    route_id = parsed.path.split("/")[-1]

    if not route_id or not route_id.isdigit():
        raise typer.BadParameter("URL must contain a valid route ID")

    return RideWithGpsUrl(
        url=value,
        parsed=parsed,
        id=route_id,
    )


def download_route(url_info: RideWithGpsUrl, outputs_path: Path, verbose: bool = False) -> Path:
    """Download route data from RideWithGPS URL."""
    download_url = url_info.url.replace(url_info.id, f"{url_info.id}.csv")
    output_file = outputs_path / f"downloaded_cues_for_{url_info.id}.csv"

    if verbose:
        console.print(f"[cyan]Downloading from:[/cyan] {download_url}")
        console.print(f"[cyan]Saving to:[/cyan] {output_file}")

    try:
        response = requests.get(download_url, timeout=30)
        response.raise_for_status()

        with open(output_file.absolute(), "wb") as tmp_file:
            tmp_file.write(response.content)

        if verbose:
            console.print("[green]✓[/green] Download completed successfully")

        return output_file

    except requests.RequestException as e:
        console.print(f"[red]Error downloading route:[/red] {e}")
        raise typer.Exit(1)


def run_conversion(input_csv: str, output_xlsx: str, options: Converter.GenerationOptions) -> None:
    console.print("[cyan]Reading CSV file...[/cyan]")

    try:
        values_array = read_csv_to_array(input_csv)
        console.print("[cyan]Generating Excel file...[/cyan]")
        Converter.generate_excel(
            filename=output_xlsx,
            csv_values=values_array,
            opts=options,
        )

        console.print("[green]✓[/green] Conversion completed successfully!")

    except Exception as e:
        console.print(f"[red]Error during conversion:[/red] {e}")
        raise typer.Exit(1)


def organize_output_files(
    excel_filename: str, inputs_path: Path, outputs_path: Path, csv_file_path: Optional[Path] = None
) -> None:
    """Move generated files to appropriate directories."""
    try:
        # Move Excel file to outputs directory
        output_path = outputs_path / excel_filename
        if Path(excel_filename).exists():
            Path(excel_filename).rename(output_path)
            console.print(f"[green]✓[/green] Output saved to: {output_path}")

        if csv_file_path:
            is_csv_in_input_dir = inputs_path in csv_file_path.parents
            if not is_csv_in_input_dir:
                moved_csv_path = inputs_path / csv_file_path.name
                if csv_file_path.exists():
                    csv_file_path.rename(moved_csv_path)
                    console.print(f"[green]✓[/green] Input CSV moved to: {moved_csv_path}")

    except OSError as e:
        console.print(f"[yellow]Warning:[/yellow] Could not organize files: {e}")


def generate_output_filename(
    url_info: Optional[RideWithGpsUrl] = None, csv_file_path: Optional[Path] = None, custom_output: Optional[str] = None
) -> str:
    if custom_output:
        return custom_output
    elif url_info:
        return f"{url_info.id}_cues.xlsx"
    elif csv_file_path:
        return f"{csv_file_path.stem}_cues.xlsx"
    logger.warning(
        f"No output filename provided, will {'overwrite' if Path('output_cues.xlsx').exists() else 'default to'} 'output_cues.xlsx'"
    )
    return "output_cues.xlsx"


def validate_inputs(filename: Optional[str], url: Optional[str]) -> tuple[Optional[Path], Optional[RideWithGpsUrl]]:
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

    return Path(filename) if filename else None, url_info


def prepare_csv_file(
    file_path: Optional[Path], url_info: Optional[RideWithGpsUrl], outputs_path: Path, verbose: bool
) -> Path:
    csv_filename = file_path
    if url_info:
        csv_filename = download_route(url_info, outputs_path, verbose)

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
