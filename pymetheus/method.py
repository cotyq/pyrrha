import numpy as np
from scipy.sparse import lil_matrix
import attr
from abc import ABC, abstractmethod, abstractproperty

from .decorators import validation_classes
from .validators import DimensionValidator, ValueValidator


class Method(ABC):
    @abstractmethod
    def get_random_values(self):
        raise NotImplementedError()

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    @abstractmethod
    def set_values(self, **kwargs):
        raise NotImplementedError()


@attr.s
class FiniteElement2D(Method):
    # TODO agregar @final para evitar que lo pisen las heredadas
    def __init__(self, attributes=None):
        if attributes:  # attributes is a dictionary containing the attributes
            self.set_attributes(attributes)

    @classmethod
    def get_random_values(cls, seed=None):
        """ Create a dictionary containing random values to initialize the
        instances

        :param seed: seed for the random arrays/numbers generator.
        :return: dictionary with random values.
        """
        np.random.seed(seed)

        r_values = {}

        r_n_nodes = np.random.randint(4, 8)
        dirichlet_size = np.random.randint(0, r_n_nodes)
        neumann_size = np.random.randint(0, r_n_nodes)
        robin_size = np.random.randint(0, r_n_nodes)

        r_values['n_nodes'] = r_n_nodes
        r_values['x_node'] = np.random.rand(r_n_nodes, 2)
        r_values['dirichlet'] = np.random.rand(dirichlet_size, 2)
        r_values['neumann'] = np.random.rand(neumann_size, 2)
        r_values['robin'] = np.random.rand(robin_size, 2)
        r_values['K'] = lil_matrix((r_n_nodes, r_n_nodes))
        r_values['C'] = lil_matrix((r_n_nodes, r_n_nodes))
        r_values['F'] = lil_matrix((r_n_nodes, 1))

        return r_values

    @abstractmethod
    @validation_classes([DimensionValidator])
    def heat_initialize(self, **kwargs):
        pass

    @abstractmethod
    @validation_classes([ValueValidator])
    def heat_neumann(self, **kwargs):
        pass

    @abstractmethod
    @validation_classes([ValueValidator])
    def heat_robin(self, **kwargs):
        pass

    @abstractmethod
    @validation_classes([ValueValidator])
    def heat_dirichlet(self, **kwargs):
        pass

    def run(self):
        # k, c, f = self.heat_initialize()
        # k, c, f = self.gen_system(k, c, f)
        # f = self.gen_neumann()
        # k, f = self.heat_robin()
        # f = self.heat_pcond()
        # k, f = self.heat_dirichlet()
        # phi, q = self.heat_solve()
        pass

    def gen_system(self):
        pass

    def heat_pcond(self):
        pass

    def heat_solve(self):
        pass

    def set_attributes(self, attributes):
        """ Set class attributes according to the provided dictionary

        :param attributes: dictionary that contains the attributes
        """
        for key, val in attributes.items():
            setattr(self, key, val)


class FiniteVolume2D(Method):
    pass


class FiniteDifferences(Method):
    pass
