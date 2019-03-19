"""
Access Conda's REST API.
"""

import datetime
import collections
import requests
import pandas as pd


def get_downloads(package):
    """Gets total number of downloads per version
    """
    uri = "https://pypistats.org/api/packages/{}/overall".format(package)
    r = requests.get(uri)
    r.raise_for_status()


    ret = []
    for x in r.json()["data"]:
        if x["category"] == "without_mirrors":
            continue

        ret.append((x["date"], x["downloads"]))
    return ret


def build_table(package, old_data=None):
    """Builds a full table of data from Conda.
    """

    df = pd.DataFrame(get_downloads(package), columns=["timestamp", "downloads"])

    if old_data is not None:
        df = pd.concat([old_data, df], sort=False, ignore_index=True)

    return df
