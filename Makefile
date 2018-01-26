install:
	pipenv install --dev

install2:
	pipenv install --two --dev

clean:
	pipenv --rm
	rm Pipfile.lock || true

typecheck:
	pipenv run bash -c "which mypy >/dev/null && mypy ./sheepdoge"

lint: typecheck
	pipenv run pylint ./sheepdoge
	pipenv check

unit_tests:
	pipenv run nose2 -s tests/unit

integration_tests:
	./tests/integration/run_integration_tests.sh

interactive_integration_tests:
	./tests/integration/run_integration_tests.sh --interactive
