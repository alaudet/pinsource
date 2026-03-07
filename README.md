# Pinsource

Pinsource is a fork of hcsr04sensor at https://github.com/alaudet/hcsr04sensor

It is a python library for easily interacting with sensors with a couple of lines.  See the recipes folder for some examples.

# Why Pinsource

The old name hcsr04sensor was limiting.  First off it works with other ultrasonic sensors such as the JSN-SR04T 2.0.

Also I would like to expand it to other environment sensors.

Pinsource also supports lgpio and is slated to work on Raspberry Pi 5, which is not supported on the new boards.

This version also changes from the MIT License to the Apache 2.0 License.

# Quick install

## WARNING - This code is alpha and not yet suitable for important tasks

This is alpha code.  It may not work.  It may fry your board, burn down your house or steal your truck.   Please use at your own risk!  While it mostly works my setup your mileage may vary.


Install the dependencies

```sh
sudo apt install python3-pip python3-rpi.gpio python3-lgpio python3-virtualenv python3-setuptools
```

Clone the repository

```sh
git clone https://github.com/alaudet/pinsource.git
```

Checkout the devel branch

```sh
cd pinsource && git fetch origin && git checkout --track origin/devel
```

Create the virtualenv

```sh
virtualenv --system-site-packages venv
```

Activate the virtualenv
```sh
source venv/bin/activate
```

```sh
pip3 install -e .
```

The cli version `pinsource` is worth a look for now.

See `pinsource --help` for usage.  

To test if the code works on pi5 try;

```sh
pi5test
```




----------------------------
Copyright © 2026 Al Audet 
