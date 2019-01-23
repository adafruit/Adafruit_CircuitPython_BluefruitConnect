# Demo using Bluefruit Connect app, a pan-tilt kit (two servos),
# and a 24-NeoPixel ring.

from adafruit_crickit import crickit
from adafruit_ble.uart import UARTServer

from adafruit_bluefruit_connect.packet import Packet
# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket

crickit.init_neopixel(24)

uart_server = UARTServer()

advertising_now = False
tilt = 0
rotate = 0
crickit.servo_1.angle = rotate
crickit.servo_2.angle = tilt

while True:

    if not uart_server.connected:
        if not advertising_now:
            uart_server.start_advertising()
            advertising_now = True
        continue

    # Connected, so no longer advertising
    advertising_now = False

    packet = Packet.from_stream(uart_server)
    if isinstance(packet, ColorPacket):
        crickit.neopixel.fill(packet.color)
    elif isinstance(packet, ButtonPacket):
        if packet.pressed:
            if packet.button == '5':
                tilt = min(170, tilt + 1)
            elif packet.button == '6':
                tilt = max(0, tilt - 1)
            elif packet.button == '7':
                rotate = min(170, rotate + 1)
            elif packet.button == '8':
                rotate = max(0, rotate - 1)

            crickit.servo_1.angle = rotate
            crickit.servo_2.angle = tilt
