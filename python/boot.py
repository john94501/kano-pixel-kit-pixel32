print('Booting...')
import PixelKit as kit
from time import sleep

kit.set_background([10, 5, 0])
kit.render()
sleep(0.5)

try:
    import wifi_config as CONF
except:
    with open('wifi_config.py', 'w') as f:
        f.write('SSID=None\n')
        f.write('PASSWORD=None\n')
        f.close()
    import wifi_config as CONF

import network
import utime

ap = network.WLAN(network.AP_IF)
sta = network.WLAN(network.STA_IF)

def draw_ip(ip_str='0.0.0.0', bg=[0, 0, 0], color=[10, 0, 0]):
    ip_bin = []
    for i in ip_str.split('.'):
      ip_bin.append(bin(int(i))[2:])
    output = []
    for ip in ip_bin:
      o = []
      for i in range(1, 9):
        try:
          o.insert(0, ip[-i])
        except Exception as e:
          o.insert(0, '0')
      output.append(o)
    for y, line in enumerate(output):
      for x, pixel in enumerate(line):
        if pixel == '1':
          kit.set_pixel(4+x, 2+y, color)
        else:
          kit.set_pixel(4+x, 2+y, bg)

def start_ap():
    sta.active(False)
    ap.active(True)
    kit.set_background([0, 0, 10])
    draw_ip(ap.ifconfig()[0])
    kit.render()

def connect(ssid, password):
    ap.active(False)
    sta.active(True)
    sta.connect(ssid, password)
    timeout = 50
    while not sta.isconnected():
        utime.sleep_ms(100)
        timeout -= 1
        if timeout == 0:
            break
    if sta.isconnected():
        print('Connected', sta.ifconfig())
        kit.set_background([0, 10, 0])
        draw_ip(sta.ifconfig()[0])
        kit.render()
    else:
        print('Not connected')
        kit.set_background([10, 0, 0])
        draw_ip()
        kit.render()

if kit.button_a.value() == 0:
    print('Forcing AP mode')
    start_ap()
elif CONF.SSID != None and CONF.PASSWORD != None:
    print('Connecting to wifi network')
    connect(CONF.SSID, CONF.PASSWORD)
else:
    print('Empty config')
    start_ap()
