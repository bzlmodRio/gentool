import os
from bazelrio_gentool.utils import TEMPLATE_BASE_DIR


def generate_vendordep_raw_libs(module_directory, group):
    template_files = [
        "private/cpp/BUILD.bazel",
    ]

    render_templates(
        template_file,
        module_directory,
        os.path.join(TEMPLATE_BASE_DIR, "vendordeps"),
        group=group,
        visibility=f'["@{group.repo_name}//:__subpackages__"]',
    )
