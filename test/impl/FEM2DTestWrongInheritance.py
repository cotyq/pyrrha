import numpy as np


class FiniteElement2DTemplate:
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
