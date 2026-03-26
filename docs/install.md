# Pinsource — Installation and Usage Guide

Pinsource is a Python library for HC-SR04 and JSN-SR04T ultrasonic distance sensors on Raspberry Pi. It uses `lgpio` for GPIO access, which supports all Raspberry Pi models including the Pi 5.

---

## Requirements

- Raspberry Pi (Pi B and later; Pi 2+ recommended)
- Raspberry Pi OS 13 (Trixie) — recommended
- Raspberry Pi OS 12 (Bookworm) — supported
- Python 3.11 or later
- HC-SR04 or JSN-SR04T 2.0 ultrasonic sensor

**Sensors:**
- HC-SR04 — supported
- JSN-SR04T 2.0 — supported (minimum reliable range ~20 cm)
- JSN-SR04T 3.0 — not supported

---

## Installation

Pinsource is distributed as a Debian package via the Linuxnorth APT repository. This is the recommended installation method for developers building on top of it.

### 1. Import the signing key

```bash
curl -fsSL https://apt.linuxnorth.org/public_key.asc \
  | sudo gpg --dearmor -o /usr/share/keyrings/linuxnorth-archive-keyring.gpg
```

### 2. Add the repository

```bash
echo "deb [signed-by=/usr/share/keyrings/linuxnorth-archive-keyring.gpg] \
  https://apt.linuxnorth.org trixie main" \
  | sudo tee /etc/apt/sources.list.d/linuxnorth.list
```

### 3. Install

```bash
sudo apt update
sudo apt install python3-pinsource
```

### Upgrading

```bash
sudo apt update && sudo apt upgrade python3-pinsource
```

---

## Hardware Connection

The HC-SR04 has four pins. Connect them to the Raspberry Pi as follows:

| Sensor Pin | Raspberry Pi        |
|------------|---------------------|
| VCC        | 5V                  |
| GND        | Ground              |
| TRIG       | Any GPIO pin (e.g. GPIO 17) |
| ECHO       | Any GPIO pin via voltage divider (e.g. GPIO 27) |

**Voltage divider required on ECHO:** The sensor outputs 5V on the ECHO pin but Raspberry Pi GPIO pins are rated for 3.3V. Use a 470 Ω resistor in series with the ECHO wire, and a 1000 Ω resistor from ECHO to Ground. This brings the voltage to approximately 3.4V — within safe limits.

GPIO pin numbers are BCM numbering. Set the pins you use in your code.

---

## Quick Test

Installing the package also installs the `pinsource` command-line tool. Use it to verify your sensor is working:

```bash
pinsource -t 17 -e 27
```

**Options:**

```
pinsource -h
usage: pinsource [-h] -t TRIG -e ECHO [-sp SPEED] [-ss SAMPLES]

  -t TRIG        TRIG GPIO pin number (required)
  -e ECHO        ECHO GPIO pin number (required)
  -sp SPEED      Sample wait interval in seconds (default: 0.1)
  -ss SAMPLES    Sample size for median reading (default: 11)
```

**Sample output:**

```
trig pin = gpio 17
echo pin = gpio 27
speed = 0.1
samples = 11

The imperial distance is 12.3 inches.
The metric distance is 31.2 centimetres.
```

---

## Using Pinsource in Your Code

Import the `usonic` module and create a `Measurement` object:

```python
from pinsource import usonic

value = usonic.Measurement(trig_pin=17, echo_pin=27)
```

**Constructor parameters:**

| Parameter   | Default    | Description |
|-------------|------------|-------------|
| `trig_pin`  | (required) | BCM GPIO pin for TRIG |
| `echo_pin`  | (required) | BCM GPIO pin for ECHO |
| `temperature` | `20`     | Ambient temperature (°C for metric, °F for imperial) |
| `unit`      | `"metric"` | `"metric"` (cm / litres) or `"imperial"` (inches / gallons) |
| `gpio_chip` | `0`        | lgpio chip number — `0` works on all current Pi models |

### Getting a distance reading

```python
raw = value.raw_distance()            # error-corrected median in cm
dist = value.distance(raw)            # cm (metric) or inches (imperial)
```

`raw_distance()` takes 11 samples by default and returns the median, corrected for temperature. You can adjust sample size and interval:

```python
raw = value.raw_distance(sample_size=5, sample_wait=0.05)
```

### Getting liquid depth

```python
hole_depth = 80  # cm from sensor to pit bottom
raw = value.raw_distance()
depth = value.depth(raw, hole_depth)
print(f"Water depth: {round(depth, 1)} cm")
```

### One-shot basic reading (no error correction)

```python
dist_cm = usonic.Measurement.basic_distance(trig_pin=17, echo_pin=27)
```

---

## Recipes

The `recipes/` directory in the source repository contains ready-to-run example scripts for every method. They are the fastest way to get started.

### How recipes work

Each recipe is a standalone Python script. Copy and adapt it for your own project. The scripts are intentionally simple — they show the minimum code needed for each use case.

**Available recipes:**

| Recipe file | What it demonstrates |
|---|---|
| `basic_reading.py` | One-shot distance using `basic_distance()` static method |
| `metric_distance.py` | Error-corrected distance in centimetres |
| `imperial_distance.py` | Error-corrected distance in inches |
| `metric_depth.py` | Liquid depth in a container (metric) |
| `imperial_depth.py` | Liquid depth in a container (imperial) |
| `cuboid_volume_metric.py` | Volume of a rectangular container in litres |
| `cuboid_volume_imperial.py` | Volume of a rectangular container in gallons |
| `cylinder_volume_metric.py` | Volume of an upright cylinder in litres |
| `cylinder_volume_imperial.py` | Volume of an upright cylinder in gallons |
| `cylinder_volume_side_metric.py` | Volume of a cylinder on its side in litres |
| `ellip_cylinder_volume.py` | Volume of an upright elliptical cylinder |
| `ellip_side_cylinder_volume.py` | Volume of a side-lying elliptical cylinder |
| `sample_speed.py` | Performance testing — adjusting sample size and wait time |

**Recipes are on GitHub:**
[github.com/alaudet/pinsource/tree/main/recipes](https://github.com/alaudet/pinsource/tree/main/recipes)

---

## Volume Calculations

All volume methods take a `depth` value (result of `value.depth()`) plus the container dimensions. Results are in litres (metric) or gallons (imperial).

| Method | Container shape |
|--------|----------------|
| `cuboid_volume(depth, width, length)` | Rectangular box |
| `cylinder_volume_standing(depth, radius)` | Upright cylinder |
| `cylinder_volume_side(depth, length, radius)` | Cylinder on its side |
| `elliptical_cylinder_volume(depth, semi_maj_axis, semi_min_axis)` | Upright elliptical cylinder |
| `elliptical_side_cylinder_volume(depth, height, width, length)` | Side-lying elliptical cylinder |

---

## License

Apache 2.0 — see [LICENSE](../LICENSE)
