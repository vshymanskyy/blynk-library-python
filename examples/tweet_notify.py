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

This example shows how to handle a button press and
send Twitter & Push notifications.

In your Blynk App project:
  Add a Button widget, bind it to Virtual Pin V4.
  Add a Twitter widget and connect it to your account.
  Add a Push notification widget.
  Run the App (green triangle in the upper right corner).
"""

import BlynkLib

BLYNK_AUTH = 'YourAuthToken'

# initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

@blynk.on("V4")
def v4_write_handler(value):
    if value[0]:   # is the the button is pressed?
        blynk.notify('You pressed the button and I know it ;)')
        blynk.tweet('My IoT project is tweeting using @blynk_app and it’s awesome! #IoT #blynk')

while True:
    blynk.run()
