from abc import ABC, abstractmethod

import numpy as np

from oct2py import io as octave_io, octave

from .decorators import validation_classes
from .validators import DimensionValidator, ValueValidator


class Method(ABC):
    @classmethod
    @abstractmethod
    def get_initial_values(cls, seed=None):
        raise NotImplementedError()

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_pipeline(cls):
        raise NotImplementedError()


class FiniteElement2D(Method):
    # TODO agregar @final para evitar que lo pisen las heredadas
    def __init__(self):
        octave.addpath("./fem2d_octave")

    @classmethod
    def get_initial_values(cls, seed=None):
        """Create a dictionary containing random values to initialize the
        instances

        :param seed: seed for the random arrays/numbers generator.
        :return: dictionary with random values.
        """
        initial_values = {}
        octave_values = octave_io.loadmat("./fem2d_octave/data_system1.mat")

        n = len(octave_values["xnode"])
        initial_values["n_nodes"] = n

        initial_values["x_node"] = octave_values["xnode"]
        initial_values["neumann"] = octave_values["NEU"]
        initial_values["dirichlet"] = octave_values["DIR"]
        initial_values["robin"] = octave_values["ROB"]

        initial_values["icone"] = octave_values["icone"]
        initial_values["pun"] = octave_values["PUN"]
        initial_values["model"] = octave_values["model"]

        np.random.seed(seed)

        initial_values["K"] = np.random.uniform(size=(n, n))
        initial_values["C"] = np.random.uniform(size=(n, n))
        initial_values["F"] = np.random.uniform(size=(n, 1))

        return initial_values

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
            (cls.heat_neumann, ["F", "neumann", "x_node"]),
            (cls.heat_robin, ["K", "F", "robin", "x_node"]),
            (cls.heat_dirichlet, ["K", "F", "dirichlet"]),
        ]

    def run(self, n_nodes):
        k, c, f = self.heat_initialize(n_nodes)
        k, c, f = self.gen_system(k, c, f)
        f = self.gen_neumann()
        k, f = self.heat_robin()
        f = self.heat_pcond()
        k, f = self.heat_dirichlet()
        phi, q = self.heat_solve()
        return k, c, f, phi, q

    def gen_system(self, K, C, F, x_node, icone, model):
        K, C, F = octave.fem2d_heat_gen_system(
            K, C, F, x_node, icone, model, nout=3
        )
        return K, C, F

    def heat_pcond(self, F, x_node, icone, pun):
        F = octave.fem2d_heat_pcond(F, x_node, icone, pun)
        return F

    def heat_solve(self, K, C, F, x_node, icone, model):
        phi, q = octave.fem2d_heat_solve(K, C, F, x_node, icone, model, nout=2)
        return phi, q


class FiniteVolume2D(Method):
    pass


class FiniteDifferences(Method):
    pass
