#!/usr/bin/env python3

"""
Stub of the machine module, useful to run the Blynk client using CPython.
"""

import time
import sys


"""
Some common utilities
"""
try:
    float(1)
    floating_point = True
except:
    floating_point = False

start_time = time.time()
def pyblog(msg):
    if floating_point:
        print ("[{:7.3f}] {:}".format(float(time.time() - start_time), msg))
    else:
        print ("[{:}] {:}".format(time.time() - start_time, msg))


"""
Stub of the machine.Pin class
"""
class Pin:

    # pin modes
    IN  = 'IN'
    OUT = 'OUT'
    OPEN_DRAIN = 'OPEN_DRAIN'
    ALT = 'ALT'
    ALT_OPEN_DRAIN = 'ALT_OPEN_DRAIN'

    # pin oull
    PULL_UP    = 'PULL_UP'
    PULL_DOWM  = 'PULL_DOWN'

    # pin interrupt modes
    IRQ_FALLING         = 'IRQ_FALLING'
    IRQ_RISING          = 'IRQ_RISING'
    IRQ_RISING_FALLING  = 'IRQ_RISING_FALLING'
    IRQ_LOW_LEVEL       = 'IRQ_LOW_LEVEL'
    IRQ_HIGH_LEVEL      = 'IRQ_HIGH_LEVEL'

    # pin drive
    LOW_POWER    = 'LOW_POWER'
    MED_POWER    = 'MED_POWER'
    HIGH_POWER   = 'HIGH_POWER'

    def __init__(self, pin, mode=OUT, pull=None, drive=MED_POWER, alt=-1):
        self.pin = pin
        self.val = 0
        pyblog ('[Pin] Init %s with mode=%s pull=%s drive=%s, alt=%s' % (pin, mode, pull if pull else 'None', drive, alt))

    def __call__(self, val=None):
        return self.__value(val)

    def __value(self, val):
        if val is not None:
            self.val = val
            pyblog ('[Pin] %s value set to %d' % (self.pin, self.val))
        else:
            pyblog ('[Pin] %s value is %d' % (self.pin, self.val))
            return self.val

    def value(self, val=None):
        return self.__value(val)

"""
Stub of the machine.Timer class
"""
class Timer:

    A               = 'A'
    B               = 'B'
    ONE_SHOT        = 'ONE_SHOT'
    PERIODIC        = 'PERIODIC'
    EDGE_COUNT      = 'EDGE_COUNT'
    EDGE_TIME       = 'EDGE_TIME'
    PWM             = 'PWM'
    POSITIVE        = 'POSITIVE'
    NEGATIVE        = 'NEGATIVE'

    def __init__(self, timer, mode):
        self.timer = timer
        self.mode = mode
        pyblog ('[Timer] Init Timer %d with %s mode' % (timer, mode))

    def channel(self, channel, freq=None, period=None, polarity=POSITIVE, duty_cycle=0):
        if (freq is None and period is None) or (freq is not None and period is not None):
            raise ValueError('[Timer] Either frequency or period need to be given')
        self.channel = TimerChannel(channel, freq, period, polarity, duty_cycle)
        pyblog ('[Timer] New TimerChannel from Timer %d' % self.timer)
        return self.channel


class TimerChannel:

    def __init__(self, channel, freq=None, period=None, polarity=Timer.POSITIVE, duty_cycle=0):
        self.channel = channel
        self.freq = freq
        self.duty = duty_cycle
        pyblog ('[TimerChannel] New TimerChannel %s with freq=%d, period=%d, polarity=%s, duty_cycle=%d' % 
               (channel, freq if freq is not None else 0, period if period is not None else 0, polarity, duty_cycle))

    def duty_cycle(self, duty_cycle):
        self.duty = duty_cycle
        pyblog ('[TimerChannel] Channel %s duty cycle set to %d' % (self.channel, duty_cycle))


"""
Stub of the machine.ADC class
"""
class ADC:

    def __init__(self, id=0, bits=12):
        if not id == 0 or not bits == 12:
            raise ValueError("Cannot create ADC%d with %d bits resolution" % (id, bits))
        pyblog ('[ADC%d] Init with %d bits' % (id, bits))

    def channel(self, channel=None, pin=None):
        pyblog ('[ADC] Create channel {} on pin {}'.format(channel, pin))
        self.channel = ADCChannel(channel, pin)
        return self.channel


class ADCChannel:

    def __init__(self, channel=None, pin=None):
        self.channel = channel
        self.pin = pin
        self.val = 128
        if (channel and pin) or not (channel or pin):
            raise ValueError("Incorrect ADC channel-pin combination {}-{}".format(channel, pin))

    def __call__(self, val=None):
        return self.value()

    def value(self):
        pyblog ('[ADCChannel] Read channel {} pin {} value {}'.format(self.channel, self.pin, self.val))
        return self.val


"""
Stub of the machine.WDT class
"""
class WDT:

    def __init__(self, id=0, timeout=None):
        self.timeout = timeout
        pyblog ('[WDT] Init with %d timeout' % self.timeout)

    def feed(self):
        pyblog ('[WDT] Watchdog kicked just now')


"""
Stub of the machine.HeartBeat class
"""
class HeartBeat:

    def __init__(self):
        pyblog ('[HeartBeat] Create instance')

    def enable(self):
        pyblog ('[HeartBeat] Enabled')

    def disable(self):
        pyblog ('[HeartBeat] Disabled')

"""
Stub of the machine functions
"""
def idle():
    pass

def sleep():
    pass

def deepsleep():
    pass

"""
Time module extensions
"""
def sleep_ms(msecs):
    if floating_point:
        time.sleep(msecs / 1000)
    else:
        time.sleep(msecs // 1000)

def ticks_ms():
    return int(time.time() * 1000)

def ticks_diff(start, end):
    return end - start;

setattr(sys.modules['time'], 'sleep_ms', sleep_ms)
setattr(sys.modules['time'], 'ticks_ms', ticks_ms)
setattr(sys.modules['time'], 'ticks_diff', ticks_diff)
