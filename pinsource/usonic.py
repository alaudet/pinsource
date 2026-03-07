"""Measure the distance or depth with an HCSR04 Ultrasonic sound
sensor and a Raspberry Pi.  Imperial and Metric measurements are available"""

# Al Audet
# MIT License
from __future__ import division

import time
import math
import lgpio


class Measurement(object):
    """Create a measurement using a HC-SR04 Ultrasonic Sensor connected to
    the GPIO pins of a Raspberry Pi.

    Metric values are used by default. For imperial values use
    unit='imperial'
    temperature=<Desired temperature in Fahrenheit>
    """

    def __init__(
        self, trig_pin, echo_pin, temperature=20, unit="metric", gpio_chip=0
    ):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.temperature = temperature
        self.unit = unit
        self.gpio_chip = gpio_chip
        self.pi = math.pi

    def raw_distance(self, sample_size=11, sample_wait=0.1):
        """Return an error corrected unrounded distance, in cm, of an object
        adjusted for temperature in Celcius.  The distance calculated
        is the median value of a sample of `sample_size` readings.


        Speed of readings is a result of two variables.  The sample_size
        per reading and the sample_wait (interval between individual samples).

        Example: To use a sample size of 5 instead of 11 will increase the
        speed of your reading but could increase variance in readings;

        value = usonic.Measurement(trig_pin, echo_pin)
        r = value.raw_distance(sample_size=5)

        Adjusting the interval between individual samples can also
        increase the speed of the reading.  Increasing the speed will also
        increase CPU usage.  Setting it too low will cause errors.  A default
        of sample_wait=0.1 is a good balance between speed and minimizing
        CPU usage.  It is also a safe setting that should not cause errors.

        e.g.

        r = value.raw_distance(sample_wait=0.03)
        """

        if self.unit == "imperial":
            temperature = (self.temperature - 32) * 0.5556
        elif self.unit == "metric":
            temperature = self.temperature
        else:
            raise ValueError("Wrong Unit Type. Unit Must be imperial or metric")

        speed_of_sound = 331.3 * math.sqrt(1 + (temperature / 273.15))
        sample = []

        # Open the GPIO chip and claim pins
        h = lgpio.gpiochip_open(self.gpio_chip)
        lgpio.gpio_claim_output(h, self.trig_pin)
        lgpio.gpio_claim_input(h, self.echo_pin)

        try:
            for distance_reading in range(sample_size):
                lgpio.gpio_write(h, self.trig_pin, 0)
                time.sleep(sample_wait)
                lgpio.gpio_write(h, self.trig_pin, 1)
                time.sleep(0.00001)
                lgpio.gpio_write(h, self.trig_pin, 0)

                echo_status_counter = 1
                while lgpio.gpio_read(h, self.echo_pin) == 0:
                    if echo_status_counter < 1000:
                        sonar_signal_off = time.time()
                        echo_status_counter += 1
                    else:
                        raise SystemError("Echo pulse was not received")
                echo_timeout = time.time() + 0.04
                while lgpio.gpio_read(h, self.echo_pin) == 1:
                    sonar_signal_on = time.time()
                    if sonar_signal_on > echo_timeout:
                        raise SystemError("Echo pulse did not complete")

                time_passed = sonar_signal_on - sonar_signal_off
                distance_cm = time_passed * ((speed_of_sound * 100) / 2)
                sample.append(distance_cm)
        finally:
            # Always release pins and close chip handle
            lgpio.gpio_free(h, self.trig_pin)
            lgpio.gpio_free(h, self.echo_pin)
            lgpio.gpiochip_close(h)

        sorted_sample = sorted(sample)
        return sorted_sample[sample_size // 2]

    def depth(self, median_reading, hole_depth):
        """Calculate the depth of a liquid. hole_depth is the
        distance from the sensor to the bottom of the hole."""
        if self.unit == "metric":
            return hole_depth - median_reading
        else:
            return hole_depth - (median_reading * 0.394)

    def distance(self, median_reading):
        """Calculate the distance from the sensor to an object."""
        if self.unit == "imperial":
            return median_reading * 0.394
        else:
            # don't need this method if using metric. Use raw_distance
            # instead.  But it will return median_reading anyway if used.
            return median_reading

    def cylinder_volume_side(self, depth, length, radius):
        """Calculate the liquid volume of a cylinder on its side"""

        if depth > (radius * 2) or depth < 0:
            raise ValueError(
                "Depth must be less than diameter (radius * 2) and not less than 0"
            )

        volume = length * (
            (radius * radius * math.acos((radius - depth) / radius))
            - (radius - depth) * math.sqrt((2 * depth * radius) - (depth * depth))
        )
        if self.unit == "metric":
            return volume / 1000
        else:
            return volume / 231

    def cylinder_volume_standing(self, depth, radius):
        """Calculate the liquid volume of a standing cylinder"""

        volume = self.pi * radius * radius * depth
        if self.unit == "metric":
            return volume / 1000
        else:
            return volume / 231

    def elliptical_cylinder_volume(self, depth, semi_maj_axis, semi_min_axis):
        """Calculate the liquid volume of a standing elliptical cylinder"""

        volume = self.pi * semi_maj_axis * semi_min_axis * depth
        if self.unit == "metric":
            return volume / 1000
        else:
            return volume / 231

    def elliptical_side_cylinder_volume(self, depth, height, width, length):
        """Calculate the liquid volume of an elliptical cylinder on its side"""
        s_maj_a = width / 2  # semi major axis
        s_min_a = height / 2  # semi minor axis
        if depth > height or depth < 0:
            raise ValueError("Depth must be less than the height and not less than 0")
        volume = (
            length
            * (s_maj_a / s_min_a)
            * (
                (self.pi * (s_min_a**2)) / 2
                + (depth - s_min_a)
                * math.sqrt((s_min_a**2) - ((depth - s_min_a) ** 2))
                + (s_min_a**2) * math.asin(depth / s_min_a - 1)
            )
        )

        if self.unit == "metric":
            return volume / 1000
        else:
            return volume / 231

    def cuboid_volume(self, depth, width, length):
        """Calculate amount of liquid in a cuboid
        (square or rectangle shaped container)"""
        volume = width * length * depth
        if self.unit == "metric":
            return volume / 1000
        else:
            return volume / 231

    @staticmethod
    def basic_distance(trig_pin, echo_pin, celsius=20, gpio_chip=0):
        """Return an unformatted distance in cm's as read directly from
        lgpio."""

        speed_of_sound = 331.3 * math.sqrt(1 + (celsius / 273.15))

        h = lgpio.gpiochip_open(gpio_chip)
        lgpio.gpio_claim_output(h, trig_pin)
        lgpio.gpio_claim_input(h, echo_pin)

        try:
            lgpio.gpio_write(h, trig_pin, 0)
            time.sleep(0.1)
            lgpio.gpio_write(h, trig_pin, 1)
            time.sleep(0.00001)
            lgpio.gpio_write(h, trig_pin, 0)

            echo_status_counter = 1
            while lgpio.gpio_read(h, echo_pin) == 0:
                if echo_status_counter < 1000:
                    sonar_signal_off = time.time()
                    echo_status_counter += 1
                else:
                    raise SystemError("Echo pulse was not received")
            while lgpio.gpio_read(h, echo_pin) == 1:
                sonar_signal_on = time.time()
        finally:
            lgpio.gpio_free(h, trig_pin)
            lgpio.gpio_free(h, echo_pin)
            lgpio.gpiochip_close(h)

        time_passed = sonar_signal_on - sonar_signal_off
        return time_passed * ((speed_of_sound * 100) / 2)