dev_requirements_prefix := dev-requirements
requirements_prefix := requirements

$(requirements_prefix).txt: $(requirements_prefix).in
	pip-compile --output-file $(requirements_prefix).txt $(requirements_prefix).in

$(dev_requirements_prefix).txt: $(dev_requirements_prefix).in
	pip-compile --output-file $(dev_requirements_prefix).txt $(dev_requirements_prefix).in

static_dockerfile := Dockerfile.dev
static_image_name := mattjmcnaughton/sheepdoge-dev:latest

build_static_image: $(requirements_prefix).txt $(dev_requirements_prefix).txt $(static_dockerfile)
	docker build -t $(static_image_name) -f $(static_dockerfile) .

lint: build_static_image
	docker run -t --rm -v $$(pwd):/src $(static_image_name) sh -c "pylint ./sheepdoge"

typecheck: build_static_image
	docker run -t --rm -v $$(pwd):/src $(static_image_name) sh -c "mypy ./sheepdoge"

static: lint typecheck

unit_test: $(requirements_prefix).txt $(dev_requirements_prefix).txt
	bazel test //tests/unit/...

integration_test:
	./tests/integration/run_integration_tests.sh

tests: unit_test integration_test

check: static tests

build: $(requirements_prefix).txt $(dev_requirements_prefix).txt
	bazel build //:sheepdoge.par

sha256: build
	sha256sum bazel-bin/sheepdoge.par > sheepdoge.par.sha256

run: build
	bazel run //:sheepdoge

clean:
	rm $(requirements_prefix).txt || true
	rm $(dev_requirements_prefix).txt || true
	rm sheepdoge.par.sha256 || true
	bazel clean
