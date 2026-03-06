# pinsource

The future home of Pinsource.  



Pinsource, a fork of hcsr04sensor at https://www.linuxnorth.org/hcsr04sensor

Coming Soon!


# Quick install

## WARNING - I HAVEN'T TESTED THIS CODE YET! USE AT YOUR OWN RISK!

This is alpha code only ported from hcsr04sensor.  It wont work.


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
git fetch origin && git checkout --track origin/devel
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

Still uses Rpi.GPIO and not lgpio which will be added later.

If anyone makes it work on Raspberry Pi 5 please let me know.


----------------------------
Copyright © 2026 Al Audet 
