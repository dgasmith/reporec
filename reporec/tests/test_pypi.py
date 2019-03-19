"""
Tests for the github API
"""

import pytest

import reporec

# Check if available token


def test_pypi():

    ret = reporec.pypi.get_downloads("opt_einsum")
    assert len(ret) > 1
    assert len(ret[0]) == 2
