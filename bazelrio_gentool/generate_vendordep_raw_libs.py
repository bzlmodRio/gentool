import os
from bazelrio_gentool.utils import render_template, write_file, TEMPLATE_BASE_DIR


def generate_vendordep_raw_libs(module_directory, group):

    template_files = [
        "private/cpp/BUILD.bazel",
    ]

    for tf in template_files:
        template_file = os.path.join(TEMPLATE_BASE_DIR, "vendordeps", tf + ".jinja2")
        output_file = os.path.join(module_directory, tf)
        render_template(
            template_file,
            output_file,
            group=group,
            visibility=f'["@{group.repo_name}//:__subpackages__"]',
        )
