# The MIT License (MIT)
#
# Copyright (c) 2018 Kenny Hora
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Controls the LCD Widget in the Blynk App
class WidgetLCD():
    # Constructor
    # Constructor for the Blynk LCD Widget
    # Parameters:
    #     blynk - Blynk object
    #     vPin  - The Virtual pin the LCD is connected to
    def __init__(self, blynk, vPin):
        self.__blynk = blynk
        self.__vPin = vPin

    # clear()
    # Clears the LCD widget
    # Parameters: None
    def clear(self):
        self.__blynk.virtual_write(self.__vPin, 'clr')

    # write(x, y, s)
    # Prints a message to the LCD
    # Parameters:
    #     x - x-position of the lcd cursor | range [0, 15]
    #     y - y-position of the lcd cursor | range [0, 1]
    #     s - messages to print to the LCD
    def write(self, x, y, s):
        self.__blynk.virtual_write(self.__vPin, '\0'.join(map(str, ('p', x, y, s))))
