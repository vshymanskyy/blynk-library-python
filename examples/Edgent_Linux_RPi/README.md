
**Warning:** Do not use SSH/remote desktop for these commands, as your network connection can become unavailable.
Connect screen and keyboard to your RPi, or use a serial adapter to access console.


## Install NetworkManager

NetworkManager provides detection and configuration for systems to automatically connect to different wired and wireless networks.

```sh
sudo apt-get install network-manager
sudo systemctl disable dhcpcd
sudo systemctl stop dhcpcd
sudo reboot
```

After reboot, check if `nmcli works` with WiFi. For example, perform scanning:
```sh
$ sudo nmcli dev wifi
IN-USE  SSID          MODE   CHAN  RATE        SIGNAL  BARS  SECURITY
        myNetwork     Infra  6     270 Mbit/s  75      ▂▄▆_  WPA2
        otherNet      Infra  9     405 Mbit/s  29      ▂___  WPA1 WPA2
```

With `nmcli`, you can also easily connect to a wifi network (if needed):

```sh
sudo nmcli device wifi con "my-ssid" password "my-pass"
```

## Troubleshooting
1. Make sure that your `wlan` interface is not configured via `/etc/network/interfaces`. NetworkManager ignores such interfaces.
2. Check if your WiFi is blocked using `rfkill list`. Run `rfkill unblock wifi` to unblock it.


## Install Edgent prerequisites

```sh
pip3 install --upgrade https://github.com/vshymanskyy/nmcli/archive/master.zip
pip3 install --upgrade RPi.GPIO
```

## Attach config reset button

Connect button between gpio16 and GND.
Hold the button for 10 seconds to reset config.

## Run script manually

```
pyhton3 beemate.py
```

Alternatively, you can configure RPi to auto-run `main.py` on boot.
