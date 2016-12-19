bootstrap:
	pip install -r requirements.txt

lint:
	flake8 src test

test:
	PYTHONPATH=src python -m unittest discover -s test -v

cover:
	PYTHONPATH=src coverage run --source=src -m unittest discover -s test -v
	coverage report -m


.PHONY: bootstrap lint test
