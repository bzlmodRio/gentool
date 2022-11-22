
import re

class BaseDependency:
    def __init__(self, maven_url, group_id, artifact_name, version, repo_name, fail_on_hash_miss):
        self.maven_url = maven_url
        self.group_id = group_id
        self.artifact_name = artifact_name
        self.version = version
        self.repo_name = repo_name
        self.fail_on_hash_miss = fail_on_hash_miss


    def get_archive_name(self, suffix=""):
        # print(self.artifact_name, self.version)
        group_underscore = self.group_id.replace(".", "_").lower()

        # Having a year in the bazel name makes things tricky downstream. Remove it.
        year_search = re.findall("20[0-9]{2}", group_underscore)
        if year_search:
            group_underscore = group_underscore.replace(year_search[0], "")

        archive_name = f"bazelrio_{group_underscore}_{self.artifact_name.lower()}"
        if suffix:
            archive_name += f"_{suffix}"

        return archive_name

    def _get_url(self, file_extension, suffix):
        group_as_folder = self.group_id.replace(".", "/")
        url = f"{self.maven_url}/{group_as_folder}/{self.artifact_name}/{self.version}/{self.artifact_name}-{self.version}"
        if suffix:
            url += f"-{suffix}"
        url += f"{file_extension}"

        return url