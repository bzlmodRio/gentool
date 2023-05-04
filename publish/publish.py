import os
from bazelrio_gentool.generate_json import generate_json
from bazelrio_gentool.deps.dependency_container import DependencyContainer


def main():
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    registry_location = os.path.join(SCRIPT_DIR, "..", "..", "..", "bazel-central-registry")

    version = "1.0.1"
    year = "2023"
    group = DependencyContainer(
        "bzlmodrio-gentool", version, year, "https://frcmaven.wpi.edu/release"
    )

    module_template = os.path.join(SCRIPT_DIR, "module_config.jinja2")
    module_json_template = os.path.join(SCRIPT_DIR, "module_config.json.jinja2")

    os.chdir(SCRIPT_DIR)
    generate_json(registry_location, group, module_json_template, module_template)


if __name__ == "__main__":
    """
    bazel run //publish --enable_bzlmod
    """
    main()
