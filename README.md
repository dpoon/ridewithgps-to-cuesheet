# ridewithgps-to-cuesheet
A converter for RideWithGPS Maps to Cuesheets for the BC Randonneurs

This converter was primarily written to save me time in creating routes, and eventually became popular enough that people started asking for it...

## Usage:

Tested with python install version in `.python-version` so you can use `pyenv install`.

Install poetry `pip install poetry`.

Fairly straightforward if using the command line, use `poetry run python script.py -h` to show help

As for now, the grab from URL is not working very well, so I recommend you use `poetry run python script.py -f PATH_TO_CSV.csv`

Common arguments are `-i` to show a running tally of distance since the last control
`-d` to hide the direction column if you don't intend on filling it out


### TODOS:

- Make this work with RideWithGPS APIs. Would be nice to just have to supply the slug
- Webservice?
