"""
Blynk is a platform with iOS and Android apps to control
Arduino, Raspberry Pi and the likes over the Internet.
You can easily build graphic interfaces for all your
projects by simply dragging and dropping widgets.

  Downloads, docs, tutorials: http://www.blynk.cc
  Blynk community:            http://community.blynk.cc
  Social networks:            http://www.fb.com/blynkapp
                              http://twitter.com/blynk_app

This example shows how to make a secure connection using SSL.

Before running this example:
  The server certificate must be uploaded to the WiPy. This
  can easily done via FTP. Take the file 'ca.pem' located in
  the blynk examples folder and put it in '/flash/cert/'.
  Similary to firmware updates, certificates go into the internal
  file system, so it won't be visible after being transferred.

In your Blynk App project:
  Add a Gauge widget,  bind it to Analog Pin 5.
  Add a Slider widget, bind it to Digital Pin 25.
  Run the App (green triangle in the upper right corner).

Don't forget to change WIFI_SSID, WIFI_AUTH and BLYNK_AUTH ;)
"""

import BlynkLib
from network import WLAN
from machine import RTC

WIFI_SSID  = 'YOUR_WIFI'
WIFI_AUTH  = (WLAN.WPA2, 'YOUR_PASS')
BLYNK_AUTH = 'YOUR_AUTH_TOKEN'

# initialize Blynk with security enabled
blynk = BlynkLib.Blynk(BLYNK_AUTH, ssl=True)

# start Blynk (this call should never return)
blynk.run()
