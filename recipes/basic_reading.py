"""Example of getting a direct reading using lgpio."""

from pinsource import usonic

# This script uses a static method inside the Measurement class
# called basic_distance.
# No median readings pulled from a sample for error correction.
# A simple return of a cm distance as reported directly from lgpio.
# lgpio pin setup and cleanup are handled internally.

# set gpio pins
trig = 17
echo = 27

x = usonic.Measurement
# use default temp of 20 Celsius
distance_warm = x.basic_distance(trig, echo)

# example of passing temperature reading
# temperature affects speed of sound
# Easily combine with a temperature sensor to pass the current temp
temp = -30
distance_cold = x.basic_distance(trig, echo, celsius=temp)

print("The distance at  20 Celsius is {} cm's".format(distance_warm))
print("The distance at -30 Celsius is {} cm's".format(distance_cold))
