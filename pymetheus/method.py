import numpy as np
import attr
from abc import ABC, abstractmethod


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
    def heat_initialize(self):
        pass

    @abstractmethod
    def heat_neumann(self):
        pass

    @abstractmethod
    def heat_robin(self):
        pass

    @abstractmethod
    def heat_dirichlet(self):
        pass

    def run(self):
        k, c, f = self.heat_initialize()
        k, c, f = self.gen_system(k, c, f)
        f = self.gen_neumann()
        k, f = self.heat_robin()
        f = self.heat_pcond()
        k, f = self.heat_dirichlet()
        phi, q = self.heat_solve()

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
