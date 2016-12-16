bootstrap:
	pip install -r requirements.txt

lint:
	flake8 *.py

test:
	python -m unittest discover -s test -v


.PHONY: bootstrap lint test
