import network, time
from machine import Pin
from umqtt.simple import MQTTClient

SSID = "DamoDob"
PASSWORD = "Error303"
BROKER = "100.83.12.97"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
while not wlan.isconnected():
    time.sleep(0.5)
print("IP:", wlan.ifconfig()[0])

led = Pin(2, Pin.OUT)

def on_msg(topic, msg):
    print(topic, msg)
    if topic == b"esp32/led":
        led.value(1 if msg == b"on" else 0)

client = MQTTClient("esp32-client", BROKER)
client.set_callback(on_msg)
client.connect()
client.subscribe(b"esp32/led")

last = time.ticks_ms()
while True:
    client.check_msg()
    if time.ticks_diff(time.ticks_ms(), last) > 5000:
        last = time.ticks_ms()
        client.publish(b"esp32/uptime", str(time.ticks_ms() // 1000))
    time.sleep(0.1)