# How the test suite works

## The problem

`usonic.py` imports `lgpio` at module load time. On a dev machine this library
is not installed, so any attempt to `import pinsource.usonic` immediately raises
`ModuleNotFoundError`, and pytest cannot even collect the test files.

## The solution: conftest.py

`tests/conftest.py` is a special file that pytest **always loads before
collecting or running any tests**. The conftest takes advantage of this
guaranteed early execution to inject a fake (`stub`) version of `lgpio` into
Python's module registry (`sys.modules`) before any test file is imported.

Because the stub is already in `sys.modules` when the test files are imported,
the statement `import lgpio` inside the source modules silently resolves to the
stub rather than looking for the real package on disk.

On a Raspberry Pi where `lgpio` is already installed and present in
`sys.modules`, the `if "lgpio" not in sys.modules` guard at the bottom of
conftest.py causes the stub injection to be skipped entirely, so the real
hardware is used instead.

## What the stub simulates

The stub models the physical echo signal that an HC-SR04 sensor produces. The
key behaviour lives in `_EchoGen._cycle()`, which is an infinite generator
producing the four-value sequence `[0, 1, 1, 0]` repeatedly:

```
gpio_read call 1 → 0   (echo pin is LOW  → first while-loop body executes, sets sonar_signal_off)
gpio_read call 2 → 1   (echo pin goes HIGH → first while-loop condition fails, loop exits)
gpio_read call 3 → 1   (echo pin still HIGH → second while-loop body executes, sets sonar_signal_on)
gpio_read call 4 → 0   (echo pin goes LOW  → second while-loop condition fails, loop exits)
```

This mirrors exactly what `raw_distance()` expects from real hardware. The
time delta `sonar_signal_on - sonar_signal_off` becomes the stub-derived
distance value.

### Valid vs invalid echo pins

Only pin `27` (the `ECHO_PIN` constant in the test files) is in `VALID_PINS`.
Any other pin number gets the failure generator, which yields `0` forever.
This means the first while-loop in `raw_distance()` never exits naturally and
the `echo_status_counter` reaches 1000, raising `SystemError("Echo pulse was
not received")`. The test `test_raises_exception_no_pulse` deliberately passes
`ECHO_PIN - 1` (pin 26) to exercise this path.

## Stub injection in detail

At the bottom of conftest.py, after the classes are defined:

```python
if "lgpio" not in sys.modules:
    _stub = _LgpioStub()
    _mod = types.ModuleType("lgpio")        # create a blank module object
    # copy each method from the stub onto the module as a top-level function
    for _name in ("gpiochip_open", "gpio_claim_output", ...):
        setattr(_mod, _name, getattr(_stub, _name))
    sys.modules["lgpio"] = _mod             # register it — import lgpio now works
```

## Summary of execution order

```
pytest starts
  └─ loads tests/conftest.py
       ├─ defines _EchoGen, _LgpioStub
       └─ injects stub into sys.modules["lgpio"]      (if not on Pi)

  └─ collects tests/tests_usonic.py
       └─ import pinsource.usonic  →  import lgpio   ✓ (resolves to stub)

  └─ collects tests/tests_pinsource.py
       └─ import pinsource.pinsource  →  import pinsource.usonic  ✓ (already cached)

  └─ runs all tests (stub gpio_read returns pre-scripted values)
```
