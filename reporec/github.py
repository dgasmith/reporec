"""
Access GitHub's Python API.
"""

import json
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

    return r.json(), r.headers


def get_views(org, repo):
    """Obtains the view data for a give repository
    """
    return get_api("repos", org, repo, "traffic", "views")


def get_clones(org, repo):
    """Obtains the clone data for a give repository
    """

    return get_api("repos", org, repo, "traffic", "clones")
