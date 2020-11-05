import numpy as np
import attr
from abc import ABC, abstractmethod

from pymetheus.decorators import validation_classes
from pymetheus.validators import DimensionValidator, ValueValidator


class Method(ABC):
    # @abstractmethod
    # def get_template(cls):
    #     raise NotImplementedError()

    @abstractmethod
    def get_random_values(cls):
        raise NotImplementedError()

    @abstractmethod
    def run(self):
        raise NotImplementedError()

    # @abstractmethod
    # def generate_report(self):
    #     raise NotImplementedError()


@attr.s(auto_attribs=True)
class FiniteElement2D(Method):
    @classmethod
    def get_random_values(cls, seed=None):
        return {"k": ..., "v": ..., "c": ...}

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

    # def run(self):
    #     k, c, f = self.heat_initialize()
    #     k, c, f = self.gen_system(k, c, f)
    #     f = self.gen_neumann()
    #     k, f = self.heat_robin()
    #     f = self.heat_pcond()
    #     k, f = self.heat_dirichlet()
    #     phi, q = self.heat_solve()

    def gen_system(self):
        pass

    def heat_pcond(self):
        pass

    def heat_solve(self):
        pass


class FiniteVolume2D(Method):
    pass


class FiniteDifferences(Method):
    pass
