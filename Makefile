.PHONY: install test lint format clean

install:
	pip install -e ".[test]"

test:
	pytest tests/ -v

lint:
	# Add linting later (ruff/black)
	pass

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
