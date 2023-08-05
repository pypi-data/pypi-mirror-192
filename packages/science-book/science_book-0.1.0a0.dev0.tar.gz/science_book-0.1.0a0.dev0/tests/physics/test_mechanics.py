import math

import pytest

from science_book.physics.mechanics import calculate_freefall_time


class TestFreeFall:
    def test_freefall_function_works(self) -> None:
        assert math.isclose(calculate_freefall_time(20), 2.019_619_977_102)
        assert math.isclose(calculate_freefall_time(20, gravity=3.72076), 3.278_794_265_427)

    def test_freefall_from_zero_works(self) -> None:
        assert calculate_freefall_time(0) == 0

    def test_invalid_height_throws(self) -> None:
        with pytest.raises(ValueError):
            calculate_freefall_time(-10.0)

    def test_negative_gravity_throws(self) -> None:
        with pytest.raises(ValueError):
            calculate_freefall_time(20, gravity=-9.81)

    def test_zero_gravity_throws(self) -> None:
        with pytest.raises(ValueError):
            time = calculate_freefall_time(20, gravity=0)
