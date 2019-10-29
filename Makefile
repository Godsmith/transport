.PHONY: venv

venv:
	rm -rf venv
	python -m venv venv
	venv/Scripts/pip install -r requirements.txt

test:
	pytest tests

test-coverage:
	pytest tests --cov=transport --cov-report html
