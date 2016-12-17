bootstrap:
	pip install -r requirements.txt

lint:
	flake8 **/*.py

test:
	PYTHONPATH=src python -m unittest discover -s test -v


.PHONY: bootstrap lint test
