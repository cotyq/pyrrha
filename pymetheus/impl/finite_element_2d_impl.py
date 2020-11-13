from oct2py import octave

from ..method import FiniteElement2D


class FiniteElement2DImpl(FiniteElement2D):
    def __init__(self):
        octave.addpath("./fem2d_octave")

    def heat_initialize(self, n_nodes):
        k, c, f = octave.fem2d_heat_initialize(n_nodes, nout=3)
        return k, c, f

    def heat_neumann(self, F, neumann, x_node):
        f = octave.fem2d_heat_neumann(F, neumann, x_node)
        return f

    def heat_robin(self, K, F, robin, x_node):
        k, f = octave.fem2d_heat_robin(K, F, robin, x_node, nout=2)
        return k, f

    def heat_dirichlet(self, K, F, dirichlet):
        k, f = octave.fem2d_heat_dirichlet(K, F, dirichlet, nout=2)
        return k, f
