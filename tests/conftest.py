"""Install a lightweight lgpio stub so tests can run off-Pi.

The stub simulates HCSR04 echo signal behaviour:
  - Valid echo pins (27) produce the sequence [0, 1, 1, 0] per sample
    iteration, which satisfies both while-loops in raw_distance.
  - Any other pin returns 0 forever, triggering the "Echo pulse was not
    received" SystemError after 1000 counter increments.

The stub is only installed if the real lgpio module is not already present
(i.e. on Pi hardware the real library is used).
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
