"""Calculate the liquid volume of a cylinder on its side"""
from pinsource import usonic

trig_pin = 17
echo_pin = 27
# default values
# temperature = 20 celcius
# unit = "metric"

# Get litres in a cylinder
cyl_length_metric = 300  # centimeters
cyl_radius_metric = 48  # centimeters
cyl_depth = 96  # cm from sensor to bottom
value = usonic.Measurement(trig_pin, echo_pin)
# for imperial add temp and unit and change all cm values to inches
# value = usonic.Measurement(trig_pin, echo_pin, 68, 'imperial')
distance = value.raw_distance()
water_depth_metric = value.depth(distance, cyl_depth)
volume_litres = value.cylinder_volume_side(
    water_depth_metric, cyl_length_metric, cyl_radius_metric
)
print(
    "The liquid volume of the cylinder on its side {} litres".format(
        round(volume_litres, 1)
    )
)
