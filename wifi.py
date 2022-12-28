import machine
import network, time
import settings

def connectWIFI():
  led = machine.Pin(2, machine.Pin.OUT)

  # Deactivate AP mode
  wlan_ap = network.WLAN(network.AP_IF)
  wlan_ap.active(False)

  wlan_sta = network.WLAN(network.STA_IF)
  wlan_sta.active(True)
  wlan_sta.ifconfig((settings.WIFI_IP, settings.WIFI_MASK, settings.WIFI_GW, settings.WIFI_DNS))
  wlan_sta.connect(settings.WIFI_NAME, settings.WIFI_PASS)

  led_value: bool = True
  while not wlan_sta.isconnected():
    print("Waiting for WIFI connection...")
    led.value(1 if led_value else 0)
    led_value = not led_value
    time.sleep_ms(500)

  led.value(0)
  return wlan_sta
