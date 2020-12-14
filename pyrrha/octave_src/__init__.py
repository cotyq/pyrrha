# This file is part of the
#   Pyrrha Project (https://gitlab.com/dsklar/pyrrha).
# Copyright (c) 2020, Diego Sklar, Constanza Quaglia, Franco Matzkin
# License: MIT
#   Full Text: https://gitlab.com/dsklar/pyrrha/-/blob/master/LICENSE

"""Octave source files."""

import os
import pathlib

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))
FEM2D_PATH = str(PATH / "fem2d_octave")


def correct_indexes(arr, name):
    """Convert Python array indexes to Octave indexes.

    Parameters
    ----------
    arr : numpy.array
        Array to convert.
    name : str
        Array identifier, that determines which columns to convert.

    Returns
    -------
    numpy.array
        Converted array
    """
    out = arr.copy()
    if name == "icone":
        out[:, 0:3] += 1
        out[out[:, 3] != -1, 3] += 1
    elif name == "dirichlet":
        out[:, 0] += 1
    elif name in ["neumann", "robin"]:
        out[:, 0:2] += 1

    return out
