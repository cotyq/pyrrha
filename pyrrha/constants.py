# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

"""Constants definitions."""

from .impl.finite_element_2d_impl import FiniteElement2DImpl
from .method import FiniteElement2D

IMPLEMENTATIONS = {FiniteElement2D: FiniteElement2DImpl}
