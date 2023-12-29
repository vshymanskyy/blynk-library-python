# Copyright (c) 2015-2019 Volodymyr Shymanskyy. See the file LICENSE for copying permission.

__version__ = "1.0.0"

import socket
import struct
import sys
import time

IOError = OSError

try:
    import machine
    gettime = lambda: time.ticks_ms()
    SOCK_TIMEOUT = 0
except ImportError:
    const = lambda x: x
    gettime = lambda: int(time.time() * 1000)
    SOCK_TIMEOUT = 0.05

def dummy(*args):
    pass

MSG_RSP = const(0)
MSG_LOGIN = const(2)
MSG_PING  = const(6)

MSG_TWEET = const(12)
MSG_NOTIFY = const(14)
MSG_BRIDGE = const(15)
MSG_HW_SYNC = const(16)
MSG_INTERNAL = const(17)
MSG_PROPERTY = const(19)
MSG_HW = const(20)
MSG_HW_LOGIN = const(29)
MSG_EVENT_LOG = const(64)

MSG_REDIRECT  = const(41)  # TODO: not implemented
MSG_DBG_PRINT  = const(55) # TODO: not implemented

STA_SUCCESS = const(200)
STA_INVALID_TOKEN = const(9)

DISCONNECTED = const(0)
CONNECTING = const(1)
CONNECTED = const(2)
RETRIES_TX_MAX_NUM = const(3)
RETRIES_TX_DELAY = const(2)


class BlynkError(Exception):
    pass


class RedirectError(Exception):
    def __init__(self, server, port):
        self.server = server
        self.port = port


print("""
    ___  __          __
   / _ )/ /_ _____  / /__
  / _  / / // / _ \\/  '_/
 /____/_/\\_, /_//_/_/\\_\\
        /___/ for Python v""" + __version__ + " (" + sys.platform + ")\n")

class EventEmitter:
    def __init__(self):
        self._cbks = {}

    def on(self, evt, f=None):
        if f:
            self._cbks[evt] = f
        else:
            def D(f):
                self._cbks[evt] = f
                return f
            return D

    def emit(self, evt, *a, **kv):
        if evt in self._cbks:
            self._cbks[evt](*a, **kv)


class BlynkProtocol(EventEmitter):
    def __init__(self, auth, tmpl_id=None, fw_ver=None, heartbeat=5, buffin=1024, log=None):
        EventEmitter.__init__(self)
        self._init_variables(auth, tmpl_id, fw_ver, heartbeat, buffin, log)
        self.connect()

    def _init_variables(self, auth, tmpl_id, fw_ver, heartbeat, buffin, log):
        self.lastRecv = None
        self.heartbeat = heartbeat*1000
        self.buffin = buffin
        self.log = log or dummy
        self.auth = auth
        self.tmpl_id = tmpl_id
        self.fw_ver = fw_ver
        self.state = DISCONNECTED

    def virtual_write(self, pin, *val):
        self._send(MSG_HW, 'vw', pin, *val)

    def send_internal(self, pin, *val):
        self._send(MSG_INTERNAL,  pin, *val)

    def set_property(self, pin, prop, *val):
        self._send(MSG_PROPERTY, pin, prop, *val)

    def sync_virtual(self, *pins):
        self._send(MSG_HW_SYNC, 'vr', *pins)

    def log_event(self, *val):
        self._send(MSG_EVENT_LOG, *val)

    def _send(self, cmd, *args, **kwargs):
        self.check_and_reconnect()
        id, data, dlen = self._prepare_send_variables(cmd, args, kwargs)
        self._log_and_send_msg(cmd, id, args, data, dlen)

    def _prepare_send_variables(self, cmd, args, kwargs):
        if 'id' in kwargs:
            id = kwargs.get('id')
        else:
            id = self.msg_id
            self.msg_id += 1
            if self.msg_id > 0xFFFF:
                self.msg_id = 1
        if cmd == MSG_RSP:
            data = b''
            dlen = args[0]
        else:
            data = ('\0'.join(map(str, args))).encode('utf8')
            dlen = len(data)
        return id, data, dlen

    def _log_and_send_msg(self, cmd, id, args, data, dlen):
        self.log('<', cmd, id, '|', *args)
        msg = struct.pack("!BHH", cmd, id, dlen) + data
        self.lastSend = gettime()
        self._write(msg)

    def connect(self):
        if self.state != DISCONNECTED: return
        self._init_connect_variables()
        self._send(MSG_HW_LOGIN, self.auth)

    def _init_connect_variables(self):
        self.msg_id = 1
        (self.lastRecv, self.lastSend, self.lastPing) = (gettime(), 0, 0)
        self.bin = b""
        self.state = CONNECTING

    def is_disconnected(self):
        return self.state == DISCONNECTED

    def reconnected(self):
        self.disconnect()
        self.connect()

    def check_and_reconnect(self):
        if self.is_disconnected():
            self.connect()

        if self._is_device_offline():
            self.reconnected()

    def _is_device_offline(self):
        now = gettime()
        return now - self.lastRecv > self.heartbeat+(self.heartbeat//2)

    def disconnect(self):
        if self.state == DISCONNECTED:
            return
        self._init_disconnect_variables()
        self.emit('disconnected')

    def _init_disconnect_variables(self):
        self.bin = b""
        self.state = DISCONNECTED

    def process(self, data=None):
        if not (self.state == CONNECTING or self.state == CONNECTED):
            return
        if self._is_device_offline():
            return self.reconnected()
        self._send_ping()
        self._process_data(data)

    def _send_ping(self):
        now = gettime()
        if (now - self.lastPing > self.heartbeat//10 and
                (now - self.lastSend > self.heartbeat or
                 now - self.lastRecv > self.heartbeat)):
            self._send(MSG_PING)
            self.lastPing = now

    def _process_data(self, data):
        if data is not None and len(data):
            self.bin += data
        self._parse_commands()

    def _parse_commands(self):
        while True:
            if len(self.bin) < 5:
                break
            cmd, i, dlen = self._unpack_bin()
            if self._process_msg_rsp(cmd, i, dlen):
                continue
            if self._check_command_length(dlen):
                break
            data = self.bin[5:5+dlen]
            self.bin = self.bin[5+dlen:]
            self.process_command(cmd, i, data)

    def _unpack_bin(self):
        cmd, i, dlen = struct.unpack("!BHH", self.bin[:5])
        if i == 0:
            self.disconnect()
        self.lastRecv = gettime()
        return cmd, i, dlen

    def _process_msg_rsp(self, cmd, i, dlen):
        if cmd == MSG_RSP:
            self.bin = self.bin[5:]
            self.log('>', cmd, i, '|', dlen)
            if self.state == CONNECTING and i == 1:
                self._handle_connecting(dlen)
            return True
        return False

    def _handle_connecting(self, dlen):
        if dlen == STA_SUCCESS:
            self._handle_connection_success()
        else:
            if dlen == STA_INVALID_TOKEN:
                self.emit("invalid_auth")
                print("Invalid auth token")
            self.disconnect()

    def _handle_connection_success(self):
        self.state = CONNECTED
        dt = gettime() - self.lastSend
        info = self._create_connection_info()
        self._send(MSG_INTERNAL, *info)
        try:
            self.emit('connected', ping=dt)
        except TypeError:
            self.emit('connected')

    def _create_connection_info(self):
        info = ['ver', __version__, 'h-beat', self.heartbeat//1000, 'buff-in', self.buffin, 'dev', sys.platform+'-py']
        if self.tmpl_id:
            info.extend(['tmpl', self.tmpl_id])
            info.extend(['fw-type', self.tmpl_id])
        if self.fw_ver:
            info.extend(['fw', self.fw_ver])
        return info

    def _check_command_length(self, dlen):
        if dlen >= self.buffin:
            print("Cmd too big: ", dlen)
            self.disconnect()
            return True
        return False

    def process_command(self, cmd, i, data):
        args = list(map(lambda x: x.decode('utf8'), data.split(b'\0')))
        self.log('>', cmd, i, '|', ','.join(args))
        if cmd == MSG_PING:
            self._send(MSG_RSP, STA_SUCCESS, id=i)
        elif cmd == MSG_HW or cmd == MSG_BRIDGE:
            self._process_hw_command(args)
        elif cmd == MSG_INTERNAL:
            self.emit("internal:"+args[0], args[1:])
        elif cmd == MSG_REDIRECT:
            self.emit("redirect", args[0], int(args[1]))
        else:
            print("Unexpected command: ", cmd)
            self.disconnect()

    def _process_hw_command(self, args):
        if args[0] == 'vw':
            self.emit("V"+args[1], args[2:])
            self.emit("V*", args[1], args[2:])


class Blynk(BlynkProtocol):
    def __init__(self, auth, server='blynk.cloud', insecure=False, port=None, **kwargs):
        self.conn = None
        self.insecure = insecure
        self.server = server
        self.port = port if port else 80 if self.insecure else 443
        BlynkProtocol.__init__(self, auth, **kwargs)
        self.on('redirect', self.redirect)

    def redirect(self, server, port):
        self.server = server
        self.port = port
        self.disconnect_and_connect()

    def disconnect_and_connect(self):
        self.disconnect()
        self.connect()

    def connect(self):
        print('Connecting to %s:%d...' % (self.server, self.port))
        end_time = time.time() + 0.5
        while not (self.state == CONNECTED):
            if self.state == DISCONNECTED:
                try:
                    self.create_socket()
                    BlynkProtocol.connect(self)
                    return True
                except BlynkError as b_err:
                    self.disconnect()
                except RedirectError as r_err:
                    self.disconnect()

            if time.time() >= end_time:
                return False

    def create_socket(self):
        s = socket.socket()
        try:
            s.connect(socket.getaddrinfo(self.server, self.port)[0][-1])
            if self.insecure:
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.conn = s
            else:
                try:
                    import ussl
                    ssl_context = ussl
                except ImportError:
                    import ssl
                    ssl_context = ssl.create_default_context()
                self.conn = ssl_context.wrap_socket(s, server_hostname=self.server)
                try:
                    self.conn.settimeout(SOCK_TIMEOUT)
                except:
                    s.settimeout(SOCK_TIMEOUT)
        except OSError:
            pass


    def _write(self, data):
        retries = RETRIES_TX_MAX_NUM
        while retries > 0:
            try:
                retries -= 1
                self._last_send_time = gettime()
                self.conn.write(data)
                break
            except (IOError, OSError):
                time.sleep(RETRIES_TX_DELAY/1000)


    def run(self):
        self.check_and_reconnect()

        try:
            data = self.conn.read(self.buffin)
            self.process(data)
        except KeyboardInterrupt:
            raise
        except BlynkError as b_err:
            self.log(b_err)
            self.disconnect()
        except Exception as g_exc:
            self.log(g_exc)



