#!/bin/bash
#
# Push a release of sheepdog to `pypi` and generate the build artifact using
# bazel.
#
# Important, while this script currently takes the version number as an
# argument, it does not automatically update the `setup.py` file. The releaser
# must make those updates manually before running this script.

set -e

VERSION_NUMBER=

release::check_version_number_updated_in_setup() {
    grep -q "$VERSION_NUMBER" sheepdoge/__version__.py
    exit_code=$?

    if [ "$exit_code" -ne 0 ]
    then
        echo "Error: $VERSION_NUMBER not found in setup.py" >&2
        exit 2
    fi
}

release::build_sdist() {
    python setup.py sdist
}

release::build_bdist_wheel() {
    python setup.py bdist_wheel
}

release::upload_with_twine() {
    twine upload dist/*
}

release::push_git_tag() {
    git tag "$VERSION_NUMBER"
    git push origin --tags
}

release::build_binary() {
    make build
    echo '===== Upload `bazel-bin/sheepdoge.par` to the release on github ======'

    make sha256
    echo '===== Upload `sheepdoge.par.sha256` to the release on github ======'
}

release::run() {
    release::check_version_number_updated_in_setup
    release::build_sdist
    release::build_bdist_wheel
    release::upload_with_twine
    release::push_git_tag
    release::build_binary
}

release::cleanup() {
    [ -d "build" ] && rm -r build
    [ -d "dist" ] && rm -r dist
    [ -d "sheepdoge.egg-info" ] && rm -r sheepdoge.egg-info
}

trap 'release::cleanup' EXIT

if [ $# -lt 1 ]
then
    echo 'Must pass a version number' >&2
    exit 2
else
    VERSION_NUMBER="$1"
    release::run
fi
