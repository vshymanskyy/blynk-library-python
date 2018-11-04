# Copyright (c) 2015-2018 Volodymyr Shymanskyy. See the file LICENSE for copying permission.

_VERSION = "0.2.0"

import struct
import time

try:
    import machine
    gettime = lambda: time.ticks_ms()
except ImportError:
    const = lambda x: x
    gettime = lambda: int(time.time() * 1000)

def dummy(*args):
    pass 

MSG_RSP = const(0)
MSG_LOGIN = const(2)
MSG_PING  = const(6)

MSG_TWEET = const(12)
MSG_EMAIL = const(13)
MSG_NOTIFY = const(14)
MSG_BRIDGE = const(15)
MSG_HW_SYNC = const(16)
MSG_INTERNAL = const(17)
MSG_PROPERTY = const(19)
MSG_HW = const(20)
MSG_EVENT_LOG = const(64)

MSG_REDIRECT  = const(41)  # TODO: not implemented
MSG_DBG_PRINT  = const(55) # TODO: not implemented

STA_SUCCESS = const(200)
STA_INVALID_TOKEN = const(9)

DISCONNECTED = const(0)
CONNECTING = const(1)
CONNECTED = const(2)

print("""
    ___  __          __
   / _ )/ /_ _____  / /__
  / _  / / // / _ \\/  '_/
 /____/_/\\_, /_//_/_/\\_\\
        /___/ for Python v""" + _VERSION + "\n")

class BlynkProtocol:
    def __init__(self, auth, heartbeat=10, buffin=1024, log=None):
        self.callbacks = {}
        self.heartbeat = heartbeat*1000
        self.buffin = buffin
        self.log = log or dummy
        self.auth = auth
        self.connect()

    def on(self, evt, func):
        self.callbacks[evt] = func

    def emit(self, evt, *args):
        self.log("Event:", evt, "->", *args)
        if evt in self.callbacks:
            self.callbacks[evt](*args)
        
    def virtual_write(self, pin, val):
        self._send(self._format_msg(MSG_HW, 'vw', pin, val))

    def set_property(self, pin, prop, val):
        self._send(self._format_msg(MSG_PROPERTY, pin, prop, val))

    def sync_virtual(self, pin):
        if self.state == CONNECTED:
            self._send(self._format_msg(MSG_HW_SYNC, 'vr', pin))

    def notify(self, msg):
        self._send(self._format_msg(MSG_NOTIFY, msg))

    def log_event(self, event, descr=None):
        if descr==None:
            self._send(self._format_msg(MSG_EVENT_LOG, event))
        else:
            self._send(self._format_msg(MSG_EVENT_LOG, event, descr))

    def sendMsg(self, cmd, id=None, *args):
        payload = ('\0'.join(map(str, args))).encode('ascii')
        if id == None:
            id = self.msg_id
            self.msg_id += 1
            if self.msg_id > 0xFFFF:
                self.msg_id = 1
        
        self.log('<', cmd, id, '|', *args)
        msg = struct.pack("!BHH", cmd, id, len(payload)) + payload
        self.lastSend = gettime()
        self._send(msg)

    def connect(self):
        self.msg_id = 1
        (self.lastRecv, self.lastSend, self.lastPing) = (gettime(), 0, 0)
        self.bin = b""
        self.state = CONNECTING
        self.sendMsg(MSG_LOGIN, None, self.auth)

    def disconnect(self):
        self.state = DISCONNECTED
        self.emit('disconnected')

    def process(self, data=b''):
        if not (self.state == CONNECTING or self.state == CONNECTED):
            return
        now = gettime()
        if now - self.lastRecv > self.heartbeat+(self.heartbeat/2):
            return self.disconnect()
        if (now - self.lastPing > self.heartbeat/10 and
            (now - self.lastSend > self.heartbeat or
             now - self.lastRecv > self.heartbeat)):
            self.sendMsg(MSG_PING)
            self.lastPing = now
        
        if data != None and len(data):
            self.bin += data

        while True:
            if len(self.bin) < 5: return
            
            cmd, i, msg_len = struct.unpack("!BHH", self.bin[:5])
            if i == 0: return self.disconnect()
                      
            self.lastRecv = now
            if cmd == MSG_RSP:
                self.bin = self.bin[5:]

                self.log('>', cmd, i, '|', msg_len)
                if self.state == CONNECTING and i == 1:
                    if msg_len == STA_SUCCESS:
                        self.state = CONNECTED
                        ping = now - self.lastSend
                        self.sendMsg(MSG_INTERNAL, None, 'ver', _VERSION, 'h-beat', self.heartbeat//1000, 'buff-in', self.buffin, 'dev', 'python')
                        self.emit('connected', ping)
                    elif msg_len == STA_INVALID_TOKEN:
                        print("Invalid auth token")
                        self.disconnect()
                    else:
                        self.disconnect()
            else:
                if msg_len >= self.buffin:
                    print("Cmd too big: ", msg_len)
                    return self.disconnect()
            
                if len(self.bin) < 5+msg_len: return
                
                data = self.bin[5:5+msg_len]
                self.bin = self.bin[5+msg_len:]

                args = list(map(lambda x: x.decode('ascii'), data.split(b'\0')))

                self.log('>', cmd, i, '|', ','.join(args))
                if cmd == MSG_PING:
                    self.sendMsg(MSG_RSP, i, STA_SUCCESS) #TODO
                elif cmd == MSG_HW or cmd == MSG_BRIDGE:
                    if args[0] == 'vw':
                        self.emit("V"+args[1], args[2:])
                    elif args[0] == 'vr':
                        self.emit("readV"+args[1])
                elif cmd == MSG_INTERNAL:
                    pass
                else:
                    print("Unexpected command: ", cmd)
                    return self.disconnect()

    def VIRTUAL_READ(blynk, pin):
        class Decorator():
            def __init__(self, func):
                self.func = func
                blynk.callbacks["readV"+str(pin)] = func
            def __call__(self):
                return self.func()
        return Decorator

    def VIRTUAL_WRITE(blynk, pin):
        class Decorator():
            def __init__(self, func):
                self.func = func
                blynk.callbacks["V"+str(pin)] = func
            def __call__(self):
                return self.func()
        return Decorator

import socket

class Blynk(BlynkProtocol):
    def __init__(self, auth, **kwargs):
        BlynkProtocol.__init__(self, auth, **kwargs)

    def connect(self):
        try:
            self.conn = socket.socket()
            self.conn.connect(socket.getaddrinfo("blynk-cloud.com", 80)[0][4])
            self.conn.settimeout(0.05)
            BlynkProtocol.connect(self)
        except:
            raise ValueError('connection with the Blynk servers failed')

    def _send(self, data):
        self.conn.send(data)

    def run(self):
        data = b''
        try:
            data = self.conn.recv(self.buffin)
        except KeyboardInterrupt:
            raise
        except OSError:
            pass
        self.process(data)

