# -*- coding: utf-8 -*-

"""Defined physical constants"""

import math


__all__ = [
    "F",
    "G",
    "N_A",
    "R",
    "R_infinity",
    "Ry",
    "Z_0",
    "a_0",
    "alpha",
    "atomic_mass",
    "avogadro",
    "big_G",
    "bohr_radius",
    "boltzmann",
    "c",
    "c_1",
    "c_2",
    "characteristic_impedance",
    "charge_of_electron",
    "coulomb",
    "dalton",
    "delta_cs",
    "e",
    "electric_constant",
    "electron_mass",
    "elementary_charge",
    "epsilon_0",
    "faraday",
    "fine_structure",
    "first_rad_constant",
    "g_0",
    "gas_constant",
    "gravitational_constant",
    "h",
    "h_bar",
    "hyperfine_transition",
    "k",
    "k_cd",
    "k_e",
    "luminous_efficacy",
    "m_e",
    "m_n",
    "m_p",
    "m_u",
    "magnetic_constant",
    "mu_0",
    "neutron_mass",
    "planck",
    "proton_mass",
    "reduced_planck_constant",
    "rydberg",
    "second_rad_constant",
    "sigma",
    "speed_of_light",
    "standard_gravity",
    "stefan_boltzmann",
]

########################
# Latin symbols
########################

c = speed_of_light = 299_792_458
"""Speed of light in vacuum, m/s

The speed of light in vacuum is defined as: c ≡ 299,792,458 m/s.  This is an exact
value using the 2019 redefinition of SI base units.
"""

delta_cs = hyperfine_transition = 9_192_631_770
"""hyperfine transition frequency of the caesium-133 atom, Hz

Also written Δν_Cs or Δν(¹³³Cs).  This is an exact value using the 2019 redefinition
of SI base units.
"""

e = elementary_charge = charge_of_electron = 1.602_176_634e-19
"""Elementary charge, C

The magnitude of the electric charge carried by a single electron in coulomb (C) or A⋅s.
This is an exact value using the 2019 redefinition of SI base units.
"""

G = gravitational_constant = big_G = 6.674_30e-11
"""Newtonian constant of gravitation (big-G), m³/(kg⋅s²)

The Newtonian constant of gravitation (big-G) was first measured by Henry
Cavendish in 1798.  The value of G = 6.674_30 × 10⁻¹¹ has a relative standard
uncertainty of 2.2 × 10⁻⁵.
"""

h = planck = 6.626_070_15e-34
"""Planck constant, J/Hz or J⋅s

A constant of proportionality relating the energy of a photon to its frequency. Planck's
constant was first calculated by Max Planck from experimental data on black-body
radiation in 1901.  It is defined today by the 2019 SI standards.
"""

k = boltzmann = 1.380_649e-23
"""Boltzmann constant, kg⋅m²⋅K⁻¹·s⁻² or J/K

This is an exact value using the 2019 redefinition of SI base units.
"""

k_cd = luminous_efficacy = 683
"""Luminous efficacy of monochromatic radiation of frequency 540 THz (defined), lm/W.

The 2019 SI defined luminous efficacy of green light at 540 THz is exactly 683 lm/W.
540 THz corresponds to a wavelength of approximately 555 nm.
"""

m_e = electron_mass = 9.109_383_710_5e-31
"""electron mass, kg

The invariant (or rest) mass of an electron in kilograms.  This corresponds to an energy
of 0.511 MeV.  This was first measured by J.J. Thompson in 1897 who showed that
mₚ/mₑ > 1000 using cathode rays.
"""

m_p = proton_mass = 1.672_621_923_69e-27
"""proton mass, kg

The invariant (or rest) mass of a proton in kilograms.  This corresponds to
approximately 938 MeV/c²
"""

m_n = neutron_mass = 1.674_927498_04e-27
"""neutron mass, kg

The invariant mass of a neutron in kilograms.  This was determined from measuring the
momenta of the resulting proton and electron from beta decay.
"""

m_u = atomic_mass = dalton = 1.660_539_066_60e-27
"""atomic mass constant, kg

Defined as 1/12 of the mass of an unbound carbon-12 atom.
"""

N_A = avogadro = 6.022_140_76e23
"""Avogadro constant, mol⁻¹

The proportionality constant relating molar mass of a compound to the mass of a sample.
This is an exact value using the 2019 redefinition of SI base units.
"""

g_0 = standard_gravity = 9.806_65
"""standard Earth gravity, m/s²

The nominal acceleration of an object due to gravity, in a vacuum, near the surface
of the Earth.
"""

########################
# Greek symbols
########################

mu_0 = magnetic_constant = (4 * math.pi) * 1e-7
r"""Magnetic constant (vacuum permeability), kg⋅m⋅s⁻²·A⁻² or N/A²

Defined:

.. math::
    \begin{equation}\label{magnetic_constant}
        \begin{split}
            {\mu}_0 & \equiv 4 \pi \times 10^{-7} \quad \mathrm{H \cdot m^{-1}} \\
                    & \cong 1.256637061 \times 10^{-6} \quad \mathrm{N \cdot A^{-2}}
        \end{split}
    \end{equation}
"""

########################
# Derived from previous
########################

# N.B. Order really matters here.

c_1 = first_rad_constant = 2 * math.pi * h * c**2
r"""first radiation constant, W⋅m²

Defined:

.. math::
    \begin{equation}\label{first_rad_constant}
        \begin{split}
            c_1 & \equiv 2 \pi h c^2 \\
                & \cong 3.741771852 \times 10^{-16} \quad \mathrm{W \cdot m^2}
        \end{split}
    \end{equation}
"""

c_2 = second_rad_constant = h * c / k
r"""second radiation constant, m⋅K

Defined:

.. math::
    \begin{equation}\label{second_rad_constant}
        \begin{split}
            c_2 & \equiv \frac{hc}{k} \\
                & \cong 1.438776877 \times 10^{-2} \quad \mathrm{m \cdot K}
        \end{split}
    \end{equation}
"""

F = faraday = N_A * e
r"""Faraday constant, C/mol

Defined:

.. math::
    \begin{equation}\label{faraday}
        \begin{split}
            F & \equiv N_A e \\
              & \cong 96,485.332123 \quad \mathrm{C \cdot {mol}^{-1}}
        \end{split}
    \end{equation}
"""

h_bar = reduced_planck_constant = h / (2 * math.pi)
r"""Reduced Planck constant, J/Hz or J⋅s

A constant of proportionality to relate the energy of a photon to its angular frequency
(one cycle is 2π radians of phase angle).  The reduced Planck constant is defined as:

.. math::
    \begin{equation}\label{reduced_planck_constant}
        \begin{split}
            \hbar & \equiv \frac{h}{2 \pi} \\
                  & \cong 1.054571817 \times 10^{-34} \quad \mathrm{J \cdot s}
        \end{split}
    \end{equation}
"""

R = gas_constant = N_A * k
r"""molar gas constant, J⋅mol⁻¹⋅K⁻¹

The work energy per thermal degree per mole of substance.

Defined:

.. math::
    \begin{equation}\label{gas_constant}
        \begin{split}
            R & \equiv N_A k \\
              & \cong 8.314462618 \quad \mathrm{J \cdot {mol}^{-1} \cdot K^{-1}}
        \end{split}
    \end{equation}
"""

Z_0 = characteristic_impedance = mu_0 * c
r"""characteristic impedance of vacuum, Ω

Defined:

.. math::
    \begin{equation}\label{characteristic_impedance}
        \begin{split}
            Z_0 & \equiv {\mu}_0 c \\
                & \cong 376.730313668 \quad \mathrm{\Omega}
        \end{split}
    \end{equation}
"""

sigma = stefan_boltzmann = (2 * math.pi**5 * R**4) / (15 * h**3 * c**2 * N_A**4)
r"""Stefan-Boltzmann constant, W⋅m⁻²⋅K⁻⁴

The constant of proportionality to relate black body radiant emittance to the fourth
power of the body's temperature.  It is derived from other physical constants.

Defined:

.. math::
    \begin{equation}\label{stefan_boltzmann}
        \begin{split}
            \sigma & \equiv \frac{2 {\pi}^5 k^4}{15 c^2 h^3} \\
                   & \cong 5.670374419 \quad \mathrm{W \cdot m^{-2} \cdot K^{-4}}
        \end{split}
    \end{equation}
"""

epsilon_0 = electric_constant = 1 / (mu_0 * c**2)
r"""electric constant (vacuum permittivity), F/m

Defined:

.. math::
    \begin{equation}\label{electric_constant}
        \begin{split}
            {\varepsilon}_0 & \equiv \frac{1}{{\mu}_0 c^2} \\
                            & \cong 8.85419 \times 10^{-12} \quad \mathrm{F \cdot m^{-1}}
        \end{split}
    \end{equation}
"""

alpha = fine_structure = e**2 / (2 * epsilon_0 * h * c)
r"""fine-structure constant (dimensionless)

The strength of the electric interation between elementary charged particles.

Defined:

.. math::
    \begin{equation}\label{fine_structure}
        \alpha \equiv \frac{e^2}{2 {\varepsilon}_0 h c} \cong 0.00729735
    \end{equation}
"""

k_e = coulomb = 1 / (4 * math.pi * epsilon_0)
r"""Coulomb's constant, N⋅m²⋅c⁻²

Defined:

.. math::
    \begin{equation}\label{coulomb}
        \begin{split}
            k_e & \equiv \frac{1}{4 \pi {\varepsilon}_0} \\
                & \cong 8.9875518 \times 10^9 \quad \mathrm{N \cdot m^2 \cdot c^{-2}}
        \end{split}
    \end{equation}
"""

a_0 = bohr_radius = h_bar**2 / (k_e * m_e * e**2)
r"""Bohr radius, m

The most probable distance from the neucleus and the electron of a hydrogen atom in
its ground state.

Defined:

.. math::
    \begin{equation}\label{bohr_radius}
        \begin{split}
            a_0 & \equiv \frac{\hbar^2}{k_e m_e e^2} \\
                & \cong 5.291772 \times 10^{-11} \quad \mathrm{m}
        \end{split}
    \end{equation}
"""

R_infinity = rydberg = (m_e * e**4) / (8 * epsilon_0**2 * h**3 * c)
r"""Rydberg constant, m⁻¹

Defined:

.. math::
    \begin{equation}\label{rydberg}
        \begin{split}
            R_{\infty} & \equiv \frac{m_e e^{4}}{8 {\varepsilon_0}^2 h^3 c}
                       = \frac{{\alpha}^2 m_e c}{2h} \\
                       & \cong 10,973,731.568 \quad \mathrm{m^{-1}}
        \end{split}
    \end{equation}
"""

Ry = h * c * R_infinity
r"""Rydberg unit of energy, J

The energy of the photon whose wavenumber is the Rydberg constant.

Defined:

.. math::
    \begin{equation}\label{Ry}
        \begin{split}
            Ry & \equiv h c R_{\infty}
               = \frac{m_e e^{4}}{8 {\varepsilon_0}^2 h^2} \\
               & \cong 2.179872361 \times 10^{-18} \quad \mathrm{J}
        \end{split}
    \end{equation}
"""
