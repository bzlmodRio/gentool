
import yaml

def load_cached_versions():
    with open('/home/pjreiniger/git/bzlmodRio/gentool/bazelrio_gentool/cached_versions.yml', 'r') as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


def load_cached_version_info(repo_name, version):
    data = load_cached_versions()

    repo_info = data[repo_name]
    for versions in repo_info:
        if versions['version'] == version:
            return versions

    raise Exception(f"{repo_name}:{version} Not found!")