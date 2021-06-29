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

This example shows how to get UTC time and Timezone info
"""

import BlynkLib
import time

BLYNK_AUTH = 'YourAuthToken'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

@blynk.on("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')
    blynk.send_internal("utc", "time")
    blynk.send_internal("utc", "tz_name")

@blynk.on("disconnected")
def blynk_disconnected():
    print('Blynk disconnected')

@blynk.on("internal:utc")
def on_utc(value):
    if value[0] == "time":
        ts = int(value[1])//1000
        # on embedded systems, you may need to subtract time difference between 1970 and 2000
        #ts -= 946684800
        tm = time.gmtime(ts)
        print("UTC time: ", time.asctime(tm))
    elif value[0] == "tz_name":
        print("Timezone: ", value[1])

while True:
    blynk.run()
