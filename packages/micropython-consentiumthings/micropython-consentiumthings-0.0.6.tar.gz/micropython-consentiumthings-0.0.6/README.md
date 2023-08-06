# ConsentiumThingsPy

Passing tests on ESP 8266 and ESP 32

Developed by Debjyoti Chowdhury from ConsentiumInc


## Installing dependencies and main library

```python

import upip
import network
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("", "")
station.isconnected()
print(station.ifconfig())

upip.install('micropython-urequests')
upip.install('micropython-consentiumthings')

```

## Examples of How To Use 

Creating A Server

```python
from ConsentiumThings import ThingsUpdate
import utime

api_key = ""

board = ThingsUpdate(key=api_key)

board.initWiFi("", "")

sensor_val = [1, 2, 3, 4, 5, 6, 7]
info_buff = ["a", "b", "c", "d", "e", "f", "g"]

while True:
    r = board.sendREST(sensor_val=sensor_val, info_buff=info_buff)
    print(r.text)
    utime.sleep(5)
```
