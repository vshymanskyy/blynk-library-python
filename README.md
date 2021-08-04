# Python client for Blynk IoT

**Note:** The library has been updated for Blynk 2.0.  
Please remain on `v0.2.0` for legacy Blynk.

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

**Blynk Mobile App:
[<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/googleplay.svg" width="18" height="18" /> Google Play](https://play.google.com/store/apps/details?id=cloud.blynk) | 
[<img src="https://cdn.rawgit.com/simple-icons/simple-icons/develop/icons/apple.svg" width="18" height="18" /> App Store](https://apps.apple.com/us/app/blynk-iot/id1559317868)**

## Documentation
Social: [Webpage](http://www.blynk.cc) / [Facebook](http://www.fb.com/blynkapp) / [Twitter](http://twitter.com/blynk_app) / [Kickstarter](https://www.kickstarter.com/projects/167134865/blynk-build-an-app-for-your-arduino-project-in-5-m/description)  
Documentation: https://docs.blynk.io  
Community Forum: http://community.blynk.cc  
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
- `log_event`
- events: `Vn`, `connected`, `disconnected`, `invalid_auth`
- `TCP` and secure `TLS/SSL` connection support
- can run on embedded hardware, like `ESP8266`, `ESP32`, `W600` or `OpenWrt`

## Ubuntu/Linux/Raspberry Pi installation

```sh
pip install blynk-library-python
```

For **Blynk.Edgent Dynamic Provisioning**, please see `examples/Edgent_Linux_RPi`

## ESP32/ESP8266 installation

- Get the latest [MicroPython](https://micropython.org/download) firmware and flash it to your board  
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
- For ESP8266, you may need to disable secure connection using:
    ```py
    blynk = BlynkLib.Blynk('YourAuthToken', insecure=True)
    ```

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
* [Node-RED for Blynk IoT](https://flows.nodered.org/node/node-red-contrib-blynk-iot)
* [LabVIEW](https://github.com/juncaofish/NI-LabVIEWInterfaceforBlynk)
* [C#](https://github.com/sverrefroy/BlynkLibrary)

### License
This project is released under The MIT License (MIT)
