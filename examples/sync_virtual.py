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
"""

import BlynkLib

BLYNK_AUTH = 'YourAuthToken'

# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

@blynk.on("V*")
def blynk_handle_vpins(pin, value):
    print("V{} value: {}".format(pin, value))

@blynk.on("connected")
def blynk_connected():
    # You can also use blynk.sync_virtual(pin)
    # to sync a specific virtual pin
    print("Updating V1,V2,V3 values from the server...")
    blynk.sync_virtual(1,2,3)

while True:
    blynk.run()
