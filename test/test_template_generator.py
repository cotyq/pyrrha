#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from pymetheus.template_generator import TemplateGenerator

from pymetheus.method import FiniteElement2D


@pytest.fixture
def test_template_generator():
    class TestTemplateGenerator(FiniteElement2D):
        TemplateGenerator.gen_template(FiniteElement2D)
        
    return TestTemplateGenerator

