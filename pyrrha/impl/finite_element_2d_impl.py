from oct2py import octave

from ..method import FiniteElement2D
from ..octave_src import correct_indexes


class FiniteElement2DImpl(FiniteElement2D):
    def __init__(self):
        super().__init__()

    def heat_initialize(self, n_nodes):
        k, c, f = octave.fem2d_heat_initialize(n_nodes, nout=3)
        return k, c, f

    def heat_neumann(self, F, neumann, x_node):
        neumann_mod = correct_indexes(neumann, "neumann")
        f = octave.fem2d_heat_neumann(F, neumann_mod, x_node)
        return f

    def heat_robin(self, K, F, robin, x_node):
        robin_mod = correct_indexes(robin, "robin")
        k, f = octave.fem2d_heat_robin(K, F, robin_mod, x_node, nout=2)
        return k, f

    def heat_dirichlet(self, K, F, dirichlet):
        dirichlet_mod = correct_indexes(dirichlet, "dirichlet")
        k, f = octave.fem2d_heat_dirichlet(K, F, dirichlet_mod, nout=2)
        return k, f
