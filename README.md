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

Create the virtualenv

```sh
virtualenv --system-site-packages pinsource
```

Activate the virtualenv
```sh
source pinsource/bin/activate
```

```sh
pip3 install -e https://github.com/alaudet/pinsource/archive/refs/heads/devel.zip
```

The cli version `pinsource` is worth a look for now.

See `pinsource --help` for usage.  


----------------------------
Copyright © 2026 Al Audet 
