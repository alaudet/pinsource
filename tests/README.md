# Running Tests

## Install pytest system wide

```sh
sudo apt install python3-pytest
```

All GPIO and hardware dependencies are mocked — tests run on any machine without a Raspberry Pi or sensor attached. Tests use Trig pin 17 and Echo pin 27 by default.

## Commands

Run all tests:
```sh
pytest tests/
```

Run a single test file:
```sh
pytest tests/tests_usonic.py
```

Run a single test:
```sh
pytest tests/tests_usonic.py::MeasurementTestCase::test_measurement
```

## Test files

| File | What it covers |
|---|---|
| `tests_usonic.py` | `Measurement` class — object creation, distance calculation, metric/imperial conversion, depth calculation |
| `tests_pinsource.py` | `hcsr04` CLI entry point — argument parsing, main function output |

## Contributing

All tests must pass before submitting a pull request. New functionality should include a corresponding test.
