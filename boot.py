# This file is executed on every boot (including wake-boot from deepsleep)
# #import esp
# #esp.osdebug(None)
# import uos, machine
# #uos.dupterm(None, 1) # disable REPL on UART(0)
# import gc
# #import webrepl
# #webrepl.start()
# gc.collect()

import gc
from wifi import connectWIFI

gc.collect()
print("Booting...")
wlan_sta = connectWIFI()
print("WIFI Connection successful")
print(wlan_sta.ifconfig())
