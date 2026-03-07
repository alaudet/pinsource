"""Install lightweight lgpio and RPi.GPIO stubs so tests can run off-Pi.

Both stubs simulate HCSR04 echo signal behaviour:
  - Valid echo pins (27) produce the sequence [0, 1, 1, 0] per sample
    iteration, which satisfies both while-loops in raw_distance.
  - Any other pin returns 0 forever, triggering the "Echo pulse was not
    received" SystemError after 1000 counter increments.

Stubs are only installed if the real module is not already present (i.e. on
Pi hardware the real libraries are used).
"""

import sys
import types


class _EchoGen:
    """Infinite generator of gpio_read values for one (handle, pin) pair."""

    VALID_PINS = {27}  # matches ECHO_PIN constant used in tests

    def __init__(self, pin: int) -> None:
        self._gen = self._cycle(pin in self.VALID_PINS)

    @staticmethod
    def _cycle(success: bool):
        if success:
            while True:
                yield 0  # first-while body runs → sonar_signal_off set
                yield 1  # first-while condition fails → exits loop
                yield 1  # second-while body runs → sonar_signal_on set
                yield 0  # second-while condition fails → exits loop
        else:
            while True:
                yield 0  # never goes high → SystemError after 1000 iters

    def read(self) -> int:
        return next(self._gen)


class _LgpioStub:
    def __init__(self) -> None:
        self._gens: dict = {}

    def gpiochip_open(self, chip: int) -> int:
        return chip + 1

    def gpio_claim_output(self, h: int, pin: int) -> None:
        pass

    def gpio_claim_input(self, h: int, pin: int) -> None:
        self._gens[(h, pin)] = _EchoGen(pin)

    def gpio_write(self, h: int, pin: int, val: int) -> None:
        pass

    def gpio_read(self, h: int, pin: int) -> int:
        gen = self._gens.get((h, pin))
        return gen.read() if gen is not None else 0

    def gpio_free(self, h: int, pin: int) -> None:
        self._gens.pop((h, pin), None)

    def gpiochip_close(self, h: int) -> None:
        pass


class _GpioEchoGen:
    """Infinite generator of GPIO.input values for one pin.

    Reuses _EchoGen._cycle — same [0, 1, 1, 0] sequence, but keyed by pin
    only (no handle) since GPIO.input(pin) has no handle argument.
    """

    # pin 26 (ECHO_PIN - 1, used in test_raises_exception_no_pulse) is
    # intentionally absent — keeps returning 0, triggering SystemError.
    VALID_PINS = {27}  # matches ECHO_PIN constant used in tests

    def __init__(self, pin: int) -> None:
        self._gen = _EchoGen._cycle(pin in self.VALID_PINS)

    def read(self) -> int:
        return next(self._gen)


class _RPiGPIOStub:
    BCM = 11
    BOARD = 10
    OUT = 0
    IN = 1
    LOW = 0

    def __init__(self) -> None:
        self._gens: dict = {}

    def setmode(self, mode: int) -> None:
        pass

    def setwarnings(self, flag: bool) -> None:
        pass

    def setup(self, pin: int, direction: int) -> None:
        # direction is compared against the stub's own IN constant (1).
        # This is consistent: conftest installs the stub before any import,
        # so GPIO.IN in test code resolves to this same value.
        if direction == self.IN:
            self._gens[pin] = _GpioEchoGen(pin)

    def output(self, pin: int, value) -> None:
        pass

    def input(self, pin: int) -> int:
        gen = self._gens.get(pin)
        return gen.read() if gen is not None else 0

    def cleanup(self, pins=None) -> None:
        if pins is None:
            self._gens.clear()
        else:
            for pin in pins:
                self._gens.pop(pin, None)


if "RPi" not in sys.modules:
    _gpio_stub = _RPiGPIOStub()
    _gpio_mod = types.ModuleType("RPi.GPIO")
    for _attr in ("BCM", "BOARD", "OUT", "IN", "LOW",
                  "setmode", "setwarnings", "setup", "output", "input", "cleanup"):
        setattr(_gpio_mod, _attr, getattr(_gpio_stub, _attr))
    # Both "RPi" and "RPi.GPIO" must be registered: `import RPi.GPIO as GPIO`
    # resolves the parent package first, then the submodule attribute.
    _rpi_mod = types.ModuleType("RPi")
    _rpi_mod.GPIO = _gpio_mod
    sys.modules["RPi"] = _rpi_mod
    sys.modules["RPi.GPIO"] = _gpio_mod


if "lgpio" not in sys.modules:
    _stub = _LgpioStub()
    _mod = types.ModuleType("lgpio")
    for _name in (
        "gpiochip_open",
        "gpio_claim_output",
        "gpio_claim_input",
        "gpio_write",
        "gpio_read",
        "gpio_free",
        "gpiochip_close",
    ):
        setattr(_mod, _name, getattr(_stub, _name))
    sys.modules["lgpio"] = _mod
