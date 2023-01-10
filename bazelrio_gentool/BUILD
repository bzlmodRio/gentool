load("@pip//:requirements.bzl", "requirement")

py_library(
    name = "bazelrio_gentool",
    srcs = glob(["**/*.py"]),
    visibility = ["//visibility:public"],
    deps = [
        requirement("jinja2")
    ]
)