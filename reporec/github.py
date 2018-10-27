"""
Access GitHub's REST API.
"""

import json
import pandas as pd
import requests

from . import config

_base = "https://api.github.com/"


def _build_header():
    """Builds headers with a GitHub token if available
    """
    token = config.get_option("github_token")
    if token is None:
        return {}
    else:
        return {"Authorization": "token " + token}


def get_api(*paths):
    """Generic GitHub API getter
    """
    path = _base + "/".join(paths)
    r = requests.get(path, headers=_build_header())
    r.raise_for_status()

    return r.json(), r.headers


def get_views(org, repo):
    """Obtains the view data for a give repository
    """
    return get_api("repos", org, repo, "traffic", "views")[0]["views"]


def get_clones(org, repo):
    """Obtains the clone data for a give repository
    """

    return get_api("repos", org, repo, "traffic", "clones")[0]["clones"]


def build_table(org, repo, old_data=None):

    view = pd.DataFrame(get_views(org, repo))
    clones = pd.DataFrame(get_clones(org, repo))

    df = view.merge(clones, how="outer", on="timestamp", suffixes=("_view", "_clone"))

    if old_data is not None:
        df = pd.concat([old_data, df], sort=False).drop_duplicates("timestamp")

    return df