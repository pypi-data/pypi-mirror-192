import math

from science_book.physics.constants import (
    F,
    G,
    N_A,
    R,
    R_infinity,
    Ry,
    Z_0,
    a_0,
    alpha,
    c,
    c_1,
    c_2,
    delta_cs,
    e,
    epsilon_0,
    h,
    h_bar,
    k,
    k_cd,
    k_e,
    m_e,
    m_n,
    m_p,
    m_u,
    math,
    mu_0,
    sigma,
)


# Defined by values
class TestDefinedValues:
    """Tests the principal physical constants that have defined values.

    The values tested here correspond to the CODATA 2018 set.
    """

    def test_defined_value_constants(self) -> None:
        assert c == 299_792_458
        assert delta_cs == 9_192_631_770
        assert k_cd == 683

        assert math.isclose(G, 6.674_30e-11)
        assert math.isclose(N_A, 6.022_140_76e23)
        assert math.isclose(e, 1.602_176_634e-19)
        assert math.isclose(h, 6.626_070_15e-34)
        assert math.isclose(k, 1.380_649e-23)
        assert math.isclose(m_e, 9.109_383_7105e-31)
        assert math.isclose(m_n, 1.674_927_498_04e-27)
        assert math.isclose(m_p, 1.672_621_923_69e-27)
        assert math.isclose(m_u, 1.660_539_066_60e-27)

    def test_proton_electron_mass_ratio(self) -> None:
        assert math.isclose(m_p / m_e, 1836.152_673_43)


class TestDerivedValues:
    """Tests the physical constants whose values may be derived from others."""

    def test_derived_value_constants(self) -> None:
        assert math.isclose(F, 96_485.332_123_310_0184)
        assert math.isclose(R, 8.314_462_618_153_24)
        assert math.isclose(R_infinity, 10_973_731.568_160)
        assert math.isclose(Ry, 2.179_872_361_1035e-18)
        assert math.isclose(Z_0, 376.730_313_668)
        assert math.isclose(a_0, 5.291_772_109_03e-11)
        assert math.isclose(alpha, 7.297_352_5693e-3)
        assert math.isclose(c_1, 3.741_771_852e-16)
        assert math.isclose(c_2, 1.438_776_877e-2)
        assert math.isclose(epsilon_0, 8.854_187_8128e-12)
        assert math.isclose(h_bar, 1.054_571_817e-34)
        assert math.isclose(k_e, 8.987_551_7923e9)
        assert math.isclose(mu_0, 1.256_637_062_12e-06)
        assert math.isclose(sigma, 5.670_374_419e-08)
