SHELL := /bin/bash
.PHONY: venv

venv:
	rm -rf venv
	python -m venv venv
	venv/Scripts/pip install -r requirements.txt
