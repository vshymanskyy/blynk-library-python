
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qsl
from contextlib import suppress
import sys, time
import nmcli
import json
import binascii

def log(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class WiFi:
    def __init__(self):
        #nmcli.disable_use_sudo()

        wifi_devices = list(filter(lambda x: x.device_type=="wifi", nmcli.device()))
        assert(len(wifi_devices) > 0)
        self.device = wifi_devices[0].device
        details = nmcli.device.show(self.device)
        self.mac_addr = details["GENERAL.HWADDR"]
        self.ap_name = "Blynk AP"
        log("WiFi devices:", wifi_devices)
        log("WiFi MAC:    ", self.mac_addr)

    def mac_address(self):
        return self.mac_addr

    def set_hostname(self, name):
        nmcli.general.set_hostname(name)
        log("Hostname:    ", name)

    def _cleanup(self, conn):
        with suppress(Exception):
            nmcli.connection.down(conn)
        with suppress(Exception):
            nmcli.connection.delete(conn)

    def create_ap(self, ssid):
        self.remove_ap()
        nmcli.connection.add(name = self.ap_name, conn_type = "wifi", options = {
            "ssid": ssid,
            "ipv4.method": "shared",
            "ipv4.addresses": "192.168.4.1/24",
            "802-11-wireless.mode": "ap",
            "802-11-wireless.band": "bg"
        })
        nmcli.connection.up(self.ap_name)
        log("AP SSID:     ", ssid)

    def remove_ap(self):
        self._cleanup(self.ap_name)

    def scan(self):
        results = []
        for net in nmcli.device.wifi():
            signal = max(30, min(net.signal, 100))
            rssi_max = -20
            rssi_min = -90
            rssi = int(-((((rssi_max - rssi_min) * (signal - 100)) / -70) - rssi_max))
            results.append({
                "ssid":     net.ssid,
                "bssid":    net.bssid,
                "freq":     net.freq,
                "rssi":     rssi,
                "sec":      net.security if len(net.security) else "OPEN",
                "ch":       net.chan
            })

        return results

    def restart(self):
        nmcli.radio.wifi_off()
        nmcli.radio.wifi_on()

    def connect(self, ssid, password):
        self._cleanup(ssid)
        nmcli.device.wifi_connect(ssid, password)

class HTTPHandler(BaseHTTPRequestHandler):
    def _reply_json(self, data):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        return

    def do_GET(self):
        o = urlparse(self.path)
        q = dict(parse_qsl(o.query))
        if o.path == "/board_info.json":
            self._reply_json(self.server.blynk_info)
        elif o.path == "/wifi_scan.json":
            self._reply_json(self.server.wifi_networks)
        elif o.path == "/config":
            q["auth"]   = q.pop("blynk")
            q["server"] = q.pop("host")
            q["port"]   = int(q.pop("port"))
            q["port_ssl"] = int(q.pop("port_ssl"))
            if "save" in q:
                self._reply_json({"status":"ok","msg":"Configuration saved"})
            else:
                self._reply_json({"status":"ok","msg":"Trying to connect..."})
            self.server.blynk_config = q
        else:
            self.send_error(404)

def provision(board, tmpl_id, fw_ver, prefix = "Blynk"):
    wifi = WiFi()

    wifi_networks = wifi.scan()

    suffix = format(binascii.crc32(wifi.mac_address().encode() * 4) & 0xFFFFF, 'X')
    my_ssid = prefix + " " + board + "-" + suffix

    config = None
    try:
        wifi.create_ap(my_ssid)
        with HTTPServer(("0.0.0.0", 11080), HTTPHandler) as httpd:
            httpd.blynk_info = {
                "board":    board,
                "tmpl_id":  tmpl_id,
                "fw_type":  tmpl_id,
                "fw_ver":   fw_ver,
                "ssid":     my_ssid,
                "bssid":    wifi.mac_address(),
                "wifi_scan": True,
                "static_ip": False
            }
            httpd.wifi_networks = wifi_networks
            httpd.blynk_config = None

            log("Waiting for Blynk App connection...")
            while httpd.blynk_config is None:
                httpd.handle_request()
            config = httpd.blynk_config
    finally:
        wifi.remove_ap()

    if config is not None:
        wifi.set_hostname(my_ssid.replace(" ", "-"))
        wifi.restart()
        time.sleep(3)
        wifi.scan()
        time.sleep(1)
        wifi.connect(config['ssid'], config['pass'])
        time.sleep(1)

    return config

if __name__ == "__main__":
    config = provision(sys.argv[1], sys.argv[2], sys.argv[3])
    print(json.dumps(config))
