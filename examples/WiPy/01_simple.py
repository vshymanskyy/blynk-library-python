"""
Blynk is a platform with iOS and Android apps to control
Arduino, Raspberry Pi and the likes over the Internet.
You can easily build graphic interfaces for all your
projects by simply dragging and dropping widgets.

  Downloads, docs, tutorials: http://www.blynk.cc
  Sketch generator:           http://examples.blynk.cc
  Blynk community:            http://community.blynk.cc
  Social networks:            http://www.fb.com/blynkapp
                              http://twitter.com/blynk_app

This example shows one of the simplest scripts,
that doesn't define any custom behaviour.
You're still able to do direct pin operations.

NOTE: You have to use the WiPy-specific Blynk library:
  https://github.com/wipy/wipy

In your Blynk App project:
  Add a Gauge widget,  bind it to Analog Pin 5.
  Add a Slider widget, bind it to Digital Pin 25.
  Run the App (green triangle in the upper right corner).

Don't forget to change WIFI_SSID, WIFI_AUTH and BLYNK_AUTH ;)
"""

import BlynkLib
from network import WLAN

WIFI_SSID = 'YourWiFiNetwork'
WIFI_AUTH = (WLAN.WPA2, 'YourWiFiPassword')

BLYNK_AUTH = 'YourAuthToken'

# Connect to WiFi
wifi = WLAN(mode=WLAN.STA)
wifi.connect(WIFI_SSID, auth=WIFI_AUTH)
while not wifi.isconnected():
    pass

print(wlan.ifconfig())

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Start Blynk (this call should never return)
blynk.run()
