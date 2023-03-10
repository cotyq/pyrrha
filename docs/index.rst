.. pyrrha documentation master file, created by
   sphinx-quickstart on Mon Dec 14 17:41:09 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to pyrrha's documentation!
==================================


.. figure:: https://gitlab.com/dsklar/pyrrha/uploads/f6f763a9ce81995256a6de4809e898e2/image__24_.png
   :alt: pyrra


pyrrha is a tool for helping in the developement and testing of
Computational Mechanics methods.

This project is based in the Octave & C++ program called “Prometheus”,
developed by Carlos Gentile, that allows to generate templates for
programming Octave implementations of classical Computional Mechanics
methods. Inspired in these ideas, this project offers the ability to
generate python templates for the Finite Elements method, and tools for
evaluating the intermediate steps of its implementation.

The name pyrrha comes from Pyrrha, the wife of Deucalion (the son of
Prometheus ), who had a child out of wedlock with Zeus. She is basically
the daughter -in-law and niece of Prometheus (a link that is in some way
preserved between the original Prometheus application and this package).


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   source/api/modules.rst

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. contents::
   :depth: 3
..

Commands
========

Generate template from a base class
-----------------------------------

::

   pyrrha generate FiniteElement2D --output <file_name>

A ``<file_name>`` file will be created with the FiniteElement2D
template.

Test implementations
--------------------

Test class
~~~~~~~~~~

::

   pyrrha validate <file_name>

will validate the class defined in ``<file_name>`` against the correct
implementation.

Test class method
~~~~~~~~~~~~~~~~~

::

   pyrrha validate <file_name> --method <method_name>

will test only the ``<method_name>`` method of the class defined in
``<file_name>``, comparing it with the correct method implementation.

.. raw:: html

   <div>

Icons made by Darius Dan from www.flaticon.com

.. raw:: html

   </div>
