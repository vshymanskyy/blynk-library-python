import BlynkLib
import WidgetLCD
import datetime

# Blynk Auth Key - Get from Blynk App
BLYNK_AUTH = 'Your Auth Key Here'

# Blynk Object - allows virtual writing and reading
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# LCD Widget
# Attached to LCD widget on Blynk app on Virtual pin V0 and in advanced mode
lcd = WidgetLCD.WidgetLCD(blynk, 0)

# Button Widget
# Attached to Button on Virtual pin V1
# Prints date and time
@blynk.VIRTUAL_WRITE(1)
def printTime(value):
    if value == '1':
        # Clear LCD
        lcd.clear()
        #Print Date and time
        lcd.write(0, 0, datetime.datetime.now().strftime("%m/%d/%Y"))
        lcd.write(0, 1, datetime.datetime.now().strftime("%I:%M:%S %p"))

if __name__ == '__main__':
    # Run Blynk
    blynk.run()
