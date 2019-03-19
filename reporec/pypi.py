"""
Access Conda's REST API.
"""

import collections
import datetime

import pandas as pd
import requests


def get_downloads(package):
    """Gets total number of downloads per version
    """
    uri = "https://pypistats.org/api/packages/{}/overall".format(package)
    r = requests.get(uri)
    r.raise_for_status()

    mirrors = []
    no_mirrors = []
    for x in r.json()["data"]:
        if x["category"] == "without_mirrors":
            no_mirrors.append((x["date"], x["downloads"]))
        else:
            mirrors.append((x["date"], x["downloads"]))

    return (mirrors, no_mirrors)


def build_table(package, old_data=None):
    """Builds a full table of data from Conda.
    """

    mirrors, no_mirrors = get_downloads(package)
    mirrors = pd.DataFrame(mirrors, columns=["timestamp", "downloads_with_mirrors"])
    no_mirrors = pd.DataFrame(no_mirrors, columns=["timestamp", "downloads"])

    df = no_mirrors.merge(mirrors, how="outer", on="timestamp")

    if old_data is not None:
        df = pd.concat([old_data, df], sort=False, ignore_index=True)

    return df
