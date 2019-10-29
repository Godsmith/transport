.PHONY: venv

venv:
	rm -rf venv
	python -m venv venv
	venv/Scripts/pip install -r requirements.txt

test:
    pytest

test-coverage:
    pytest --cov=transport --cov-report html
