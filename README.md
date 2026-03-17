# Pinsource Alpha Release

Pinsource is a Python library for easily interacting with sensors on the Raspberry Pi. It is a fork and modernisation of [hcsr04sensor](https://github.com/alaudet/hcsr04sensor). Currently supports ultrasonic distance sensors; additional sensor types are planned.

---

## Why Pinsource?

The original name `hcsr04sensor` was too narrow, the library already works with other ultrasonic sensors such as the JSN-SR04T 2.0, and is intended to grow beyond that.

Pinsource uses `lgpio` instead of `RPi.GPIO`, which adds support for Raspberry Pi 5 and keeps the library compatible with current Raspberry Pi OS releases.

The license has also changed from MIT to Apache 2.0.

---

## Supported Hardware

- Raspberry Pi 2, 3, 4, and 5
- Ultrasonic sensors: HC-SR04, JSN-SR04T 2.0 (waterproof). JSN-SR04T 3.0 not recommended.

---

## Supported OS

| OS | Architecture |
|---|---|
| Raspberry Pi OS 13 (Trixie) | 32-bit and 64-bit |
| Raspberry Pi OS 12 (Bookworm) | 32-bit and 64-bit |

---

## Install

Alpha releases are available via the Linuxnorth APT repository. This is an
unstable channel intended for testers — use on a production system at your own risk.

You should remove any previous versions of hcsr04sensor before doing this.  

```bash
# 1. Import the signing key
curl -fsSL https://apt.linuxnorth.org/public_key.asc \
  | sudo gpg --dearmor -o /usr/share/keyrings/linuxnorth-archive-keyring.gpg

# 2. Add the repository
echo "deb [signed-by=/usr/share/keyrings/linuxnorth-archive-keyring.gpg] \
  https://apt.linuxnorth.org unstable main" \
  | sudo tee /etc/apt/sources.list.d/linuxnorth.list

# 3. Install
sudo apt update
sudo apt install python3-pinsource
```

Please report issues in the [issue tracker](https://github.com/alaudet/raspi-sump/issues).
---

## Usage

The `pinsource` CLI command is a quick way to test your sensor:

```sh
pinsource --help
```

See the `recipes/` folder for example scripts using the library directly.

---

## Why not just use gpiozero?

gpiozero is an excellent project. Pinsource exists primarily to support [Raspi-Sump](https://github.com/alaudet/raspi-sump) with the specific measurement behaviour that application requires, and as a learning exercise in library design. 

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) before submitting a pull request.

Issue tracker: https://github.com/alaudet/pinsource/issues

---

## License

Released under the [Apache 2.0 License](LICENSE).

---

Copyright © 2026 Al Audet
