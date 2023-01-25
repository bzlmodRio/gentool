
import yaml


__CACHED_FILE = '/home/pjreiniger/git/bzlmodRio/gentool/bazelrio_gentool/cached_versions.yml'

def load_cached_versions():
    with open(__CACHED_FILE, 'r') as file:
        return yaml.load(file, Loader=yaml.SafeLoader)


def load_cached_version_info(repo_name, version, throw_on_missing=True):
    data = load_cached_versions()

    repo_info = data[repo_name]
    if version in repo_info:
        return repo_info[version]

    if throw_on_missing:
        raise Exception(f"{repo_name}:{version} Not found!")

    return None


def update_cached_version(repo_name, version, sha, commitish):
    data = load_cached_versions()

    if repo_name not in data:
        data[repo_name] = {}

    repo_info = data[repo_name]
    repo_info[version] = dict(sha=sha, commitish=commitish)
    
    with open(__CACHED_FILE, 'w') as file:
        yaml.dump(data, file)