class BaseDependencyWriterHelper:
    def __init__(
        self,
        repo_name,
        version,
        sha,
        url_base,
        needs_stripped_prefix=False,
        old_release_style=False,
    ):
        self.repo_name = repo_name
        self.version = version
        self.sha = sha
        self.url_base = url_base
        self.needs_stripped_prefix = needs_stripped_prefix
        self.old_release_style = old_release_style

        self.sanitized_version = version.replace("+", "-")

        self.local_path = f"../../../rules/{self.repo_name}"

    def get_repository_url(self):
        archive_name = self.__cleanup_archive_name()
        if self.old_release_style:
            return f"{self.url_base}/{archive_name}/archive/refs/tags/{self.version}.tar.gz"
        return f"{self.url_base}/{archive_name}/releases/download/{self.version}/{archive_name}-{self.version}.tar.gz"

    def __cleanup_archive_name(self):
        archive_name = self.repo_name
        if archive_name == "bazel_skylib":
            archive_name = archive_name.replace("_", "-")

        archive_name = archive_name.replace("bzlmodrio", "bzlmodRio")

        return archive_name

    def local_module_override(self):
        if self.use_local_version:
            return f"""
local_path_override(
    module_name = "{self.repo_name}",
    path = "../../{self.repo_name}",
)"""
        return ""

    def http_archive(self, indent_num, maybe, native):
        indent = " " * indent_num
        native_text = "native." if native else ""
        if native:
            raise

        output = f"{indent}"
        if maybe:
            output += f"maybe(\n{indent}    {native_text}http_archive,"
        else:
            output += "http_archive("

        strip_prefix = (
            f'{indent}    strip_prefix = "{self.repo_name}-{self.version}",\n'
            if self.needs_stripped_prefix
            else ""
        )

        output += f"""
{indent}    name = "{self.repo_name}",
{indent}    sha256 = "{self.sha}",
{strip_prefix}{indent}    url = "{self.get_repository_url()}",
{indent})"""

        return output

    def module_dep(self):
        return f'bazel_dep(name = "{self.repo_name}", version = "{self.sanitized_version}")'


class BaseLocalDependencyWriterHelper(BaseDependencyWriterHelper):
    def __init__(self, use_local_version, **kwargs):
        BaseDependencyWriterHelper.__init__(self, **kwargs)
        self.use_local_version = use_local_version

    def maybe_local_repository(self):
        if self.use_local_version:
            return self.local_repository_override()
        return ""

    def local_repository_override(self, indent_num=0, maybe=False, native=False):
        indent = " " * indent_num
        native_text = "native." if native else ""
        output = f"{indent}"
        if maybe:
            output += f"maybe(\n{indent}    {native_text}local_repository,"
        else:
            output += "local_repository("

        output += f"""{indent}    name = "{self.repo_name}",
{indent}    path = "{self.local_path}",
{indent})"""
        return output

    def download_repository(self, num_indent, native=False, maybe=False):
        if self.use_local_version:
            return self.local_repository_override(
                num_indent, maybe=maybe, native=native
            )
        return self.http_archive(indent_num=num_indent, maybe=maybe, native=native)
