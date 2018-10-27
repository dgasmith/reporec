"""
Tests for the github API
"""

import pytest
import requests

import reporec

def test_github_views():

    ret = reporec.github.get_views("dgasmith", "opt_einsum")
    assert len(ret) > 1
    assert ret[0].keys() == {"timestamp", "count", "uniques"}

def test_github_clones():

    ret = reporec.github.get_clones("dgasmith", "opt_einsum")
    assert len(ret) > 1
    assert ret[0].keys() == {"timestamp", "count", "uniques"}

def test_github_downloads_error():

    with pytest.raises(requests.exceptions.HTTPError):
        ret = reporec.github.get_clones("dgasmith", "cookiemonster")