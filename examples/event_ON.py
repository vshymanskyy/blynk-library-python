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

This example shows how to use the clever blynk ON() decorator in BlynkLib.py for reads 
and writes, rather than the VIRTUAL_READ() and VIRTUAL_WRITE() decorators
    -   read data from the hardware (Raspberry, ESP32, etc) and 
        display it on the Blynk app widget (example: Gauge, Value Display, etc)
    -   write data from the Blynk app widget (example: Numeric Input, Slider, etc) 
        to the hardware (Raspberry, ESP32, etc)

In your Blynk App project:
    Add a couple of Value Display widgets,
    bind them to Virtual Pin V11 and V12,
    set the read frequency to 1 second.
and
    Add a couple of Numeric Input widgets,
    bind them to Virtual Pin V21 and V22,
then
    Run the App (green triangle in the upper right corner).

It will automagically call the functions
    blynk_handle_vpins_read(pin)
    blynk_handle_vpins_write(pin, value)

"""

import BlynkLib

BLYNK_AUTH = 'YourAuthToken'

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)


#
# general purpose callback function for all READ functions,
# i.e. when the App is reading info from the Raspberry or other hardware
#
# the general pattern: the App, in Pull mode, asks for PinXX.  This code
# responds by obtaining the correct value, and writing in to PinXX
#
# note the 'pin' parameter is arriving as a string, not an int
#
@blynk.ON("readV*")
def blynk_handle_vpins_read(pin):

    print('Server asks a value for V{}'.format(pin))

    # pin 11 used to display 11+11
    if (pin == '11'):
        value = '{}'.format(11+11)
        blynk.virtual_write(11, value)

    # pin 12 used to display 12*12
    elif (pin == '12'):
        value = '{}'.format(12*12)
        blynk.virtual_write(12, value)


#
# general purpose callback function for all WRITE functions,
# i.e. when the App is writing to the Raspberry or other hardware
#
# note the 'pin' parameter is arriving as a string, not an int
# note the 'value' parameter is arriving as a list, with the desired 
# info in the 0th position
#
@blynk.ON("V*")
def blynk_handle_vpins_write(pin, value):

    print('V{} value: {}'.format(pin, value))

    # pin 21 used to write user input 1
    if (pin == '21'):
        user_input_1 = float(value[0])

    # pin 22 used to write user input 2
    elif (pin == '22'):
        user_input_2 = float(value[0])






while True:
    blynk.run()

