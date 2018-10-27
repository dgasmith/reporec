"""
Access Conda's REST API.
"""

import datetime
import collections
import requests
import pandas as pd


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

    if old_data is not None:
        df = pd.concat([old_data, df])

    return df
