load("@bzlmodrio-gentool-pip//:requirements.bzl", "requirement")
load("@rules_python//python:defs.bzl", "py_binary", "py_library")

py_library(
    name = "bazelrio_gentool",
    srcs = glob(["**/*.py"]),
    data = ["cached_versions.yml"] + glob(["templates/**"]),
    visibility = ["//visibility:public"],
    deps = [
        requirement("jinja2"),
        requirement("pyyaml"),
    ],
)

py_binary(
    name = "create_vendordep_library",
    srcs = ["create_vendordep_library.py"],
    deps = [
        ":bazelrio_gentool",
    ],
)
