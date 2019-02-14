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

This example shows how to initialize your PyCom board
and connect it to Blynk.

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

print(wifi.ifconfig())

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

while True:
    blynk.run()
