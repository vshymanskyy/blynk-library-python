#!/usr/bin/env python3

import time, os, sys
import json

import BlynkLib
import BlynkEdgent
import RPi.GPIO as GPIO

# -- Configuration --------------------
BLYNK_TEMPLATE_ID = ""
BLYNK_DEVICE_NAME = ""

BLYNK_FIRMWARE_VERSION = "0.1.0"

BUTTON_GPIO = 16
# -------------------------------------

try:
    with open("config.json") as jsonFile:
        config = json.load(jsonFile)
    needToSave = False
except:
    config = BlynkEdgent.provision(BLYNK_DEVICE_NAME, BLYNK_TEMPLATE_ID, BLYNK_FIRMWARE_VERSION)
    needToSave = True

def reset_config():
    if os.path.exists("config.json"):
        print("Resetting configuration")
        os.remove("config.json")
        # Restart
        os.execv(sys.executable, ['python3'] + sys.argv)
        sys.exit(0)

# Initialize Blynk
blynk = BlynkLib.Blynk(config['auth'],
                       server   = config['server'],
                       port     = config['port_ssl'],
                       tmpl_id  = BLYNK_TEMPLATE_ID,
                       fw_ver   = BLYNK_FIRMWARE_VERSION)

@blynk.on("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')
    if needToSave:
        with open('config.json', 'w') as jsonFile:
            json.dump(config, jsonFile)
        print("Configuration is saved")

@blynk.on("disconnected")
def blynk_disconnected():
    print('Blynk disconnected')

@blynk.on("V*")
def blynk_handle_vpins(pin, value):
    print("V{} value: {}".format(pin, value))

def button_callback(channel):
    if GPIO.input(channel) == 1:
        return

    print("Hold button for 10 seconds to reset configuration")
    start_time = time.time()
    # Wait for the button up
    while (GPIO.input(channel) == 0 and
           time.time() - start_time <= 10):
        time.sleep(0.1)
    if time.time() - start_time > 10:
        reset_config()

# Main

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(BUTTON_GPIO, GPIO.BOTH,
        callback=button_callback, bouncetime=50)

def blynk_connect_with_retries():
    while True:
        try:
            blynk.connect()
            return
        except Exception as e:
            print(e)
            time.sleep(1)

blynk_connect_with_retries()

while True:
    blynk.run()
