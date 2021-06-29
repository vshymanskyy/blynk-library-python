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

This example shows how to perform custom actions
using data from the widget.

In your Blynk App project:
  Add a Slider widget,
  bind it to Virtual Pin V3.
  Run the App (green triangle in the upper right corner)

It will automagically call v3_write_handler.
In the handler, you can use args[0] to get current slider value.
"""

import BlynkLib

BLYNK_AUTH = 'YourAuthToken'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Register virtual pin handler
@blynk.on("V3")
def v3_write_handler(value):
    print('Current slider value: {}'.format(value[0]))

while True:
    blynk.run()
