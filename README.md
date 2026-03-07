# pinsource

The future home of Pinsource.  



Pinsource, a fork of hcsr04sensor at https://www.linuxnorth.org/hcsr04sensor

Coming Soon!


# Quick install

## WARNING - I HAVEN'T TESTED THIS CODE YET! USE AT YOUR OWN RISK!

This is alpha code only ported from hcsr04sensor.  It may not work.  It may fry your board and burn down your house.   Please use at your own risk!


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

To test if the code works on pi5 try;

```sh
pi5test
```


----------------------------
Copyright © 2026 Al Audet 
