load("@bzlmodrio-gentool-pip//:requirements.bzl", "requirement")

py_library(
    name = "bazelrio_gentool",
    srcs = glob(["**/*.py"]),
    visibility = ["//visibility:public"],
    deps = [
        requirement("jinja2"),
        requirement("pyyaml"),
    ],
)
