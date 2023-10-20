import os
import yaml


__SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
__CACHED_FILE = os.path.join(__SCRIPT_DIR, "cached_versions.yml")


def load_cached_versions():
    with open(__CACHED_FILE, "r") as file:
        output = yaml.load(file, Loader=yaml.SafeLoader)
    return output or {}


def load_cached_version_info(repo_name, version, throw_on_missing=True):
    data = load_cached_versions()

    repo_info = data.get(repo_name, {})
    if version in repo_info:
        return repo_info[version]

    # if throw_on_missing:
    #     raise Exception(f"{repo_name}:{version} Not found!")
    return {"sha": None, "version": None, "commitish": None}

    return None


def update_cached_version(repo_name, version, sha, commitish):
    data = load_cached_versions()

    if repo_name not in data:
        data[repo_name] = {}

    repo_info = data[repo_name]
    repo_info[version] = dict(sha=sha, commitish=commitish)

    with open(__CACHED_FILE, "w") as file:
        yaml.dump(data, file, sort_keys=False)
