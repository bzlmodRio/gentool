import tempfile
import hashlib
from urllib.request import urlopen
import os

__DEFAULT_CACHE_DIRECTORY = os.path.join(tempfile.gettempdir(), "bazelrio_cache")
CACHE_DIRECTORY = os.path.join(os.path.expanduser("~"), "bzlmod_cache")
# print(f"Writing cache to {CACHE_DIRECTORY}")


def __download_and_cache(cached_file, url, fail_on_miss):
    if not os.path.exists(CACHE_DIRECTORY):
        os.mkdir(CACHE_DIRECTORY)

    print(f"Cache miss for {url}")
    try:
        url_result = urlopen(url)
    except:
        if fail_on_miss:
            raise
        return None

    if url_result.getcode() != 200:
        raise Exception(f"Could not grab '{url}'")

    data = url_result.read()

    # CTRE does a fake 404 page, that makes it seem like a valid 200 response. Treat this like a 404
    if b"html>" in data:
        message = f"Looks like a fake 404 happened for '{url}'"
        if fail_on_miss:
            raise Exception(message)
        print("  " + message)
        data = b""  # Cache an empty file, so we don't try to download it everytime
        sha256 = None
    else:
        sha256 = hashlib.sha256(data).hexdigest()

    with open(cached_file + ".raw", "wb") as f:
        f.write(data or "None")

    with open(cached_file, "w") as f:
        f.write(sha256)

    return sha256


def get_hash(url, fail_on_miss):
    cached_file = os.path.join(CACHE_DIRECTORY, os.path.basename(url) + ".sha256")
    if not os.path.exists(cached_file):
        return __download_and_cache(cached_file, url, fail_on_miss)

    with open(cached_file, "r") as f:
        data = f.read()
        return data
