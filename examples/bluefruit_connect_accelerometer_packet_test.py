# Stream accelerometer data from your phone or tablet.
# To use, start this program, and start the Adafruit Bluefruit LE Connect app.
# Connect and go to the Controller screen. Turn on
# STREAM SENSOR DATA -> Accelerometer to send data from the device's
# accelerometer. See how it matches what this prints.

from adafruit_ble.uart import UARTServer
from adafruit_bluefruit_connect.packet import Packet
# Only the packet classes that are imported will be known to Packet.
from adafruit_bluefruit_connect.accelerometer_packet import AccelerometerPacket

uart_server = UARTServer()

while True:
    # Advertise when not connected.
    uart_server.start_advertising()
    while not uart_server.connected:
        pass

    while uart_server.connected:
        packet = Packet.from_stream(uart_server)
        if isinstance(packet, AccelerometerPacket):
            print(packet.x, packet.y, packet.z)
