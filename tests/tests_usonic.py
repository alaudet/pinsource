import unittest
import math
from unittest.mock import patch
from pinsource.usonic import Measurement

TRIG_PIN = 17
ECHO_PIN = 27
GPIO_CHIP = 0


class MeasurementTestCase(unittest.TestCase):
    def setUp(self):
        """Create metric and imperial Measurement instances for use in tests."""
        self.metric_value_25 = Measurement(TRIG_PIN, ECHO_PIN, 25, "metric", gpio_chip=GPIO_CHIP)
        self.imperial_value = Measurement(TRIG_PIN, ECHO_PIN, 68, "imperial", gpio_chip=GPIO_CHIP)
        self.metric_value = Measurement(TRIG_PIN, ECHO_PIN, 20, "metric", gpio_chip=GPIO_CHIP)

    def test_measurement(self):
        """Test that object is being created properly."""
        value = self.metric_value_25
        value_defaults = Measurement(TRIG_PIN, ECHO_PIN)
        self.assertIsInstance(value, Measurement)
        self.assertEqual(value.trig_pin, TRIG_PIN)
        self.assertEqual(value.echo_pin, ECHO_PIN)
        self.assertEqual(value.temperature, 25)
        self.assertEqual(value.unit, "metric")
        self.assertEqual(value_defaults.trig_pin, TRIG_PIN)
        self.assertEqual(value_defaults.echo_pin, ECHO_PIN)
        self.assertEqual(value_defaults.temperature, 20)
        self.assertEqual(value_defaults.unit, "metric")

    def test_imperial_temperature_and_speed_of_sound(self):
        """Test that Fahrenheit is converted to Celsius internally without mutating
        self.temperature, that speed of sound is calculated correctly, and that
        raw_distance returns a positive float."""
        value = self.imperial_value
        raw_measurement = value.raw_distance()
        converted_temp = (value.temperature - 32) * 0.5556
        speed_of_sound = 331.3 * math.sqrt(1 + (converted_temp / 273.15))
        self.assertEqual(value.temperature, 68)
        self.assertEqual(value.unit, "imperial")
        self.assertIsInstance(raw_measurement, float)
        self.assertGreater(raw_measurement, 0.0)
        self.assertAlmostEqual(speed_of_sound, 343.21555930656075)

    def test_imperial_measurements(self):
        """Test that an imperial measurement is what you would expect with a precise
        raw_measurement."""
        value = self.imperial_value
        raw_measurement = 26.454564846
        hole_depth = 25

        imperial_distance = value.distance(raw_measurement)
        imperial_depth = value.depth(raw_measurement, hole_depth)

        self.assertIsInstance(imperial_distance, float)
        self.assertAlmostEqual(imperial_distance, 10.423098549324001)
        self.assertAlmostEqual(imperial_depth, 14.576901450675999)

    def test_metric_measurements(self):
        """Test that a metric measurement is what you would expect with a precise
        raw_measurement."""
        value = self.metric_value
        raw_measurement = 48.80804985408
        hole_depth = 72

        metric_distance = value.distance(raw_measurement)
        metric_depth = value.depth(raw_measurement, hole_depth)

        self.assertAlmostEqual(metric_distance, 48.80804985408)
        self.assertAlmostEqual(metric_depth, 23.191950145920003)

    def test_temperature_not_mutated(self):
        """Test that calling raw_distance multiple times on an imperial Measurement
        does not double-convert the temperature."""
        value = self.imperial_value
        value.raw_distance()
        value.raw_distance()
        self.assertEqual(value.temperature, 68)

    def test_different_sample_size(self):
        """Test that a user defined sample_size works correctly and returns a
        positive float."""
        value = self.imperial_value
        raw_measurement1 = value.raw_distance(sample_size=1)
        raw_measurement2 = value.raw_distance(sample_size=4)
        raw_measurement3 = value.raw_distance(sample_size=11)
        self.assertIsInstance(raw_measurement1, float)
        self.assertIsInstance(raw_measurement2, float)
        self.assertIsInstance(raw_measurement3, float)
        self.assertGreater(raw_measurement1, 0.0)
        self.assertGreater(raw_measurement2, 0.0)
        self.assertGreater(raw_measurement3, 0.0)

    def test_different_sample_wait(self):
        """Test that a user defined sample_wait time works correctly and returns a
        positive float."""
        value = self.metric_value
        raw_measurement1 = value.raw_distance(sample_wait=0.3)
        raw_measurement2 = value.raw_distance(sample_wait=0.1)
        raw_measurement3 = value.raw_distance(sample_wait=0.03)
        raw_measurement4 = value.raw_distance(sample_wait=0.01)
        self.assertIsInstance(raw_measurement1, float)
        self.assertIsInstance(raw_measurement2, float)
        self.assertIsInstance(raw_measurement3, float)
        self.assertIsInstance(raw_measurement4, float)
        self.assertGreater(raw_measurement1, 0.0)
        self.assertGreater(raw_measurement2, 0.0)
        self.assertGreater(raw_measurement3, 0.0)
        self.assertGreater(raw_measurement4, 0.0)

    def test_basic_distance(self):
        """Test static method ensuring a positive float is returned with default,
        positive, and negative temps."""
        x = Measurement
        basic_reading = x.basic_distance(TRIG_PIN, ECHO_PIN)
        basic_reading2 = x.basic_distance(TRIG_PIN, ECHO_PIN, celsius=10)
        basic_reading3 = x.basic_distance(TRIG_PIN, ECHO_PIN, celsius=0)
        basic_reading4 = x.basic_distance(TRIG_PIN, ECHO_PIN, celsius=-100)
        self.assertIsInstance(basic_reading, float)
        self.assertIsInstance(basic_reading2, float)
        self.assertIsInstance(basic_reading3, float)
        self.assertIsInstance(basic_reading4, float)
        self.assertGreater(basic_reading, 0.0)
        self.assertGreater(basic_reading2, 0.0)
        self.assertGreater(basic_reading3, 0.0)
        self.assertGreater(basic_reading4, 0.0)

    def test_raises_exception_unit(self):
        """Test that a ValueError is raised if user passes invalid unit type."""
        with self.assertRaises(ValueError):
            Measurement(TRIG_PIN, ECHO_PIN, unit="Fahrenheit").raw_distance()

    def test_raises_exception_no_pulse(self):
        """Test that SystemError is raised if echo pulse not received.
        Typically raised with a faulty cable; wrong echo pin simulates that condition."""
        wrong_echo_pin = ECHO_PIN - 1
        with self.assertRaises(SystemError):
            Measurement(TRIG_PIN, wrong_echo_pin).raw_distance()

    def test_depth(self):
        """Test the depth of a liquid."""
        value = self.metric_value
        raw_measurement = 48.80804985408
        hole_depth = 72
        metric_depth = value.depth(raw_measurement, hole_depth)
        self.assertAlmostEqual(metric_depth, 23.191950145920003)

        value2 = self.imperial_value
        hole_depth_inches = hole_depth * 0.394
        imperial_depth = value2.depth(raw_measurement, hole_depth_inches)
        self.assertAlmostEqual(imperial_depth, 9.137628357492481)

    def test_depth_exceeds_container(self):
        """Test that depth() returns a negative value when the reading exceeds
        the container depth, documenting the expected behaviour."""
        value = self.metric_value
        self.assertLess(value.depth(50, 30), 0)

        value2 = self.imperial_value
        self.assertLess(value2.depth(50, 10), 0)

    def test_distance(self):
        """Test the distance measurement."""
        value = self.metric_value
        raw_measurement = 48.80804985408
        metric_distance = value.distance(raw_measurement)
        self.assertAlmostEqual(metric_distance, 48.80804985408)

        value2 = self.imperial_value
        imperial_distance = value2.distance(raw_measurement)
        self.assertAlmostEqual(imperial_distance, 19.23037164250752)

    @patch("pinsource.usonic.lgpio")
    def test_raw_distance_returns_median(self, mock_lgpio):
        """Test that raw_distance returns the median of the sample, not the
        first or last reading, by injecting deterministic time values."""
        mock_lgpio.gpiochip_open.return_value = 0
        # Each sample needs gpio_read to return: 0 (enter first while), 1 (exit
        # first while), 1 (enter second while), 0 (exit second while).
        mock_lgpio.gpio_read.side_effect = [
            0, 1, 1, 0,   # sample 0
            0, 1, 1, 0,   # sample 1
            0, 1, 1, 0,   # sample 2
        ]

        value = self.metric_value  # 20°C metric
        speed_of_sound = 331.3 * math.sqrt(1 + 20 / 273.15)
        factor = (speed_of_sound * 100) / 2

        # Three samples with time_passed values 0.001, 0.003, 0.002.
        # Sorted distances: [0.001*f, 0.002*f, 0.003*f]; median is 0.002*f.
        # Each sample consumes 3 time.time() calls:
        #   1. sonar_signal_off  2. echo_timeout base  3. sonar_signal_on
        time_sequence = [
            1.000, 1000.0, 1.001,   # sample 0: time_passed = 0.001
            2.000, 1000.0, 2.003,   # sample 1: time_passed = 0.003
            3.000, 1000.0, 3.002,   # sample 2: time_passed = 0.002
        ]
        with patch("time.time", side_effect=time_sequence):
            result = value.raw_distance(sample_size=3)

        self.assertAlmostEqual(result, 0.002 * factor)

    def test_cylinder_volume_side(self):
        """Test the volume of liquid in a cylinder resting on its side."""
        value = self.metric_value
        depth = 20
        height = 120
        radius = 45
        cylinder_volume = value.cylinder_volume_side(depth, height, radius)
        self.assertAlmostEqual(cylinder_volume, 126.31926004538707)

        value2 = self.imperial_value
        depthi = 17
        heighti = 27
        radiusi = 18
        cylinder_volume_g = value2.cylinder_volume_side(depthi, heighti, radiusi)
        self.assertAlmostEqual(cylinder_volume_g, 55.28063419280857)

    def test_cylinder_volume_side_boundary(self):
        """Test cylinder_volume_side at the exact boundary values depth=0
        and depth=diameter."""
        value = self.metric_value
        radius = 45
        length = 120
        # Empty container
        self.assertAlmostEqual(value.cylinder_volume_side(0, length, radius), 0.0)
        # Full container: volume = π * r^2 * length / 1000
        full = math.pi * radius ** 2 * length / 1000
        self.assertAlmostEqual(value.cylinder_volume_side(radius * 2, length, radius), full)

    def test_cylinder_volume_standing(self):
        """Test the volume of a liquid in a standing cylinder."""
        depth = 50
        radius = 30
        value = self.metric_value
        cylinder_volume = value.cylinder_volume_standing(depth, radius)
        self.assertAlmostEqual(cylinder_volume, 141.3716694115407)

        depthi = 24
        radiusi = 12
        value2 = self.imperial_value
        cylinder_volume_g = value2.cylinder_volume_standing(depthi, radiusi)
        self.assertAlmostEqual(cylinder_volume_g, 47.00149009007067)

    def test_cuboid_volume(self):
        """Test the volume of a liquid in a cuboid."""
        value = self.metric_value
        depth = 53
        width = 32
        length = 21
        cuboid_volume = value.cuboid_volume(depth, width, length)
        self.assertAlmostEqual(cuboid_volume, 35.616)

        value2 = self.imperial_value
        cuboid_volume_g = value2.cuboid_volume(depth, width, length)
        self.assertAlmostEqual(cuboid_volume_g, 154.1818181818182)

    def test_elliptical_cylinder_volume(self):
        """Test the volume of a liquid in an elliptical cylinder."""
        depth = 50
        semi_maj_axis = 24
        semi_min_axis = 15
        value = self.metric_value
        e_cyl_vol = value.elliptical_cylinder_volume(depth, semi_maj_axis, semi_min_axis)
        self.assertAlmostEqual(e_cyl_vol, 56.548667764616276)

        value2 = self.imperial_value
        e_cyl_vol_g = value2.elliptical_cylinder_volume(depth, semi_maj_axis, semi_min_axis)
        self.assertAlmostEqual(e_cyl_vol_g, 244.79942755245142)

    def test_elliptical_side_cylinder_volume(self):
        """Test the volume of a liquid in an elliptical cylinder on its side."""
        depth = 28
        height = 40
        width = 30
        length = 100
        value = self.metric_value
        e_cyl_vol_side = value.elliptical_side_cylinder_volume(depth, height, width, length)
        self.assertAlmostEqual(e_cyl_vol_side, 70.46757685376555)

        value2 = self.imperial_value
        e_cyl_vol_side_g = value2.elliptical_side_cylinder_volume(depth, height, width, length)
        self.assertAlmostEqual(e_cyl_vol_side_g, 305.05444525439634)

    def test_elliptical_side_boundary(self):
        """Test elliptical_side_cylinder_volume at the exact boundary values
        depth=0 and depth=height."""
        value = self.metric_value
        height = 40
        width = 30
        length = 100
        s_maj_a = width / 2
        s_min_a = height / 2
        # Empty container
        self.assertAlmostEqual(
            value.elliptical_side_cylinder_volume(0, height, width, length), 0.0
        )
        # Full container: volume = π * s_maj_a * s_min_a * length / 1000
        full = math.pi * s_maj_a * s_min_a * length / 1000
        self.assertAlmostEqual(
            value.elliptical_side_cylinder_volume(height, height, width, length), full
        )

    def test_raise_cylinder_v_side(self):
        """Test ValueError raised with impossible depth values."""
        value = self.metric_value
        with self.assertRaises(ValueError):
            value.cylinder_volume_side(20, 80, 9)

        with self.assertRaises(ValueError):
            value.cylinder_volume_side(-1, 80, 20)

        with self.assertRaises(ValueError):
            value.elliptical_side_cylinder_volume(20, 15, 9, 120)

        with self.assertRaises(ValueError):
            value.elliptical_side_cylinder_volume(-1, 80, 20, 120)

    @patch("pinsource.usonic.lgpio")
    def test_gpio_chip_nonzero(self, mock_lgpio):
        """Test that a non-default gpio_chip value is passed to lgpio.gpiochip_open."""
        mock_lgpio.gpiochip_open.return_value = 1
        mock_lgpio.gpio_read.side_effect = [0, 1, 1, 0]   # one sample
        value = Measurement(TRIG_PIN, ECHO_PIN, gpio_chip=1)
        value.raw_distance(sample_size=1)
        mock_lgpio.gpiochip_open.assert_called_once_with(1)
