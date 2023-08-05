"""A module for handling temperature unit conversions."""

from typing import Union

from science_book.units import zero_celsius


__all__ = [
    "convert_celsius_to_kelvin",
    "convert_fahrenheit_to_kelvin",
    "convert_rankine_to_kelvin",
    "convert_kelvin_to_celsius",
    "convert_kelvin_to_fahrenheit",
    "convert_kelvin_to_rankine",
    "convert_to_kelvin",
    "convert_from_kelvin",
    "convert_temperature",
]


def __get_normalized_temperature_scale(scale: str) -> str:
    """Determines the temperature scale based on input.

    Parameters
    ----------
    scale : str
        A string to use for interpreting which temperature scale to use.

    Returns
    -------
    str
        One of "C", "K", "F", or "R" for the temperature scales: celsius, kelvin,
        fahrenheit, or rankine, respectively.  An empty string is returned when
        the scale cannot be determined from the input.
    """
    if scale.lower() in {"celsius", "c", "centigrade"}:
        return "C"
    elif scale.lower() in {"kelvin", "k"}:
        return "K"
    elif scale.lower() in {"fahrenheit", "f"}:
        return "F"
    elif scale.lower() in {"rankine", "r"}:
        return "R"
    else:
        return ""


def convert_celsius_to_kelvin(celsius_temperatures: list[float]) -> list[float]:
    """Converts a list of celsius temperature values to kelvin temperature values

    Parameters
    ----------
    celsius_temperatures : list of float
        A list of temperatures in celsius which are to be converted to the kelvin
        temperature scale.

    Returns
    -------
    list of float
        A list of temperature values converted from celsius to kelvin.

    Raises
    ------
    ValueError
        If any temperature below absolute zero is present in the array.

    Notes
    -----
    The conversion from celsius to kelvin is a linear shift of 273.15:

    .. math:: T_{K} = T_{C} + 273.15

    Examples
    --------
    >>> convert_celsius_to_kelvin([-273.15, 0, 24.85, 50.75])
    [0.0, 273.15, 298.0, 323.9]
    """
    if any(temperature < zero_celsius for temperature in celsius_temperatures):
        raise ValueError("A celsius temperature below absolute zero was given")

    return [temperature_value + zero_celsius for temperature_value in celsius_temperatures]


def convert_fahrenheit_to_kelvin(fahrenheit_temperatures: list[float]) -> list[float]:
    return [((temperature_value - 32) * 5 / 9) + zero_celsius for temperature_value in fahrenheit_temperatures]


def convert_rankine_to_kelvin(rankine_temperatures: list[float]) -> list[float]:
    return [temperature_value * 5 / 9 for temperature_value in rankine_temperatures]


def convert_kelvin_to_celsius(kelvin_temperatures: list[float]) -> list[float]:
    return [temperature_value - zero_celsius for temperature_value in kelvin_temperatures]


def convert_kelvin_to_fahrenheit(kelvin_temperatures: list[float]) -> list[float]:
    return [((temperature_value - zero_celsius) * 9 / 5) + 32 for temperature_value in kelvin_temperatures]


def convert_kelvin_to_rankine(kelvin_temperatures: list[float]) -> list[float]:
    return [temperature_value * 9 / 5 for temperature_value in kelvin_temperatures]


def convert_to_kelvin(temperature_array: list[float], convert_from: str) -> list[float]:
    convert_from = __get_normalized_temperature_scale(convert_from)
    if convert_from == "C":
        return convert_celsius_to_kelvin(temperature_array)
    elif convert_from == "K":
        return temperature_array
    elif convert_from == "F":
        return convert_fahrenheit_to_kelvin(temperature_array)
    elif convert_from == "R":
        return convert_rankine_to_kelvin(temperature_array)
    else:
        raise NotImplementedError("The specified temperature scale is not supported.")


def convert_from_kelvin(kelvin_temperature_array: list[float], convert_to: str) -> list[float]:
    convert_to = __get_normalized_temperature_scale(convert_to)
    if convert_to == "C":
        return convert_kelvin_to_celsius(kelvin_temperature_array)
    elif convert_to == "K":
        return kelvin_temperature_array
    elif convert_to == "F":
        return convert_kelvin_to_fahrenheit(kelvin_temperature_array)
    elif convert_to == "R":
        return convert_kelvin_to_rankine(kelvin_temperature_array)
    else:
        raise NotImplementedError("The specified temperature scale is not supported.")


def convert_temperature(
    temperature: Union[float, list[float]], old_scale: str, new_scale: str
) -> Union[float, list[float]]:
    """Converts temperature from one given scale to another

    This function converts temperature(s) from a specified scale (e.g. celsius) to
    another specified scale (e.g. kelvin).

    Parameters
    ----------
    temperature : float or list of float
        An array of temperatures that are to be converted.  Note that validity checking
        is not done here (e.g. negative absolute temperature).
    old_scale : str
        A string specifying the original scale of the input temperature(s).  Celsius
        ("celsius", "C", "c", or "centigrade"), Fahrenheit ("fahrenheit", "F", or "f"),
        Kelvin ("kelvin", "K", or "k"), or Rankine ("rankine", "R", or "r").
    new_scale : str
        A string specifying the scale to which the given temperature(s) is to be
        converted.  Celsius ("celsius", "C", "c", or "centigrade"), Fahrenheit
        ("fahrenheit", "F", or "f"), Kelvin ("kelvin", "K", or "k"), or Rankine
        ("rankine", "R", or "r").

    Returns
    -------
    float or list of float
        The converted temperature(s) in the scale specified by `new_scale`.

    Raises
    ------
    NotImplemented
        If either `old_scale` or `new_scale` is a not a supported temperature scale.

    See Also
    --------
    convert_to_kelvin
    convert_from_kelvin

    Notes
    -----
    This function does NOT check the validity of the given temperatures (such as a
    negative absolute temperature).  The function first attempts to convert the
    input(s) from the specified original scale to kelvin, then from kelvin to the
    desired output scale.

    Examples
    --------
    Passing a list of temperatures to convert from fahrenheit to celsius.

    >>> fahrenheit_temperatures = [32, 72, 98.6]
    >>> convert_temperature(fahrenheit_temperatures, "F", "C")
    [0.0, 22.22222222222223, 37.0]

    Using a single value to convert celsius to kelvin

    >>> convert_temperature(-273.15, "celsius", "kelvin")
    0.0
    """
    temperature_is_a_list = True
    if type(temperature) is not list:
        temperature = [temperature]
        temperature_is_a_list = False

    try:
        temperature_in_kelvin = convert_to_kelvin(temperature, old_scale)
        result = convert_from_kelvin(temperature_in_kelvin, new_scale)
    except NotImplementedError:
        raise

    return result if temperature_is_a_list else result[0]
