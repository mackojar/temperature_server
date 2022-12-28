import time, network, socket, sys, json
from machine import Pin
import onewire, ds18x20
from wifi import connectWIFI

UTF_8: str = 'utf-8'

def initTemperature():
  print(f"Starting temperature readings...")
  ow = onewire.OneWire(Pin(4))
  ds = ds18x20.DS18X20(ow)
  print(f"Devices on the wire: {ow.scan()}")
  return ds

def readTemperatures(ds) -> dict[str, float]:
  roms = ds.scan()
  ds.convert_temp()
  time.sleep_ms(750)
  temps: dict[str, float] = {}
  for rom in roms:
    romString = ''.join('{:02x}'.format(x) for x in rom)
    temps[romString] = ds.read_temp(rom)
  return temps

def initAPIServer() -> socket:
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.bind(('', 80))
  s.listen()
  return s

def sendResponse(conn, httpStatusString: str, contentType: str, body: str):
  conn.send(bytes('HTTP/1.1 %s\n' % httpStatusString, UTF_8))
  conn.send(bytes('Content-Type: %s\n' % contentType, UTF_8))
  conn.send(b'Connection: close\n\n')
  conn.sendall(bytes(body, UTF_8))

def handleConnections(socketServer: socket, ds):
  while True:
    conn, addr = socketServer.accept()
    try:
      print('Got a connection from %s' % str(addr))
      requestBytes = conn.recv(1024)
      requestString = requestBytes.decode(UTF_8)
      print('Content: %s' % requestString)
      isTemperatureRequest = requestString.find('GET /temp HTTP/')
      if isTemperatureRequest == 0:
        temps = readTemperatures(ds)
        tempsString = json.dumps(temps)
        print('Temps: %s' % tempsString)
        sendResponse(conn, '200 OK', 'application/json', tempsString)
      else:
        sendResponse(conn, '404 Not Found', 'text/html', 'Resource not found')
    except Exception as e1:
      try:
        sendResponse(conn, '404 Internal error', 'text/html', 'Processing error: %s' % e1)
      except Exception as e2:
        sys.print_exception(e2)
      raise e1
    finally:
      conn.close()

def main():
  ds = initTemperature()
  station = network.WLAN(network.STA_IF)
  socketServer: socket = initAPIServer()
  while True:
    try:
      if station.isconnected() == False:
        station = connectWIFI()
        socketServer = initAPIServer()
      handleConnections(socketServer, ds)
    except Exception as e:
      sys.print_exception(e)

main()
