# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

"""Public module."""
from oct2py import octave

from ..method import FiniteElement2D
from ..octave_src import correct_indexes


class FiniteElement2DImpl(FiniteElement2D):
    """Class to instance FiniteElement2D.

    class to implement a specific Numerical Method.
    """

    def __init__(self):
        """Add path to run the octave code implementations.

        method inherited from FiniteElement2d Class
        """
        super().__init__()

    def heat_initialize(self, n_nodes):
        """Initialize the matrix and vector of the system.

        Parameters
        ----------
        n_nodes : int
                number of mesh noodes.

        Returns
        -------
        matrix k and matrix c with n_nodes rows and n_nodes columns and vector
        f with n_nodes rows.
        """
        k, c, f = octave.fem2d_heat_initialize(n_nodes, nout=3)
        return k, c, f

    def heat_neumann(self, F, neumann, x_node):
        """Apply the Neumann condition.

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
        modified f vector
        """
        neumann_mod = correct_indexes(neumann, "neumann")
        f = octave.fem2d_heat_neumann(F, neumann_mod, x_node)
        return f

    def heat_robin(self, K, F, robin, x_node):
        """Apply the Robin condition.

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
        modified k maxtrix and f vector
        """
        robin_mod = correct_indexes(robin, "robin")
        k, f = octave.fem2d_heat_robin(K, F, robin_mod, x_node, nout=2)
        return k, f

    def heat_dirichlet(self, K, F, dirichlet):
        """Apply the Dirichlet condition.

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
        modified k maxtrix and f vector
        """
        dirichlet_mod = correct_indexes(dirichlet, "dirichlet")
        k, f = octave.fem2d_heat_dirichlet(K, F, dirichlet_mod, nout=2)
        return k, f
