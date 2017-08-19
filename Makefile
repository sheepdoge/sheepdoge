lint:
	pylint ./sheepdoge

unit_tests:
	nose2 -s tests/unit

integration_tests:
	./tests/integration/run_integration_tests.sh

interactive_integration_tests:
	./tests/integration/run_integration_tests.sh --interactive

release:
	./release.sh
