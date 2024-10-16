import os


def clean_existing_version(
    module_directory, extra_dir_blacklist=None, file_blacklist=None, force_tests=False
):
    module_directory = os.path.abspath(module_directory).replace("\\", "/")

    DIR_BLACKLIST = [
        ".git",
        "bazel-bin",
        "bazel-out",
        "bazel-testlogs",
        "bazel-tests",
        "generate",
        "robot-cpp",
        "robot-java",
    ]
    if extra_dir_blacklist:
        DIR_BLACKLIST.extend(extra_dir_blacklist)

    file_blacklist = file_blacklist or []
    file_blacklist += [
        ".git",  # for submodules, where the .git is a file
        "MODULE.bazel.lock",
        ".buildbuddy-auth.rc",
        "tests/MODULE.bazel.lock",
        "tests/.buildbuddy-auth.rc",
    ]
    file_blacklist = [
        os.path.join(module_directory, x).replace("\\", "/") for x in file_blacklist
    ]

    for root, dirs, files in os.walk(module_directory):
        dirs[:] = [d for d in dirs if d not in DIR_BLACKLIST]
        dirs[:] = [
            d
            for d in dirs
            if not os.path.join(root, d).startswith(os.path.join(root, "generate_"))
        ]

        for f in files:
            full_file = os.path.join(root, f).replace("\\", "/")
            if full_file.endswith("main.cpp") or full_file.endswith("Main.java"):
                continue
            if full_file.endswith("test.cpp") or full_file.endswith("Test.java"):
                continue
            if full_file.endswith("user.bazelrc"):
                continue
            if file_blacklist and full_file in file_blacklist:
                continue
            if not force_tests:
                if f"{module_directory}/tests/cpp" in full_file and full_file.endswith(
                    "BUILD.bazel"
                ):
                    continue
                if (
                    f"{module_directory}/tests/java" in full_file
                    and full_file.endswith("BUILD.bazel")
                ):
                    continue
            os.remove(full_file)
