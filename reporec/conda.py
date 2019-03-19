"""
Access Conda's REST API.
"""

import collections
import datetime

import pandas as pd
import requests


def get_downloads(username, package):
    """Gets total number of downloads per version
    """
    uri = "https://api.anaconda.org/package/{}/{}/files".format(username, package)
    r = requests.get(uri)
    r.raise_for_status()

    ret = collections.defaultdict(lambda: 0)
    for packet in r.json():
        ret[packet["version"]] += packet["ndownloads"]

    dt = datetime.datetime.utcnow().strftime("%Y-%M-%dT%H:%M:%SZ")
    ret = [{"timestamp": dt, "version": k, "downloads": v} for k, v in ret.items()]
    return ret


def build_table(username, package, old_data=None):
    """Builds a full table of data from Conda.
    """

    df = pd.DataFrame(get_downloads(username, package))
    df["username"] = username

    if old_data is not None:
        df = pd.concat([old_data, df], sort=False, ignore_index=True)

    return df
