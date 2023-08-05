r"""
.. currentmodule:: science_book.physics

==========================================
The Physics Module (:mod:`science_book.physics`)
==========================================

This module is used for physics calculations.  It includes physical constants (the
:mod:`~science_book.physics.constants` module) and functions to calculate phenomena such as
freefall, projectile motion, etc.

.. toctree::
    :caption: Submodules
    :maxdepth: 1
    :name: physics_module_contents

    constants
    mechanics
"""

from science_book.physics import constants, mechanics

__all__ = [
    "constants",
    "mechanics",
]
