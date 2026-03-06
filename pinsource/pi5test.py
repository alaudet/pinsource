import lgpio
import time

# GPIO pin configuration (BCM numbering)
TRIG_PIN = 17
ECHO_PIN = 27
SPEED_OF_SOUND = 34300  # cm/s at ~20°C

def measure_distance(handle):
    # Send 10µs trigger pulse
    lgpio.gpio_write(handle, TRIG_PIN, 1)
    time.sleep(0.00001)  # 10µs
    lgpio.gpio_write(handle, TRIG_PIN, 0)

    # Wait for echo to go high (pulse start)
    timeout = time.time() + 0.04  # 40ms timeout
    while lgpio.gpio_read(handle, ECHO_PIN) == 0:
        if time.time() > timeout:
            return None
    pulse_start = time.time()

    # Wait for echo to go low (pulse end)
    timeout = time.time() + 0.04
    while lgpio.gpio_read(handle, ECHO_PIN) == 1:
        if time.time() > timeout:
            return None
    pulse_end = time.time()

    # Distance = (travel time * speed of sound) / 2
    duration = pulse_end - pulse_start
    distance = (duration * SPEED_OF_SOUND) / 2
    return distance

def main():
    # Open GPIO chip (chip 0 on Pi 4/5, may vary)
    handle = lgpio.gpiochip_open(0)

    # Claim pins
    lgpio.gpio_claim_output(handle, TRIG_PIN, 0)  # TRIG as output, start LOW
    lgpio.gpio_claim_input(handle, ECHO_PIN)       # ECHO as input
 
    print("CRTL C to quit")
    try:
        while True:
            dist = measure_distance(handle)
            if dist is not None:
                print(f"Distance: {dist} cm")
            else:
                print("Timeout — check wiring or range")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        lgpio.gpiochip_close(handle)

if __name__ == "__main__":
    main()