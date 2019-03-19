"""
Tests for the github API
"""

import pytest

import reporec

# Check if available token


def test_pypi():

    ret = reporec.pypi.get_downloads("opt_einsum")
    assert len(ret) == 2
    assert len(ret[0][0]) == 2
