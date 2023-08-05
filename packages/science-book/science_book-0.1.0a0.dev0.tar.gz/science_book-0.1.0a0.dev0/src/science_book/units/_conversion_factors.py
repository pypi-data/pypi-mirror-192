import math

from science_book.physics.constants import atomic_mass as _atomic_mass
from science_book.physics.constants import speed_of_light, standard_gravity

###########################################################
# Time units (relative to second)
###########################################################

second = 1
minute = 60.0
hour = 60 * minute
day = 24 * hour
week = 7 * day
year = 365 * day
julian_year = 365.25 * day

###########################################################
# Angular units (relative to radians)
###########################################################

radian = 1
degree = math.pi / 180
arcmin = arcminute = degree / 60
arcsec = arcsecond = arcmin / 60

###########################################################
# Length units (relative to meter)
###########################################################

meter = metre = 1
inch = 0.0254  # US customary unit
foot = 12 * inch  # US customary unit
yard = 3 * foot  # US customary unit
mile = 5280 * foot  # US customary unit
mil = inch / 1000
fermi = 1e-15
angstrom = 1e-10
micron = 1e-6
au = astronomical_unit = 149_597_870_700.0
light_year = julian_year * speed_of_light
parsec = au / arcsec

###########################################################
# Mass units (relative to kilogram)
###########################################################

# US customary conversion factor to make sure |1 lbm| == |1 lbf|
# as used in Newton's second law (F = ma).
g_c = standard_gravity / foot  # lbm⋅ft/lbf⋅s²

kilogram = 1
gram = 1e-3
metric_ton = 1e3
lb = lbm = pound = 0.453_592_37  # avoirdupois
slug = g_c * lbm  # lbf⋅s²/ft ≅ 14.59390 kg
oz = ounce = pound / 16
stone = 14 * pound
ton = 2000 * pound
u = atomic_mass = _atomic_mass

###########################################################
# Pressure units (relative to Pascal)
###########################################################

pa = Pa = pascal = 1
atm = atmosphere = 101_325
bar = 1e5
torr = mmHg = atm / 760
psi = pound * standard_gravity / inch**2

###########################################################
# Volume units (relative to meter³)
###########################################################

liter = litre = 1e-3
cc = cubic_centimeter = 1e-6
gallon = gallon_us = 231 * inch**3  # US
gallon_imp = 4.546_09e-3  # UK/Imperial gallon
fluid_ounce = fluid_ounce_us = fluid_oz = gallon / 128  # US
fluid_ounce_imp = gallon_imp / 160  # UK/Imperial fluid oz.
bbl = barrel = 42 * gallon_us  # Typically used for oil/petroleum products

###########################################################
# Speed units (relative to meter per second or m/s)
###########################################################

kmh = 1000.0 / hour
mph = mile / hour
fps = foot / second

###########################################################
# Temperature units (relative to kelvin)
###########################################################

zero_celsius = 273.15
degree_fahrenheit = 5.0 / 9.0  # Not for linear conversion, used for incremental differences.
