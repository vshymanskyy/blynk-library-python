"""
Blynk is a platform with iOS and Android apps to control
Arduino, Raspberry Pi and the likes over the Internet.
You can easily build graphic interfaces for all your
projects by simply dragging and dropping widgets.

  Downloads, docs, tutorials: http://www.blynk.cc
  Blynk community:            http://community.blynk.cc
  Social networks:            http://www.fb.com/blynkapp
                              http://twitter.com/blynk_app

This example shows how to display custom data on the widget.

In your Blynk App project:
  Add a Value Display widget,
  bind it to Virtual Pin V2,
  set the read frequency to 1 second.
  Run the App (green triangle in the upper right corner).
  
It will automagically call v2_read_handler.
Calling virtual_write updates widget value.

Don't forget to change WIFI_SSID, WIFI_AUTH and BLYNK_AUTH ;)
"""

import BlynkLib
import time

BLYNK_AUTH = 'YOUR_AUTH_TOKEN'

# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# to register virtual pins first define a handler:
@blynk.VIRTUAL_READ(2)
def my_read_handler():
    # this widget will show some time in seconds..
    blynk.virtual_write(2, time.ticks_ms() // 1000)

# start Blynk (this call should never return)
blynk.run()
