from pymetheus.method import FiniteElement2D
from pymetheus.template_generator import TemplateGenerator

import pytest


@pytest.fixture
def test_template_generator():
    class TestTemplateGenerator(FiniteElement2D):
        TemplateGenerator.gen_template(FiniteElement2D)

    return TestTemplateGenerator
