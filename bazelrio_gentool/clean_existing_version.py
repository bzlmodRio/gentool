import os

def clean_existing_version(module_directory):
    module_directory = os.path.abspath(module_directory)

    DIR_BLACKLIST = [
        ".git",
        "bazel-bin",
        "bazel-out",
        "bazel-testlogs",
        "bazel-tests",
        "generate",
    ]

    for root, dirs, files in os.walk(module_directory):
        dirs[:] = [d for d in dirs if d not in DIR_BLACKLIST]
        dirs[:] = [d for d in dirs if not os.path.join(root, d).startswith(os.path.join(root, "generate_"))]

        for f in files:
            full_file = os.path.join(root, f).replace("\\", "/")
            if full_file.endswith("main.cpp") or full_file.endswith("Main.java"):
                continue
            if full_file.endswith("test.cpp") or full_file.endswith("Test.java"):
                continue
            if full_file.endswith("user.bazelrc"):
                continue
            os.remove(full_file)


