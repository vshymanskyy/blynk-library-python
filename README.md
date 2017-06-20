# blynk-library-python

**Warning:** Work in progress. Code reviews and contributions are more than welcome!

Supports:
- Python 2 and Python 3
- Windows, Linux, OSX
- Micropython (PyCom WiPy, LoPy)
- Virtual pins (see examples)

## Installation

```sh
pip install blynk-library-python
```

## Usage

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
