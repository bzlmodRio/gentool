load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "publish",
    srcs = ["publish.py"],
    visibility = ["//visibility:public"],
    deps = [
        "@bzlmodrio-gentool//bazelrio_gentool",
    ],
)
