"""
Blynk is a platform with iOS and Android apps to control
Arduino, Raspberry Pi and the likes over the Internet.
You can easily build graphic interfaces for all your
projects by simply dragging and dropping widgets.

  Downloads, docs, tutorials: http://www.blynk.cc
  Blynk community:            http://community.blynk.cc
  Social networks:            http://www.fb.com/blynkapp
                              http://twitter.com/blynk_app

This example shows how to turn a Terminal widget into
the REPL console.

In your Blynk App project:
  Add a Terminal widget, bind it to Virtual Pin V5.
  Run the App (green triangle in the upper right corner).

Don't forget to change WIFI_SSID, WIFI_AUTH and BLYNK_AUTH ;)
"""

import BlynkLib
import os

BLYNK_AUTH = 'YOUR_AUTH_TOKEN'

def hello():
    print('Welcome!')

# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

term = blynk.repl(5)
os.dupterm(term)

# start Blynk (this call should never return)
blynk.run()
