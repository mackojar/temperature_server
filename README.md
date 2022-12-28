Temperature server for ESP8266 running Micropython.
Temperature is read from two ds18b20 connected to single data wire (1-wire).

Create settings.py file:
```
WIFI_NAME='your WIFI SSID'
WIFI_PASS='your WIFI password'
WIFI_IP='your static IP'
WIFI_MASK='your IP mask'
WIFI_GW='your gateway'
WIFI_DNS='your DNS'
```

Copy your files to ESP8266 and reboot it:
```
ampy -p /dev/tty.<your port> put settings.py
ampy -p /dev/tty.<your port> put main.py
ampy -p /dev/tty.<your port> put boot.py
ampy -p /dev/tty.<your port> put wifi.py
```

Or just run your program:
```
ampy -p /dev/tty.<your port> run main.py
```
