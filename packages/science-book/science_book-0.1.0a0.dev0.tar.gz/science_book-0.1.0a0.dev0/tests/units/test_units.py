import math

import science_book.units as units


class TestMassUnits:
    def test_mass_units(self) -> None:
        mass_of_carbon_12 = 12 * units.atomic_mass
        assert math.isclose(mass_of_carbon_12, 1.992_646_879_92e-26)

