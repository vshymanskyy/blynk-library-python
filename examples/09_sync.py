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

# initialize Blynk with security enabled
blynk = BlynkLib.Blynk(BLYNK_AUTH)

@blynk.ON("connected")
def blynk_connected():
    # You can also use blynk.sync_virtual(pin)
    # to sync a specific virtual pin
    print("Updating all values from the server...")
    blynk.sync_all()

while True:
    blynk.run()
