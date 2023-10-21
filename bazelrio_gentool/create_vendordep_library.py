import argparse
import os
from bazelrio_gentool.utils import (
    render_template,
    render_templates,
    TEMPLATE_BASE_DIR,
)
from bazelrio_gentool.auto_update_utils import download_url
from bazelrio_gentool.load_vendordep_dependency import vendordep_dependency
from bazelrio_gentool.generate_shared_files import get_bazel_dependencies


def create_vendordep_library(vendordep, library_name, base_output_directory):
    print(base_output_directory)
    if not os.path.exists(base_output_directory):
        os.makedirs(base_output_directory)

    os.chdir(base_output_directory)

    fail_on_hash_miss = False
    has_static_libraries = False
    # subprocess.check_call(["git", "init", library_name])

    output_directory = os.path.join(base_output_directory)

    template_files = [
        "generate/auto_update.py",
        "generate/BUILD.bazel",
        "generate/generate.py",
        "generate/publish.py",
        "generate/WORKSPACE",
    ]

    render_templates(
        template_files,
        output_directory,
        os.path.join(TEMPLATE_BASE_DIR, "create_vendordep_library"),
        library_name=library_name,
        bazel_dependencies=get_bazel_dependencies(),
    )

    local_vendor_dep_file = os.path.join(
        output_directory, "generate", "vendor_dep.json"
    )
    with open(local_vendor_dep_file, "wb") as f:
        f.write(download_url(vendordep))

    group = vendordep_dependency(
        library_name,
        local_vendor_dep_file,
        None,
        fail_on_hash_miss,
        has_static_libraries,
    )

    render_template(
        os.path.join(
            "create_vendordep_library", "generate/get_library_dependencies.py.jinja2"
        ),
        os.path.join(
            output_directory, "generate", f"get_{library_name}_dependencies.py"
        ),
        library_name=library_name,
        fail_on_hash_miss=fail_on_hash_miss,
        has_static_libraries=has_static_libraries,
        group=group,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vendordep", required=True)
    parser.add_argument("--library_name", required=True)
    parser.add_argument("--output_directory", required=True)
    args = parser.parse_args()

    create_vendordep_library(args.vendordep, args.library_name, args.output_directory)


if __name__ == "__main__":
    main()
