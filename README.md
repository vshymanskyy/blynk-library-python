# Python client for Blynk

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

# Initialize Blynk
blynk = BlynkLib.Blynk('YourAuthToken')

# Register Virtual Pins
@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
    print('Current V1 value: {}'.format(value))

@blynk.VIRTUAL_READ(2)
def my_read_handler():
    # this widget will show some time in seconds..
    blynk.virtual_write(2, int(time.time()))

while True:
    blynk.run()
```


## Features
- **Python 2, Python 3, MicroPython** support
- **<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/linux.svg" width="18" height="18" /> Linux,
<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/windows.svg" width="18" height="18" /> Windows,
<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/apple.svg" width="18" height="18" /> MacOS** support
- `virtual_write`
- `sync_virtual`
- `set_property`
- `notify`, `tweet`
- `log_event`
- events: `Vn`, `readVn`, `connected`, `disconnected`
- can run on embedded hardware, like `ESP8266`, `ESP32`, `W600` or `OpenWrt`

## Ubuntu/Linux/Raspberry Pi installation

```sh
pip install blynk-library-python
```

## ESP8266/ESP32 installation

- Get the latest [MicroPython](https://micropython.org/download) firmware and flash it to your board  
  **Note:** for ESP32 you can also try [LoBo](https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/firmwares) firmware
- Edit [ESP8266_ESP32.py](examples/hardware/ESP8266_ESP32.py) example (put your `auth token` and wifi credentials)
- Use `ampy` or any other method to transfer files to the device  
    ```sh
    export AMPY_PORT=/dev/ttyUSB0
    ampy mkdir /lib
    ampy put BlynkLib.py /lib/BlynkLib.py
    ampy put ./examples/hardware/ESP8266_ESP32.py main.py
    ```
  **Note:** LoBo firmware stores files uder `/flash` directory, use `ampy mkdir /flash/lib` and so on
- Open device terminal and reboot the board (or type `execfile('main.py')`)

## PyCom installation
- This should work with WiPy 1.0, 2.0, 3.0, LoPy, SiPy, GPy, FiPy
- Instructions are the same as for ESP32, just use [PyCom_WiPy.py](examples/hardware/PyCom_WiPy.py) example

__________

### Implementations for other platforms
* [Arduino](https://github.com/blynkkk/blynk-library)
* [Particle](https://github.com/vshymanskyy/blynk-library-spark)
* [Lua, OpenWrt, NodeMCU](https://github.com/vshymanskyy/blynk-library-lua)
* [Node.js, Espruino, Browsers](https://github.com/vshymanskyy/blynk-library-js)
* [OpenWrt packages](https://github.com/vshymanskyy/blynk-library-openwrt)
* [MBED](https://developer.mbed.org/users/vshymanskyy/code/Blynk/)
* [Node-RED](https://www.npmjs.com/package/node-red-contrib-blynk-ws)
* [LabVIEW](https://github.com/juncaofish/NI-LabVIEWInterfaceforBlynk)
* [C#](https://github.com/sverrefroy/BlynkLibrary)

### License
This project is released under The MIT License (MIT)
