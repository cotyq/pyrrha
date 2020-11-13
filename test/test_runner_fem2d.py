from pymetheus.impl.finite_element_2d_impl import FiniteElement2DImpl
from pymetheus.method import FiniteElement2D
from pymetheus.runner import Runner
from pymetheus.validators import DimensionValidator

import pytest


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
    _, impl = Runner.search_implementation(test_finite_element_2d)
    assert impl == FiniteElement2DImpl


def test_search_implementation_not_exists(test_finite_element_2d):
    # It receives a class without implementation
    with pytest.raises(NotImplementedError):
        Runner.search_implementation(DimensionValidator)


# def test_validate_class(test_finite_element_2d):
#     Runner.validate_class(test_finite_element_2d)
