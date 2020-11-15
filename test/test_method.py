from pyrrha.method import FiniteElement2D

import pytest


@pytest.fixture
def test_initial_values():
    return FiniteElement2D.get_initial_values()


@pytest.fixture
def test_pipeline():
    return FiniteElement2D.get_pipeline()


def test_pipeline_parameters(test_initial_values, test_pipeline):
    """
    Checks if pipeline keys returned by get_pipeline
    are present in the dictionary returned by get_random_values
    :return:
    """
    pipeline_keys = {key for _, keys in test_pipeline for key in keys}
    assert pipeline_keys.issubset(test_initial_values.keys())
