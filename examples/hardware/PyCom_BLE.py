"""
    THIS EXAMPLE IS NOT FINISHED YET.
(You can use this for educational purposes)
"""

from network import Bluetooth
from binascii import unhexlify
from BlynkLib import BlynkProtocol
import machine, time

BLYNK_AUTH = "YourAuthToken"

def unhex(s):
    return bytes(reversed(unhexlify(s.replace('-',''))))


class BlynkBLE(BlynkProtocol):
    def __init__(self, auth, **kwargs):
        self.bout = b''
        BlynkProtocol.__init__(self, auth, **kwargs)

    def connect(self):
        bluetooth = Bluetooth()
        bluetooth.set_advertisement(name='Blynk')

        def conn_cb(bt):
            events = bt.events()
            if  events & Bluetooth.CLIENT_CONNECTED:
                self.bout = b''
                print("Client connected")
            elif events & Bluetooth.CLIENT_DISCONNECTED:
                print("Client disconnected")
                BlynkProtocol.disconnect(self)

        bluetooth.callback(trigger=Bluetooth.CLIENT_CONNECTED | Bluetooth.CLIENT_DISCONNECTED, handler=conn_cb)

        nus = bluetooth.service(uuid=unhex('6E400001-B5A3-F393-E0A9-E50E24DCCA9E'), isprimary=True, nbr_chars=2)
        self.rx = nus.characteristic(uuid=unhex('6E400002-B5A3-F393-E0A9-E50E24DCCA9E'),
                                     properties=Bluetooth.PROP_WRITE | Bluetooth.PROP_WRITE_NR,
                                     value='')
        self.tx = nus.characteristic(uuid=unhex('6E400003-B5A3-F393-E0A9-E50E24DCCA9E'),
                                     properties=Bluetooth.PROP_READ | Bluetooth.PROP_NOTIFY,
                                     value='')

        bluetooth.advertise(True)

        def rx_cb(chr):
            data = chr.value()
            print('>', data)
            self.process(bytes(data))

        def tx_subsc(chr):
            print("Client subscribed", chr)
            BlynkProtocol.connect(self, login=False)

        self.tx.callback(trigger=Bluetooth.CHAR_SUBSCRIBE_EVENT, handler=tx_subsc)
        self.rx.callback(trigger=Bluetooth.CHAR_WRITE_EVENT, handler=rx_cb)

    def _write(self, data):
        self.bout += data

    def run(self):
        self.process()

        while len(self.bout):
            data = self.bout[:20]
            self.bout = self.bout[20:]
            print('<', data)
            self.tx.value(data)

blynk = BlynkBLE(BLYNK_AUTH)

@blynk.on("connected")
def blynk_connected(ping):
    print('Blynk ready. Ping:', ping, 'ms')

def runLoop():
    while True:
        blynk.run()
        time.sleep(0.1)
        #machine.idle()

# Run blynk in the main thread:
runLoop()
