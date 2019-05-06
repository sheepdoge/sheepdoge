load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

git_repository(
    name = "subpar",
    remote = "https://github.com/google/subpar",
    tag = "1.3.0"
)

git_repository(
    name = "io_bazel_rules_python",
    remote = "https://github.com/bazelbuild/rules_python.git",
    commit = "8b5d0683a7d878b28fffe464779c8a53659fc645"
)

load("@io_bazel_rules_python//python:pip.bzl", "pip_repositories", "pip_import")
pip_repositories()

pip_import(
    name = "sheepdoge",
    requirements = "//:requirements.txt",
)

load("@sheepdoge//:requirements.bzl", "pip_install")
pip_install()

pip_import(
    name = "sheepdoge_dev",
    requirements = "//:dev-requirements.txt",
)

load("@sheepdoge_dev//:requirements.bzl", "pip_install")
pip_install()
