"""Calculate the liquid volume of an elliptical cylinder on its side.
For example a milk tank on a truck"""
from pinsource import usonic

trig_pin = 17
echo_pin = 27
# default values
# temperature = 20 celcius
# unit = "metric"

# Get litres in a cylinder
height = 30  # cm height of tank on it side
width = 45  # cm width of tank on its side
length = 96  # cm length of tank on its side
sdistance = 32  # cm from the sensor to the bottom
value = usonic.Measurement(trig_pin, echo_pin)
# for imperial add temp and unit and change all cm values to inches
# value = usonic.Measurement(trig_pin, echo_pin, 68, "imperial")
distance = value.raw_distance()

water_depth_metric = value.depth(distance, sdistance)

volume_litres = value.elliptical_side_cylinder_volume(
    water_depth_metric, height, width, length
)
print(
    "The liquid volume of the elliptical cylinder on its side is {} litres".format(
        round(volume_litres, 1)
    )
)
