"""
Tests for the conda API
"""

import pytest
import requests

import reporec


def test_conda_downloads():

    ret = reporec.conda.get_downloads("conda-forge", "qcengine")
    assert len(ret) > 1
    assert ret[0].keys() == {"timestamp", "version", "downloads"}


def test_conda_downloads_error():

    with pytest.raises(requests.exceptions.HTTPError):
        ret = reporec.conda.get_downloads("molssi", "cookiemonster")
