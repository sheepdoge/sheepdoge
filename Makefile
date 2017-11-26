install:
	pipenv install --dev

lint:
	pipenv run pylint ./sheepdoge
	pipenv check

unit_tests:
	pipenv run nose2 -s tests/unit

integration_tests:
	./tests/integration/run_integration_tests.sh

interactive_integration_tests:
	./tests/integration/run_integration_tests.sh --interactive
