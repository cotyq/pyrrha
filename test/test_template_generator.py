# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

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
from pyrrha.method import GenericClass


class GenericClassTemplate(GenericClass):

    def method_template_with_params(self, a, b):
        pass

    def method_template_without_params(self):
        pass
"""
    template = TemplateGenerator.gen_template(test_generic_class)
    assert template.strip() == target_template.strip()


def test_template_generator_finite_element_2d():
    target_template = """
from pyrrha.method import FiniteElement2D


class FiniteElement2DTemplate(FiniteElement2D):

    def heat_dirichlet(self, K, F, dirichlet):
        pass

    def heat_initialize(self, n_nodes):
        pass

    def heat_neumann(self, F, neumann, x_node):
        pass

    def heat_robin(self, K, F, robin, x_node):
        pass
"""
    template = TemplateGenerator.gen_template(FiniteElement2D)
    assert template.strip() == target_template.strip()
