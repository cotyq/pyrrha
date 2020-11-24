import pytest


@pytest.fixture
def finite_element_2D_template():
    return """class FiniteElement2DTemplate(FiniteElement2D):

    heat_dirichlet(self, K, F, dirichlet):
        pass

    heat_initialize(self, n_nodes):
        pass

    heat_neumann(self, F, neumann, x_node):
        pass

    heat_robin(self, K, F, robin, x_node):
        pass
"""


def test_generate_fe2d(finite_element_2D_template, script_runner):
    ret = script_runner.run("pyrrha", "generate", "FiniteElement2D")
    assert ret.success
    assert ret.stdout == finite_element_2D_template
    assert ret.stderr == ""


def test_generate_empty_base(finite_element_2D_template, script_runner):
    ret = script_runner.run("pyrrha", "generate")
    error_msg = "Missing required arguments: base"
    assert not ret.success
    assert error_msg in ret.stderr
    assert ret.stdout == ""
