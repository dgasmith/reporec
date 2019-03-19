"""
Tests for the github API
"""

import pytest

import reporec

# Check if available token


def test_pypi():

    ret = reporec.pypi.get_downloads("opt_einsum")
    print(ret)
    assert len(ret) > 1
    assert ret[0].keys() == {"timestamp", "count", "uniques"}
