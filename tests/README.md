# Running tests

## Install Pytest system wide

```sh
sudo apt install python3-pytest
```

If running on a development system the tests will mock the lgpio or Rpi.GPIO modules

If running on a pi connected with hardware it will run the tests with the actual sensor.

Make sure to set your Trig and Echo pins accordingly. These tests use Trig 17 and Echo 27

## Commands

Run all tests (test files use `tests_*.py` naming, configured in `pyproject.toml`):
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

