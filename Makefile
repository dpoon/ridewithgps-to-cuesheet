.PHONY: run require-var-%

.venv:
	pyenv install --skip-existing
	@`which poetry` &2>1 /dev/null || pip install --upgrade pip poetry setuptools
	pip install -r requirements.txt

require-var-%:
	@if [ -z '${${*}}' ]; then echo 'ERROR: variable $* not set' && exit 1; fi

convert-from-url: .venv require-var-URL
	poetry install --sync
	poetry run python script.py --url ${URL} --verbose
