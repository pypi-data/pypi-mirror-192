r"""
.. currentmodule:: science_book.physics.mechanics

======================================================
The Mechanics Module (:mod:`science_book.physics.mechanics`)
======================================================

.. autosummary::
   :toctree: generated/

    calculate_freefall_time
    calculate_momentum
    calculate_kinetic_energy
    calculate_potential_energy

"""

from ._mechanics import *

__all__ = [name for name in dir() if not name.startswith('_')]
