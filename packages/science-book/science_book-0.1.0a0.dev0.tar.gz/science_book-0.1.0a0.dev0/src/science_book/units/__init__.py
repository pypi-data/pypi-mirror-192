r"""

.. currentmodule:: science_book.units

==========================================
Units of Measurement (:mod:`science_book.units`)
==========================================

science_book expressly endorses the SI unit system.  In this system, there are seven
standard units of measurement (which are derived using physical constants).  These
seven base units and the quantity they measure are:

1. second (s) - time,
2. meter or metre (m) - length,
3. kilogram (kg) - mass,
4. ampere (A) - electric current,
5. kelvin (K) - temperature,
6. mole (mol) - amount of substance, and
7. candela (cd) - luminous intensity

SI prefixes are provided for indicating order-of-magnitude of a base unit.

This module is influenced by SciPy_'s ability to make unit conversions in calculations.
Special thanks to those contributors.

.. _SciPy: https://docs.scipy.org/doc/

.. autosummary::
   :toctree: generated/

"""


from ._conversion_factors import *
from ._prefixes import *


__all__ = [name for name in dir() if not name.startswith('_')]
