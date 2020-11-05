import unittest

from method import FiniteElement2D
from impl.finite_element_2d_impl import FiniteElement2DImpl
from runner import Runner
from validators import DimensionValidator


class TestFiniteElement2D(FiniteElement2D):
    def heat_initialize(self):
        ...

    def heat_neumann(self):
        ...

    def heat_robin(self):
        ...

    def heat_dirichlet(self):
        ...


class TestRunner(unittest.TestCase):
    def test_search_implementation_exists(self):
        impl = Runner.search_implementation(TestFiniteElement2D)
        self.assertIs(impl, FiniteElement2DImpl)

    def test_search_implementation_not_exists(self):
        impl = Runner.search_implementation(DimensionValidator)  # Le pasamos una clase sin implementacion en impl
        self.assertIsNone(impl)

    def test_validate_class(self):
        Runner.validate_class(TestFiniteElement2D)
