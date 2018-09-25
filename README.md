# blynk-library-python

**Warning:** Work in progress. Code reviews and contributions are more than welcome!

[![GitHub version](https://img.shields.io/github/release/vshymanskyy/blynk-library-python.svg)](https://github.com/vshymanskyy/blynk-library-python/releases/latest)
[![GitHub download](https://img.shields.io/github/downloads/vshymanskyy/blynk-library-python/total.svg)](https://github.com/vshymanskyy/blynk-library-python/releases/latest)
[![GitHub stars](https://img.shields.io/github/stars/vshymanskyy/blynk-library-python.svg)](https://github.com/vshymanskyy/blynk-library-python/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/vshymanskyy/blynk-library-python.svg)](https://github.com/vshymanskyy/blynk-library-python/issues)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/vshymanskyy/blynk-library-python/blob/master/LICENSE)

If you like **Blynk** - give it a star, or fork it and contribute! 
[![GitHub stars](https://img.shields.io/github/stars/blynkkk/blynk-library.svg?style=social&label=Star)](https://github.com/blynkkk/blynk-library/stargazers) 
[![GitHub forks](https://img.shields.io/github/forks/blynkkk/blynk-library.svg?style=social&label=Fork)](https://github.com/blynkkk/blynk-library/network)
__________

## What is Blynk?
Blynk provides **iOS** and **Android** apps to control any hardware **over the Internet** or **directly using Bluetooth**.
You can easily build graphic interfaces for all your projects by simply dragging and dropping widgets, **right on your smartphone**.
Blynk is **the most popular IoT platform** used by design studios, makers, educators, and equipment vendors all over the world.

![Blynk Banner](https://github.com/blynkkk/blynkkk.github.io/blob/master/images/GithubBanner.jpg)

## Download

**Blynk App: 
[<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/googleplay.svg" width="18" height="18" /> Google Play](https://play.google.com/store/apps/details?id=cc.blynk) | 
[<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/apple.svg" width="18" height="18" /> App Store](https://itunes.apple.com/us/app/blynk-control-arduino-raspberry/id808760481?ls=1&mt=8)**

**Blynk [Server](https://github.com/blynkkk/blynk-server)**

## Documentation
Social: [Webpage](http://www.blynk.cc) / [Facebook](http://www.fb.com/blynkapp) / [Twitter](http://twitter.com/blynk_app) / [Kickstarter](https://www.kickstarter.com/projects/167134865/blynk-build-an-app-for-your-arduino-project-in-5-m/description)  
Help Center: http://help.blynk.cc  
Documentation: http://docs.blynk.cc/#blynk-firmware  
Community Forum: http://community.blynk.cc  
Examples Browser: http://examples.blynk.cc  
Blynk for Business: http://www.blynk.io

## Usage example

```py
import BlynkLib
import time

BLYNK_AUTH = 'YourAuthToken'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Register Virtual Pins
@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
    print('Current V1 value: {}'.format(value))

@blynk.VIRTUAL_READ(2)
def my_read_handler():
    # this widget will show some time in seconds..
    blynk.virtual_write(2, time.ticks_ms() // 1000)

# Start Blynk (this call should never return)
blynk.run()
```

## Installation

```sh
pip install blynk-library-python
```

## Features
- Python 2 and Python 3
- Windows, Linux, OSX
- Micropython (PyCom WiPy, LoPy)
- Virtual pins (see examples)


## Notes

For some devices (like PyCom WiPy) you need to setup internet connection first:
```py
from network import WLAN

WIFI_SSID = 'YourWiFiNetwork'
WIFI_AUTH = (WLAN.WPA2, 'YourWiFiPassword')

wlan = WLAN(mode=WLAN.STA)
wlan.connect(WIFI_SSID, auth=WIFI_AUTH, timeout=5000)
print(wlan.ifconfig())
```

__________

### Implementations for other platforms
* [Arduino](https://github.com/blynkkk/blynk-library)
* [Particle](https://github.com/vshymanskyy/blynk-library-spark)
* [Lua, OpenWrt, NodeMCU](https://github.com/vshymanskyy/blynk-library-python)
* [Node.js, Espruino, Browsers](https://github.com/vshymanskyy/blynk-library-js)
* [OpenWrt packages](https://github.com/vshymanskyy/blynk-library-openwrt)
* [MBED](https://developer.mbed.org/users/vshymanskyy/code/Blynk/)
* [Node-RED](https://www.npmjs.com/package/node-red-contrib-blynk-ws)
* [LabVIEW](https://github.com/juncaofish/NI-LabVIEWInterfaceforBlynk)
* [C#](https://github.com/sverrefroy/BlynkLibrary)

### License
This project is released under The MIT License (MIT)
