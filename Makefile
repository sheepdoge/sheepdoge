install:
	pipenv install --dev

install2:
	pipenv install --two --dev

clean:
	pipenv --rm
	rm Pipfile.lock || true

lint:
	pipenv run pylint ./sheepdoge
	pipenv check

unit_tests:
	pipenv run nose2 -s tests/unit

integration_tests:
	./tests/integration/run_integration_tests.sh

interactive_integration_tests:
	./tests/integration/run_integration_tests.sh --interactive
