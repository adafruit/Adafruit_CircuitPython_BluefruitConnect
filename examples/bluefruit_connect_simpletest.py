# Print out the color data from a ColorPacket.

from adafruit_ble.uart import UARTServer
from adafruit_bluefruit_connect.packet import Packet
# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.color_packet import ColorPacket

uart_server = UARTServer()

advertising_now = False

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
        print(packet.color)
