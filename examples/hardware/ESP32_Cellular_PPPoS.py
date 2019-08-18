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

This example shows how to initialize your ESP32 board
and connect it to Blynk using a Cellular modem.

Read more about LoBo GSM module here:
  https://github.com/loboris/MicroPython_ESP32_psRAM_LoBo/wiki/gsm

Don't forget to change TX/RX pins, APN, user, password and BLYNK_AUTH ;)
"""

import BlynkLib
import gsm
import machine, time

BLYNK_AUTH = 'YourAuthToken'

gsm.start(tx=27, rx=26, apn='', user='', password='')

for retry in range(10):
    if gsm.atcmd('AT'):
        break
    else:
        print("Waiting modem")
        time.sleep_ms(5000)
else:
    raise Exception("Modem not responding!")

print("Connecting to GSM...")
gsm.connect()

while gsm.status()[0] != 1:
    pass

print('IP:', gsm.ifconfig()[0])

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
#_thread.start_new_thread("Blynk", runLoop, ())
