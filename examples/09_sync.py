"""
Blynk is a platform with iOS and Android apps to control
Arduino, Raspberry Pi and the likes over the Internet.
You can easily build graphic interfaces for all your
projects by simply dragging and dropping widgets.

  Downloads, docs, tutorials: http://www.blynk.cc
  Blynk community:            http://community.blynk.cc
  Social networks:            http://www.fb.com/blynkapp
                              http://twitter.com/blynk_app

Don't forget to change WIFI_SSID, WIFI_AUTH and BLYNK_AUTH ;)
"""

import BlynkLib

BLYNK_AUTH = 'YOUR_AUTH_TOKEN'

# initialize Blynk with security enabled
blynk = BlynkLib.Blynk(BLYNK_AUTH)

def blynk_connected():
    # You can also use blynk.sync_virtual(pin)
    # to sync a specific virtual pin
    print("Updating all values from the server...")
    blynk.sync_all()

blynk.on_connect(blynk_connected)

# start Blynk (this call should never return)
blynk.run()
