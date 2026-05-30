.PHONY: setup lint

setup:
	pip install pre-commit ruff
	pre-commit install
	pre-commit install --hook-type pre-push

lint:
	ruff check .
