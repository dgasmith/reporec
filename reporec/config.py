"""
Configuration for repo rep
"""

import os

__all__ = ["get_option"]

_globals = {}
_globals["github_token"] = os.environ.get("GITHUB_TOKEN", None)


def get_option(key):
    return _globals[key]


def set_option(key, value):
    _globals[key] = value
