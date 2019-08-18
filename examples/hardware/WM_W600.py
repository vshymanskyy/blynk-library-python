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

This example shows how to initialize your W600 board
and connect it to Blynk.

Don't forget to change WIFI_SSID, WIFI_PASS and BLYNK_AUTH ;)
"""

import BlynkLib
import machine
from easyw600 import *

WIFI_SSID = 'YourWiFiNetwork'
WIFI_PASS = 'YourWiFiPassword'

BLYNK_AUTH = 'YourAuthToken'


wifi = connect(WIFI_SSID, WIFI_PASS)

print("Connecting to Blynk...")
blynk = BlynkLib.Blynk(BLYNK_AUTH, log=print)

@blynk.on("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')

@blynk.VIRTUAL_WRITE(1)
def v1(param):
    print('!!!VIRTUAL_WRITE', param)

@blynk.ON("V2")
def v2(param):
    print('!!!ON')

@blynk.on("V3")
def v3(param):
    print('!!!on')

def runLoop():
    while True:
        blynk.run()
        machine.idle()

runLoop()
