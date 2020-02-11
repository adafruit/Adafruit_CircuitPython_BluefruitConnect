# Basic example for using the BLE Connect UART
# To use, start this program, and start the Adafruit Bluefruit LE Connect app.
# Connect, and then select UART

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

while True:
    print("WAITING...")
    # Advertise when not connected.
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass

    # Connected
    ble.stop_advertising()
    print("CONNECTED")

    # Loop and read packets
    while ble.connected:
        if uart_server.in_waiting:
            raw_bytes = uart_server.read(uart_server.in_waiting)
            text = raw_bytes.decode().strip()
            print("raw bytes =", raw_bytes)
            print("text =", text)

    # Disconnected
    print("DISCONNECTED")
