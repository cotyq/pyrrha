# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

"""Public module."""
import os
from abc import ABC, abstractmethod

import numpy as np

from oct2py import io as octave_io, octave

from .octave_src import FEM2D_PATH, correct_indexes


class Method(ABC):
    """Abstract Class to implement Numerical Method.

    class inherited from ABC
    """

    @classmethod
    @abstractmethod
    def get_initial_values(cls, seed=None):
        """Abstract method to initialize the instances with initial values.

        Parameters
        ----------
        seed : int
               optional seed for the random arrays/numbers generator.

        Returns
        -------
        dictionary with random values.
        """
        ...

    @abstractmethod
    def run(self):
        """Abstract method to run all steps of the numerical method.

        Returns
        -------
        vector with phi solution.
        """
        ...

    @classmethod
    @abstractmethod
    def get_pipeline(cls):
        """Abstract method to get pipeline."""
        ...


class FiniteElement2D(Method):
    """Class to instance Method.

    class to define a specific Numerical Method.
    """

    def __init__(self):
        """Add path to run the octave code implementations."""
        octave.addpath(FEM2D_PATH)

    @classmethod
    def get_initial_values(cls, seed=None):
        """Create a dictionary containing random values array.

        :param seed: seed for the random arrays/numbers generator.
        :return: dictionary with random value.
        """
        initial_values = {}

        octave_values = octave_io.loadmat(
            os.path.join(FEM2D_PATH, "data_test.mat")
        )

        n = len(octave_values["xnode"])
        initial_values["n_nodes"] = n

        initial_values["x_node"] = octave_values["xnode"]

        initial_values["neumann"] = np.array(octave_values["NEU"])

        initial_values["dirichlet"] = octave_values["DIR"]
        initial_values["robin"] = octave_values["ROB"]

        initial_values["icone"] = octave_values["icone"]
        initial_values["pun"] = octave_values["PUN"]
        initial_values["model"] = octave_values["model"]
        initial_values["phi"] = octave_values["PHI"]

        np.random.seed(seed)

        initial_values["K"] = np.random.uniform(size=(n, n))
        initial_values["C"] = np.random.uniform(size=(n, n))
        initial_values["F"] = np.random.uniform(size=(n, 1))

        return initial_values

    @abstractmethod
    def heat_initialize(self, n_nodes):
        """Abstract method to initialize the matrix and vector of the system.

        Parameters
        ----------
        n_nodes : int
                number of mesh noodes.

        Returns
        -------
        matrix K with n_nodes rows and n_nodes columns and vector F with
        n_nodes rows.
        """
        raise ...

    @abstractmethod
    def heat_neumann(self, F, neumann, x_node):
        """Abstract method to apply the Neumann condition.

        The Neumann conditions are applied to modify the F vector of de system
        based in data Neumman matrix.

        Parameters
        ----------
        F : float array
                F vector of the system.
        neumann : float matrix
                data Neumann matrix.
        x_node : float matrix
                mesh nodes coordinates.

        Returns
        -------
        modified F vector
        """
        raise ...

    @abstractmethod
    def heat_robin(self, K, F, robin, x_node):
        """Abstract method to apply the Robin condition.

        The Robin conditions are applied to modify the K matrix and F vector
        of de system based in data Robin matrix.

        Parameters
        ----------
        K : float matrix
                K matrix of the system.
        F : float array
                F vector of the system.
        robin : float matrix
                data Robin matrix.
        x_node : float matrix
                mesh nodes coordinates.

        Returns
        -------
        modified K maxtrix and F vector
        """
        raise ...

    @abstractmethod
    def heat_dirichlet(self, K, F, dirichlet):
        """Abstract method to apply the Dirichlet condition.

        The Dirichlet conditions are applied to modify the K matrix and F
        vector of de system based in data Dirichlet matrix.

        Parameters
        ----------
        K : float matrix
                K matrix of the system.
        F : float array
                F vector of the system.
        dirichlet : float matrix
                data dirichlet matrix.

        Returns
        -------
        modified K maxtrix and F vector
        """
        raise ...

    @classmethod
    def get_pipeline(cls):
        """Return tuple of implemmented method with their parameters."""
        return [
            (cls.heat_initialize, ["n_nodes"]),
            (cls.heat_neumann, ["F", "neumann", "x_node"]),
            (cls.heat_robin, ["K", "F", "robin", "x_node"]),
            (cls.heat_dirichlet, ["K", "F", "dirichlet"]),
        ]

    def run(
        self, n_nodes, x_node, icone, model, dirichlet, neumann, robin, pun
    ):
        """Run all steps of the numerical method.

        Parameters
        ----------
        n_nodes : int
                number of mesh noodes.
        x_node : float matrix
                mesh nodes coordinates.
        icone : int matrix
                mesh connectivity elements.
        model : dictionary
                constants of the physical model.
        dirichlet : float matrix
                data dirichlet matrix.
        neumann : float matrix
                data Neumann matrix.
        robin : float matrix
                data Robin matrix.
        pun: float matrix
                heat source puntual data matrix

        Returns
        -------
        k : float matrix
                final diffusion matrix.
        c : float matrix
                final mass matrix.
        f : float vector
                final model independent vector.
        phi : float vector
                model temperature solution.
        q : float matrix
                model flux solution.
        """
        k, c, f = self.heat_initialize(n_nodes)
        k, c, f = self.gen_system(k, c, f, x_node, icone, model)
        f = self.heat_neumann(f, neumann, x_node)
        k, f = self.heat_robin(k, f, robin, x_node)
        f = self.heat_pcond(f, x_node, icone, pun)
        k, f = self.heat_dirichlet(k, f, dirichlet)
        phi, q = self.heat_solve(k, c, f, x_node, icone, model)
        return k, c, f, phi, q

    def gen_system(self, K, C, F, x_node, icone, model):
        """Assembling elementary contribution.

        Parameters
        ----------
        K : float matrix
                K diffusion matrix of the system.
        C : float matrix
                C mass matrix of the system.
        F : float array
                F vector of the system.
        x_node : float matrix
                mesh nodes coordinates.
        icone : int matrix
                mesh connectivity elements.
        model : dictionary
                constants of the physical model.

        Returns
        -------
        K : float matrix
                final diffusion matrix.
        C : float matrix
                final mass matrix.
        F : float vector
                final model independent vector.
        """
        icone_mod = correct_indexes(icone, "icone")
        K, C, F = octave.fem2d_heat_gen_system(
            K, C, F, x_node, icone_mod, model, nout=3
        )
        return K, C, F

    def heat_pcond(self, F, x_node, icone, pun):
        """Apply point source.

        Parameters
        ----------
        F : float array
                F vector of the system.
        x_node : float matrix
                mesh nodes coordinates.
        icone : int matrix
                mesh connectivity elements.
        pun: float matrix
                heat source puntual data matrix.

        Returns
        -------
        F : float vector
                model independent vector.
        """
        icone_mod = correct_indexes(icone, "icone")
        F = octave.fem2d_heat_pcond(F, x_node, icone_mod, pun)
        return F

    def heat_solve(self, K, C, F, x_node, icone, model):
        """Solve the direct system equations.

        Parameters
        ----------
        K : float matrix
                K diffusion matrix of the system.
        C : float matrix
                C mass matrix of the system.
        F : float array
                F vector of the system.
        x_node : float matrix
                mesh nodes coordinates.
        icone : int matrix
                mesh connectivity elements.
        model : dictionary
                constants of the physical model.

        Returns
        -------
        phi : float vector
                model temperature solution.
        q : float matrix
                model flux solution.
        """
        icone_mod = correct_indexes(icone, "icone")
        phi, q = octave.fem2d_heat_solve(
            K, C, F, x_node, icone_mod, model, nout=2
        )
        return phi, q
