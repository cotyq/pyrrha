# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

import numpy as np

from pyrrha.impl.finite_element_2d_impl import FiniteElement2DImpl
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


def test_run_fe2d():
    iv = FiniteElement2D.get_initial_values()
    ins = FiniteElement2DImpl()

    k, c, f, phi, q = ins.run(
        iv["n_nodes"],
        iv["x_node"],
        iv["icone"],
        iv["model"],
        iv["dirichlet"],
        iv["neumann"],
        iv["robin"],
        iv["pun"],
    )

    assert np.all(np.isclose(iv["phi"].toarray(), phi.toarray()))
