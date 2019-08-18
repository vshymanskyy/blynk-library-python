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

This example shows how to initialize your WiPy board
and connect it to Blynk.

Don't forget to change WIFI_SSID, WIFI_PASS and BLYNK_AUTH ;)
"""

import BlynkLib
from network import WLAN
import machine, time

WIFI_SSID = 'YourWiFiNetwork'
WIFI_PASS = 'YourWiFiPassword'

BLYNK_AUTH = 'YourAuthToken'

print("Connecting to WiFi...")
wifi = WLAN(mode=WLAN.STA)
wifi.connect(ssid=WIFI_SSID, auth=(WLAN.WPA2, WIFI_PASS))
while not wifi.isconnected():
    time.sleep_ms(50)

print('IP:', wifi.ifconfig()[0])

print("Connecting to Blynk...")
blynk = BlynkLib.Blynk(BLYNK_AUTH)

@blynk.on("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')

def runLoop():
    while True:
        blynk.run()
        machine.idle()

# Run blynk in the main thread:
runLoop()
