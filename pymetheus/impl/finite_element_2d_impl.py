from pymetheus.method import FiniteElement2D
from oct2py import octave


class FiniteElement2DImpl(FiniteElement2D):
    def __init__(self):
        octave.addpath('./fem2d_octave')

    def heat_initialize(self, nnodes):
        k, c, f = octave.fem2d_heat_initialize(nnodes, nout=3)
        return k, c, f

    def heat_neumann(self, F, NEU, xnode):
        f = octave.fem2d_heat_neumann(F, NEU, xnode)
        return f

    def heat_robin(self, K, F, ROB, xnode):
        k, f = octave.fem2d_heat_robin(K, F, ROB, xnode, nout=2)
        return k, f

    def heat_dirichlet(self, K, F, DIR):
        k, f = octave.fem2d_heat_dirichlet(K, F, DIR, nout=2)
        return k, f
