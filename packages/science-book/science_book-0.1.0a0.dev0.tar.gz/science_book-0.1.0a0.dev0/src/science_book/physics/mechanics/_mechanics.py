# -*- coding: utf-8 -*-

import math

from science_book.physics.constants import g_0


def calculate_freefall_time(initial_height: float, gravity: float = g_0) -> float:
    """Calculates the time an object will spend in gravitational freefall.

    This function calculates the time an object spends in a uniform gravitational
    field with no air resistance or other external forces (i.e. no terminal velocity).

    Parameters
    ----------
    initial_height : float
        The height above the surface (in meters) from which the object is dropped.

    gravity : float, default = :data:`science_book.physics.constants.g_0`
        The gravitational acceleration toward the surface in m/s²

    Returns
    -------
    float
        The time, in seconds, that the object spends in gravitational freefall.

    Notes
    -----
    This corresponds to the classical Newtonian physics model where a body's position
    as a function of time can be modeled as:

    x(t) = x₀ + u₀t + ½a₀t²

    Under freefall, the initial velocity, u₀, is zero and the final position (relative
    to the initial height) is also zero.  The acceleration is a downward vector due
    only to gravity, meaning that a₀ = -g.  So the characteristic equation becomes:

    x(t) = x₀ - ½gt² = 0

    Rearranging, yields t = ±√(2 * x₀ / g).  The negative value is nonsensical, so it
    is ignored.

    Examples
    --------
    >>> # Standard Earth gravity
    >>> round(calculate_freefall_time(20), 4)
    2.0196

    >>> # Using gravity of Mars
    >>> round(calculate_freefall_time(20, gravity=3.72076), 4)
    3.2788
    """

    if initial_height < 0:
        raise ValueError("The initial height must be a positive value.")
    if gravity == 0 or gravity < 0:
        raise ValueError("The gravitational acceleration must be a positive value.")

    return math.sqrt(2.0 * initial_height / gravity)


def calculate_momentum(mass: float, velocity: float) -> float:
    return mass * velocity


def calculate_kinetic_energy(mass: float, velocity: float) -> float:
    return 0.5 * mass * velocity**2


def calculate_potential_energy(mass: float, height: float, gravity: float = g_0) -> float:
    return mass * height * gravity
