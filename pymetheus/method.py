from abc import ABC, abstractmethod

import attr

import numpy as np

import oct2py as oct

from .decorators import validation_classes
from .validators import DimensionValidator, ValueValidator


class Method(ABC):
    @classmethod
    @abstractmethod
    def get_random_values(cls):
        raise NotImplementedError()

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_pipeline(cls):
        raise NotImplementedError()


@attr.s
class FiniteElement2D(Method):
    # TODO agregar @final para evitar que lo pisen las heredadas

    @classmethod
    def get_random_values(cls, seed=None):
        """Create a dictionary containing random values to initialize the
        instances

        :param seed: seed for the random arrays/numbers generator.
        :return: dictionary with random values.
        """
        r_values = oct.io.loadmat("../fem2d_octave/data_system1.mat")
        n = len(r_values["xnode"])
        np.random.seed(seed)

        r_values["K"] = np.random.uniform(size=(n, n))
        r_values["C"] = np.random.uniform(size=(n, n))
        r_values["F"] = np.random.uniform(size=(n, 1))

        # r_values['K'] = lil_matrix((r_n_nodes, r_n_nodes))
        # r_values['C'] = lil_matrix((r_n_nodes, r_n_nodes))
        # r_values['F'] = lil_matrix((r_n_nodes, 1))

        # r_values = {}

        # r_n_nodes = np.random.randint(4, 8)
        # dirichlet_size = np.random.randint(0, r_n_nodes)
        # neumann_size = np.random.randint(0, r_n_nodes)
        # robin_size = np.random.randint(0, r_n_nodes)

        # r_values['n_nodes'] = r_n_nodes
        # r_values['x_node'] = np.random.rand(r_n_nodes, 2)
        # r_values['dirichlet'] = np.random.rand(dirichlet_size, 2)
        # r_values['neumann'] = np.random.rand(neumann_size, 2)
        # r_values['robin'] = np.random.rand(robin_size, 2)

        # r_values['icone'] = None
        # r_values['pun'] = None
        # r_values['model'] = None

        return r_values

    @abstractmethod
    @validation_classes([DimensionValidator])
    def heat_initialize(self, n_nodes):
        raise NotImplementedError()

    @abstractmethod
    @validation_classes([ValueValidator])
    def heat_neumann(self, F, neumann, x_node):
        raise NotImplementedError()

    @abstractmethod
    @validation_classes([ValueValidator])
    def heat_robin(self, K, F, robin, x_node):
        raise NotImplementedError()

    @abstractmethod
    @validation_classes([ValueValidator])
    def heat_dirichlet(self, K, F, dirichlet):
        raise NotImplementedError()

    @classmethod
    def get_pipeline(cls):
        return [
            (cls.heat_initialize, ["n_nodes"]),
            # (cls.gen_system, ['K', 'C', 'F', 'x_node', 'icone', 'model']),
            (cls.heat_neumann, ["F", "neumann", "x_node"]),
            (cls.heat_robin, ["K", "F", "robin", "x_node"]),
            # (cls.heat_pcond, ['F', 'x_node', 'icone', 'pun']),
            (cls.heat_dirichlet, ["K", "F", "dirichlet"]),
            # (cls.heat_solve, ['K', 'C', 'F', 'x_node', 'icone', 'model']),
        ]

    def run(self):
        # k, c, f = self.heat_initialize()
        # k, c, f = self.gen_system(k, c, f)
        # f = self.gen_neumann()
        # k, f = self.heat_robin()
        # f = self.heat_pcond()
        # k, f = self.heat_dirichlet()
        # phi, q = self.heat_solve()
        pass

    def gen_system(self, K, C, F, x_node, icone, model):
        pass

    def heat_pcond(self, F, x_node, icone, pun):
        pass

    def heat_solve(self, K, C, F, x_node, icone, model):
        pass


class FiniteVolume2D(Method):
    pass


class FiniteDifferences(Method):
    pass
