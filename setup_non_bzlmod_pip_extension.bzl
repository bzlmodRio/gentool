load("@rules_python//python:pip.bzl", "pip_parse")

def setup_non_bzlmod_pip_extensions():
    pip_parse(
        name = "pip",
        requirements_lock = "@bzlmodrio-gentool//:requirements_lock.txt",
    )
