init:
	pip install pip pipenv
	pipenv lock
	pipenv install --dev

lint:
	pipenv run flake8 happiestbaby_api
	pipenv run pydocstyle happiestbaby_api
	pipenv run pylint happiestbaby_api

typing:
	pipenv run mypy --ignore-missing-imports happiestbaby_api

test:
	pipenv run pytest

test-unit:
	pipenv run pytest tests/unit -v

test-integration:
	pipenv run pytest tests/integration -v -m "integration"

test-no-integration:
	pipenv run pytest -m "not integration" -v

test-coverage:
	pipenv run pytest --cov=happiestbaby_api --cov-report=html --cov-report=term-missing

test-coverage-unit:
	pipenv run pytest tests/unit --cov=happiestbaby_api --cov-report=html --cov-report=term-missing

test-fast:
	pipenv run pytest -m "not slow and not integration" -v

test-credentials:
	pipenv run pytest tests/integration -v -m "requires_credentials"

test-watch:
	pipenv run pytest-watch

clean-test:
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

publish:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg simplisafe_python.egg-info/
