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

This example shows how to run functions after certain intervals

It will automagically call hello_word once after 2 seconds, and print_me
every 5 seconds

You should only need one BlynkTimer instance for a project,
as you can add multiple functions to it
"""

import BlynkLib
from BlynkTimer import BlynkTimer

BLYNK_AUTH = 'YourAuthToken'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Create BlynkTimer Instance
timer = BlynkTimer()


# Will only run once after 2 seconds
def hello_world():
    print("Hello World!")


# Will Print Every 5 Seconds
def print_me():
    print("Thanks!")


# Add Timers
timer.set_timeout(2, hello_world)
timer.set_interval(5, print_me)


while True:
    blynk.run()
    timer.run()
