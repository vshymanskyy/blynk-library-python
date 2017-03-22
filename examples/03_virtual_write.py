"""
Blynk is a platform with iOS and Android apps to control
Arduino, Raspberry Pi and the likes over the Internet.
You can easily build graphic interfaces for all your
projects by simply dragging and dropping widgets.

  Downloads, docs, tutorials: http://www.blynk.cc
  Blynk community:            http://community.blynk.cc
  Social networks:            http://www.fb.com/blynkapp
                              http://twitter.com/blynk_app

This example shows how to perform custom actions
using data from the widget.

In your Blynk App project:
  Add a Slider widget,
  bind it to Virtual Pin V3.
  Run the App (green triangle in the upper right corner)
  
It will automagically call v3_write_handler.
In the handler, you can use args[0] to get current slider value.

Don't forget to change WIFI_SSID, WIFI_AUTH and BLYNK_AUTH ;)
"""

import BlynkLib
import time

BLYNK_AUTH = 'YOUR_AUTH_TOKEN'

# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# to register virtual pins first define a handler
def v3_write_handler(value):
    print('Current slider value: {}'.format(value))

# attach virtual pin 3 to our handler
blynk.add_virtual_pin(3, write=v3_write_handler)

# start Blynk (this call should never return)
blynk.run()
