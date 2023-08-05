r"""
.. currentmodule:: science_book.physics.constants

====================================================
Physical Constants (:mod:`science_book.physics.constants`)
====================================================

Value-Defined Constants
=======================

These constants are defined expressly by value.  Most of them are defined by the 2019 redefinition of SI base units.

===========================  ===================================================================================
``c``                        speed of light in vacuum, m/s
``speed_of_light``           speed of light in vacuum, m/s
``delta_cs``                 hyperfine transition frequency of the caesium-133 atom :math:`{\Delta\nu}_{Cs}`, Hz
``hyperfine_transition``     hyperfine transition frequency of the caesium-133 atom :math:`{\Delta\nu}_{Cs}`, Hz
``e``                        elementary charge, C
``elementary_charge``        elementary charge, C
``charge_of_electron``       elementary charge, C
``G``                        Newtonian constant of gravitation (big-G), m³/(kg⋅s²)
``gravitational_constant``   Newtonian constant of gravitation (big-G), m³/(kg⋅s²)
``big_G``                    Newtonian constant of gravitation (big-G), m³/(kg⋅s²)
``h``                        the Planck constant :math:`h`, J/Hz or J⋅s
``planck``                   the Planck constant :math:`h`, J/Hz or J⋅s
``k``                        Boltzmann constant :math:`k`, kg⋅m²⋅K⁻¹·s⁻² or J/K
``boltzmann``                Boltzmann constant :math:`k`, kg⋅m²⋅K⁻¹·s⁻² or J/K
``k_cd``                     luminous efficacy of monochromatic radiation of frequency 540 THz (defined), lm/W.
``luminous_efficacy``        luminous efficacy of monochromatic radiation of frequency 540 THz (defined), lm/W.
``m_e``                      electron mass :math:`m_e`, kg
``electron_mass``            electron mass :math:`m_e`, kg
``m_p``                      proton mass :math:`m_p`, kg
``proton_mass``              proton mass :math:`m_p`, kg
``m_n``                      neutron mass :math:`m_n`, kg
``neutron_mass``             neutron mass :math:`m_n`, kg
``m_u``                      atomic mass constant :math:`m_u`, kg
``atomic_mass``              atomic mass constant :math:`m_u`, kg
``N_A``                      Avogadro constant :math:`N_A`, mol⁻¹
``Avogadro``                 Avogadro constant :math:`N_A`, mol⁻¹
``g_0``                      standard Earth gravity, m/s²
``standard_gravity``         standard Earth gravity, m/s²
===========================  ===================================================================================

Example
-------

Calculating the mass of Earth

>>> from science_book.physics.constants import gravitational_constant, standard_gravity
>>>
>>> radius_of_earth = 6.378e6  # meters
>>> mass_of_earth = radius_of_earth**2 * standard_gravity / gravitational_constant
>>>
>>> print(f"{mass_of_earth:.3e}")
5.977e+24


Derived Constants
=================

These constants are typically defined by an equation using other defined quantities (such as :math:`c` or :math:`\pi`).

============================  ===========================================================================
``mu_0``                      magnetic constant (vacuum permeability) :math:`\mu_0`, kg⋅m⋅s⁻²·A⁻² or N/A²
``magnetic_constant``         magnetic constant (vacuum permeability) :math:`\mu_0`, kg⋅m⋅s⁻²·A⁻² or N/A²
``c_1``                       first radiation constant :math:`c_1`, W⋅m²
``first_rad_constant``        first radiation constant :math:`c_1`, W⋅m²
``c_2``                       second radiation constant :math:`c_2`, m⋅K
``second_rad_constant``       second radiation constant :math:`c_2`, m⋅K
``F``                         Faraday constant, C/mol
``faraday``                   Faraday constant, C/mol
``h_bar``                     reduced Planck constant (:math:`\hbar \equiv h / 2 \pi`), J/Hz or J⋅s
``reduced_planck_constant``   reduced Planck constant (:math:`\hbar \equiv h / 2 \pi`), J/Hz or J⋅s
``R``                         molar gas constant, J⋅mol⁻¹⋅K⁻¹
``gas_constant``              molar gas constant, J⋅mol⁻¹⋅K⁻¹
``Z_0``                       characteristic impedance of vacuum :math:`Z_0`, Ω
``characteristic_impedance``  characteristic impedance of vacuum :math:`Z_0`, Ω
``sigma``                     Stefan-Boltzmann constant :math:`\sigma`, W⋅m⁻²⋅K⁻⁴
``stefan_boltzmann``          Stefan-Boltzmann constant :math:`\sigma`, W⋅m⁻²⋅K⁻⁴
``epsilon_0``                 electric constant (vacuum permittivity) :math:`{\varepsilon}_0`, F/m
``electric_constant``         electric constant (vacuum permittivity) :math:`{\varepsilon}_0`, F/m
``alpha``                     fine-structure constant :math:`\alpha` (dimensionless)
``fine_structure``            fine-structure constant :math:`\alpha` (dimensionless)
``k_e``                       Coulomb's constant :math:`k_e`, N⋅m²⋅c⁻²
``coulomb``                   Coulomb's constant :math:`k_e`, N⋅m²⋅c⁻²
``a_0``                       Bohr radius :math:`a_0`, m
``bohr_radius``               Bohr radius :math:`a_0`, m
``R_infinity``                Rydberg constant :math:`R_{\infty}`, m⁻¹
``rydberg``                   Rydberg constant :math:`R_{\infty}`, m⁻¹
``Ry``                        Rydberg unit of energy, J
============================  ===========================================================================

Example
-------

Calculating the heat flux from the sun:

>>> from science_book.physics.constants import stefan_boltzmann
>>>
>>> temperature_sun = 5800  # kelvin
>>> heat_flux = stefan_boltzmann * temperature_sun**4  # W/m**2
>>>
>>> print(f"{heat_flux:.2e}")
6.42e+07

Equations for Defining Derived Constants
========================================

This section shows the equations for defining those physical constants that may be derived from other, value-defined
constants.  The values shown for these data correspond to the CODATA 2018 data set.

The Magnetic Constant :math:`\mu_0`
-----------------------------------

While the currently accepted term for this quantity is the magnetic constant, it has also been called the *constant of
vacuum permeability* in the past.

.. math::
    \begin{equation}\label{magnetic_constant}
        \begin{split}
            {\mu}_0 & \equiv 4 \pi \times 10^{-7} \quad \mathrm{H \cdot m^{-1}} \\
                    & \cong 1.256637061 \times 10^{-6} \quad \mathrm{N \cdot A^{-2}}
        \end{split}
    \end{equation}

The First and Second Radiation Constants
----------------------------------------

The first radiation constant, :math:`c_1`, is defined as:

.. math::
    \begin{equation}\label{first_rad_constant}
        \begin{split}
            c_1 & \equiv 2 \pi h c^2 \\
                & \cong 3.741771852 \times 10^{-16} \quad \mathrm{W \cdot m^2}
        \end{split}
    \end{equation}

The second radiation constant, :math:`c_2`, is defined as:

.. math::
    \begin{equation}\label{second_rad_constant}
        \begin{split}
            c_2 & \equiv \frac{hc}{k} \\
                & \cong 1.438776877 \times 10^{-2} \quad \mathrm{m \cdot K}
        \end{split}
    \end{equation}

The Faraday Constant
--------------------

.. math::
    \begin{equation}\label{faraday}
        \begin{split}
            F & \equiv N_A e \\
              & \cong 96,485.332123 \quad \mathrm{C \cdot {mol}^{-1}}
        \end{split}
    \end{equation}

The Reduced Planck Constant :math:`\hbar`
-----------------------------------------

The reduced Planck constant is a constant of proportionality to relate the energy of a photon to its angular frequency
(one cycle is :math:`2 \pi` radians of phase angle).

.. math::
    \begin{equation}\label{reduced_planck_constant}
        \begin{split}
            \hbar & \equiv \frac{h}{2 \pi} \\
                  & \cong 1.054571817 \times 10^{-34} \quad \mathrm{J \cdot s}
        \end{split}
    \end{equation}

The Molar Gas Constant
----------------------

The molar gas constant is the amount of work energy required per thermal degree per mole of substance.

.. math::
    \begin{equation}\label{gas_constant}
        \begin{split}
            R & \equiv N_A k \\
              & \cong 8.314462618 \quad \mathrm{J \cdot {mol}^{-1} \cdot K^{-1}}
        \end{split}
    \end{equation}

Characteristic Impedance
------------------------

.. math::
    \begin{equation}\label{characteristic_impedance}
        \begin{split}
            Z_0 & \equiv {\mu}_0 c \\
                & \cong 376.730313668 \quad \mathrm{\Omega}
        \end{split}
    \end{equation}

The Stefan-Boltzmann Constant :math:`\sigma`
--------------------------------------------

The Stefan-Boltzmann Constant is constant of proportionality to relate black body radiant emittance to the fourth
power of the body's temperature.  It is derived from other physical constants.

.. math::
    \begin{equation}\label{stefan_boltzmann}
        \begin{split}
            \sigma & \equiv \frac{2 {\pi}^5 k^4}{15 c^2 h^3} \\
                   & \cong 5.670374419 \quad \mathrm{W \cdot m^{-2} \cdot K^{-4}}
        \end{split}
    \end{equation}

The Electric Constant :math:`\epsilon_0`
----------------------------------------

The currently accepted term for this value is the electric constant; however it has also been referred to as the
*constant of vacuum permittivity*

.. math::
    \begin{equation}\label{electric_constant}
        \begin{split}
            {\varepsilon}_0 & \equiv \frac{1}{{\mu}_0 c^2} \\
                            & \cong 8.85419 \times 10^{-12} \quad \mathrm{F \cdot m^{-1}}
        \end{split}
    \end{equation}

The Fine-Structure Constant :math:`\alpha`
------------------------------------------

The strength of the electric interation between elementary charged particles.

.. math::
    \begin{equation}\label{fine_structure}
        \alpha \equiv \frac{e^2}{2 {\varepsilon}_0 h c} \cong 0.00729735
    \end{equation}

Coulomb's Constant :math:`k_e`
------------------------------

.. math::
    \begin{equation}\label{coulomb}
        \begin{split}
            k_e & \equiv \frac{1}{4 \pi {\varepsilon}_0} \\
                & \cong 8.9875518 \times 10^9 \quad \mathrm{N \cdot m^2 \cdot c^{-2}}
        \end{split}
    \end{equation}

Bohr Radius :math:`a_0`
-----------------------

The Bohr radius is the most probable distance from the neucleus and the electron of a hydrogen atom in
its ground state.

.. math::
    \begin{equation}\label{bohr_radius}
        \begin{split}
            a_0 & \equiv \frac{\hbar^2}{k_e m_e e^2} \\
                & \cong 5.291772 \times 10^{-11} \quad \mathrm{m}
        \end{split}
    \end{equation}

The Rydberg Constant :math:`R_{\infty}` and the Rydberg Unit of Energy
----------------------------------------------------------------------

.. math::
    \begin{equation}\label{rydberg}
        \begin{split}
            R_{\infty} & \equiv \frac{m_e e^{4}}{8 {\varepsilon_0}^2 h^3 c}
                       = \frac{{\alpha}^2 m_e c}{2h} \\
                       & \cong 10,973,731.568 \quad \mathrm{m^{-1}}
        \end{split}
    \end{equation}

The Rydberg unit of energy is defined as the energy of a photon whose wavenumber is the Rydberg constant.

.. math::
    \begin{equation}\label{Ry}
        \begin{split}
            Ry & \equiv h c R_{\infty}
               = \frac{m_e e^{4}}{8 {\varepsilon_0}^2 h^2} \\
               & \cong 2.179872361 \times 10^{-18} \quad \mathrm{J}
        \end{split}
    \end{equation}

References
==========
- CODATA Recommended Values of the Fundamental Physical Constants 2018.
  https://physics.nist.gov/cuu/Constants/
- List of physical constants.
  https://en.wikipedia.org/wiki/List_of_physical_constants

"""

from ._constants import *

__all__ = [name for name in dir() if not name.startswith('_')]
