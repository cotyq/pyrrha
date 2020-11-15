from abc import ABC, abstractmethod

from pyrrha.method import FiniteElement2D
from pyrrha.template_generator import TemplateGenerator

import pytest


@pytest.fixture
def test_generic_class():
    class GenericClass(ABC):
        @abstractmethod
        def method_template_without_params(self):
            ...

        @abstractmethod
        def method_template_with_params(self, a, b):
            ...

        @classmethod
        def class_method(cls):
            ...

        def instance_method(self):
            ...

    return GenericClass


def test_template_generator(test_generic_class):
    target_template = """
class GenericClassTemplate(GenericClass):

    method_template_with_params(self, a, b):
        pass

    method_template_without_params(self):
        pass
"""
    template = TemplateGenerator.gen_template(test_generic_class)
    assert template.strip() == target_template.strip()


def test_template_generator_finite_element_2d():
    target_template = """
class FiniteElement2DTemplate(FiniteElement2D):

    heat_dirichlet(self, K, F, dirichlet):
        pass

    heat_initialize(self, n_nodes):
        pass

    heat_neumann(self, F, neumann, x_node):
        pass

    heat_robin(self, K, F, robin, x_node):
        pass
"""
    template = TemplateGenerator.gen_template(FiniteElement2D)
    assert template.strip() == target_template.strip()
