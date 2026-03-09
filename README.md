# Pinsource

Pinsource is a fork of hcsr04sensor at https://github.com/alaudet/hcsr04sensor

It is a python library for easily interacting with sensors with a couple of lines.  See the recipes folder for some examples.  For now only Ultrasonic sound sensors are available.

## Why Pinsource?

The old name hcsr04sensor was limiting.  First off it works with other ultrasonic sensors such as the JSN-SR04T 2.0.

Also I would like to expand it to other environment sensors.

Pinsource also supports lgpio and is slated to work on Raspberry Pi 5, which is not supported on the new boards.

This version also changes from the MIT License to the Apache 2.0 License.

## Why not just use gpiozero?

I love gpiozero.  It's a wonderful project and I am amazed how many sensors it can interact with. 

My motivation for Pinsource (and its predecessor hcsr04sensor which I released in 2014) is to learn and  use in my own Raspi-Sump application (an application for monitoring water depth in any container).  It's more focused on the things I require.

## Use of AI in code

Claude Code was used to help migrate legacy code from hcsr04sensor to pinsource.

I use AI to help in tasks that I am comfortable doing but saves time.  All code is reviewed by me and accepted by me before publishing.  I will never publish anything I didn't ask for specifically and/or which I haven't reviewed personally.

# Quick install

## WARNING - This code is alpha and not yet suitable for important tasks

This is alpha code.  It may not work. While it mostly works on my setup, your mileage may vary.


Install the dependencies

```sh
sudo apt install python3-pip python3-lgpio python3-virtualenv python3-setuptools
```

Clone the repository

```sh
git clone https://github.com/alaudet/pinsource.git
```

Checkout the devel branch

```sh
cd pinsource && git fetch origin && git checkout --track origin/devel
```

Create the virtualenv.  All dependencies use approved debian system packages that are installed in the system python.

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


# Usage

The cli version `pinsource` is a quick way to test your sensor.

See `pinsource --help` for usage.  

To test if the code works on pi5 try;

```sh
pi5test
```




----------------------------
Copyright © 2026 Al Audet 
