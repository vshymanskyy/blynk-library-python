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

This example shows how to initialize your ESP8266/ESP32 board
and connect it to Blynk.

Don't forget to change WIFI_SSID, WIFI_PASS and BLYNK_AUTH ;)
"""

import BlynkLib
import network
import machine

WIFI_SSID = 'YourWiFiNetwork'
WIFI_PASS = 'YourWiFiPassword'

BLYNK_AUTH = 'YourAuthToken'

print("Connecting to WiFi...")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASS)
while not wifi.isconnected():
    pass

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

# Or, run blynk in a separate thread (unavailable for esp8266):
#import _thread
#_thread.stack_size(5*1024)
#_thread.start_new_thread(runLoop, ())


# Note:
# Threads are currently unavailable on some devices like esp8266
# ESP32_psRAM_LoBo has a bit different thread API:
# _thread.start_new_thread("Blynk", runLoop, ())
