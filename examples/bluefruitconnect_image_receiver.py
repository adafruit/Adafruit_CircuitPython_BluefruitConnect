# SPDX-FileCopyrightText: 2026 Tim Cocks for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Example for Playground Bluefruit + TFTGizmo that receives an image sent by the
BLE Connect V2 mobile app.

Current limitations:
 - Maximum size image is 120x120. Not enough RAM for bigger
 - 16bit 565 format only

"""

import time

import displayio
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_gizmo import tft_gizmo

from adafruit_bluefruit_connect.image_parser import BLEImageParser

# Create the TFT Gizmo display
display = tft_gizmo.TFT_Gizmo()

# Create a bitmap with max color count
bitmap = displayio.Bitmap(128, 128, 65535)

# Color converter for RGB565 color coming from BLE and going into displayio
converter_565 = displayio.ColorConverter(input_colorspace=displayio.Colorspace.RGB565)

# Create a TileGrid using the Bitmap and ColorConverter
tile_grid = displayio.TileGrid(bitmap, pixel_shader=converter_565)

# Create a Group
group = displayio.Group(scale=2)

# Add the TileGrid to the Group
group.append(tile_grid)

# Add the Group to the Display
display.root_group = group

# initialize image parser
parser = BLEImageParser(bitmap)

# set up BLE
ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)

display.auto_refresh = False

count = 0
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
    last_send = time.monotonic()
    while ble.connected:
        # incoming data chunk
        if uart_server.in_waiting:
            raw_bytes = uart_server.read(uart_server.in_waiting)
            full_img_received = parser.add_chunk(raw_bytes)
            if full_img_received:
                display.refresh()

    # Disconnected
    print("DISCONNECTED")
