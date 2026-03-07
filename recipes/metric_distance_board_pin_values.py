from pinsource import usonic

# Created by Al Audet
# MIT License


def main():
    """Calculate the distance of an object in centimeters using a HCSR04 sensor
    and a Raspberry Pi"""
    # lgpio uses BCM (GPIO) numbers only.
    # Board pin 11 = GPIO 17, board pin 13 = GPIO 27.
    trig_pin = 17
    echo_pin = 27
    # Default values
    # unit = 'metric'
    # temperature = 20

    value = usonic.Measurement(trig_pin, echo_pin)
    raw_measurement = value.raw_distance()

    # Calculate the distance in centimeters
    print("The Distance = {} centimeters".format(round(raw_measurement, 1)))


if __name__ == "__main__":
    main()
