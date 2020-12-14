# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

from pyrrha.constants import IMPLEMENTATIONS
from pyrrha.impl.finite_element_2d_impl import FiniteElement2DImpl
from pyrrha.method import FiniteElement2D
from pyrrha.runner import Runner

import pytest


@pytest.fixture
def generic_class():
    class GenericClass:
        ...

    return GenericClass


@pytest.fixture
def test_finite_element_2d():
    class TestFiniteElement2D(FiniteElement2D):
        def heat_initialize(self, n_nodes):
            ...

        def heat_neumann(self, F, neumann, x_node):
            ...

        def heat_robin(self, K, F, robin, x_node):
            ...

        def heat_dirichlet(self, K, F, dirichlet):
            ...

    return TestFiniteElement2D


def test_search_implementation_exists(test_finite_element_2d):
    runner = Runner(test_finite_element_2d, IMPLEMENTATIONS)
    assert runner.method_impl == FiniteElement2DImpl


def test_search_implementation_not_exists(generic_class):
    with pytest.raises(NotImplementedError):
        # Create a Runner with a programmed class which is not present in the
        # IMPLEMENTATIONS dictionary
        Runner(generic_class, IMPLEMENTATIONS)


def test_validate_class(test_finite_element_2d):
    # runner = Runner()
    ...
