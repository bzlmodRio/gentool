import json
from urllib.request import urlopen, Request


def download_url(url):
    print(f"Downloading from {url}")

    req = Request(url)
    with urlopen(req) as x:
        contents = x.read()

    return contents


def get_latest_tag(owner, repo):
    tags = json.loads(
        download_url(f"https://api.github.com/repos/{owner}/{repo}/tags").decode(
            "utf-8"
        )
    )

    return tags[0]["name"]


def split_tag(tag):
    if tag.startswith("v"):
        tag = tag[1:]

    parts = tag.split(".")
    year = parts[0]
    raw_version = ".".join(parts[1:])

    print("Before")
    print(year)
    print(raw_version)

    if "-" in year:
        hyphen_start = year.index("-")
        version = year[hyphen_start + 1 :] + "." + raw_version
        year = year[:hyphen_start]
    else:
        version = ".".join(parts[1:])

    return year, version


def update_vendor_dep(vendordep_path):
    with open(vendordep_path, "r") as f:
        contents = json.load(f)

    latest_url = contents["jsonUrl"]

    new_vendordep = download_url(latest_url)
    with open(vendordep_path, "wb") as f:
        f.write(new_vendordep)
