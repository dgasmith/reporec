"""
Tests for the github API
"""

import pytest
import requests

import reporec

# Check if available token


@pytest.mark.xfail(reason="Requires token authentication")
def test_github_views():

    ret = reporec.github.get_views("dgasmith", "opt_einsum")
    assert len(ret) > 1
    assert ret[0].keys() == {"timestamp", "count", "uniques"}


@pytest.mark.xfail(reason="Requires token authentication")
def test_github_clones():

    ret = reporec.github.get_clones("dgasmith", "opt_einsum")
    assert len(ret) > 1
    assert ret[0].keys() == {"timestamp", "count", "uniques"}


def test_github_downloads_error_403():
    # A RuntimeError is raised when a repo exists and the API call returns
    # a 403 due to lack of a Personal Access Token
    with pytest.raises(RuntimeError):
        ret = reporec.github.get_clones("dgasmith", "opt_einsum")


def test_github_downloads_error():
    # This repo doesn't exist so an HTTPError is raised
    with pytest.raises(requests.exceptions.HTTPError):
        ret = reporec.github.get_clones("dgasmith", "cookiemonster")
