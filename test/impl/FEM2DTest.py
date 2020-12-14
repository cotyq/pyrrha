# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

import numpy as np

from pyrrha.method import FiniteElement2D


class FiniteElement2DTemplate(FiniteElement2D):
    def heat_dirichlet(self, K, F, dirichlet):
        pass

    def heat_initialize(self, n_nodes):
        C = np.zeros((n_nodes, n_nodes))
        F = np.zeros((n_nodes, 1))
        K = np.zeros((n_nodes, n_nodes))
        return K, C, F

    def heat_neumann(self, F, neumann, x_node):
        return 1

    def heat_robin(self, K, F, robin, x_node):
        return (1, 2)
