# ridewithgps-to-cuesheet
A converter for RideWithGPS Maps to Cuesheets for the BC Randonneurs

This converter was primarily written to save me time in creating routes, and eventually became popular enough that people started asking for it...

## Prereqs

You need uv to install dependencies. See [uv documentation](https://docs.astral.sh/uv/)

## Usage:

Tested with python install version in `.python-version` so you can use `uv sync`.

Fairly straightforward if using the command line, use `uv run script.py --help` to show help

`uv run poe convert-route to run the script`

Common arguments are `--island` to show a running tally of distance since the last control
`--hidedir` to hide the direction column if you don't intend on filling it out


### TODOS:

- module-ize
- Webservice?
