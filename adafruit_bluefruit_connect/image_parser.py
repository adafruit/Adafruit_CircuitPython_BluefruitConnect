# SPDX-FileCopyrightText: 2026 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_bluefruit_connect.image_parser`
====================================================

Parse chunks of data making up an image sent by the BLE Connect app.

Current limitations:
 - 16bit 565 format only

* Author(s): Tim Cocks, Claude Sonnet 4.5

"""


class BLEImageParser:
    """
    Stateful parser for BLE image data received in chunks.
    """

    def __init__(self, bitmap):
        """
        Initialize the parser.

        Args:
            bitmap: 2D array-like object that supports bitmap[x, y] = value assignment
        """
        self.bitmap = bitmap
        self.reset()

    def reset(self):
        """Reset the parser state for a new image."""
        self.buffer = bytearray()
        self.header_parsed = False
        self.width = 0
        self.height = 0
        self.color_space = 0
        self.expected_total_size = 0
        self.pixels_written = 0

    def add_chunk(self, chunk_data):
        """
        Add a chunk of data to the parser.

        Args:
            chunk_data: bytes or bytearray containing a chunk of image data

        Returns:
            True if the complete image has been received and parsed, False if more data needed

        Raises:
            ValueError if the data format is invalid
        """
        # Add chunk to buffer
        self.buffer.extend(chunk_data)

        # Parse header if we haven't yet
        if not self.header_parsed:
            # Need at least 7 bytes for header (without CRC)
            if len(self.buffer) < 7:
                return False  # Need more data

            # Check magic bytes
            if self.buffer[0] != 0x21 or self.buffer[1] != 0x49:
                raise ValueError("Invalid magic bytes")

            # Get color space
            self.color_space = self.buffer[2]

            if self.color_space != 16:
                raise ValueError(f"Only 16-bit 565 format supported, got {self.color_space}")

            # Get width (uint16 little endian)
            self.width = self.buffer[3] | (self.buffer[4] << 8)

            # Get height (uint16 little endian)
            self.height = self.buffer[5] | (self.buffer[6] << 8)

            # Calculate expected total size
            bytes_per_pixel = 2  # 16-bit = 2 bytes
            pixel_data_size = self.width * self.height * bytes_per_pixel
            self.expected_total_size = 7 + pixel_data_size + 1  # header + pixels + CRC

            self.header_parsed = True
            print(f"Header parsed: {self.width}x{self.height}, {self.color_space}-bit")
            print(f"Expected total size: {self.expected_total_size} bytes")

        # Check if we have all the data yet
        if len(self.buffer) < self.expected_total_size:
            print(f"Progress: {len(self.buffer)}/{self.expected_total_size} bytes received")
            return False  # Need more data

        # We have all the data, parse the pixels
        print("All data received, parsing pixels...")
        self._parse_pixels()

        return True  # Complete!

    def _parse_pixels(self):
        """Parse pixel data from the complete buffer."""
        pixel_idx = 7  # Start after header

        for y in range(self.height):
            for x in range(self.width):
                # Read 16-bit pixel (little endian)
                low_byte = self.buffer[pixel_idx]
                high_byte = self.buffer[pixel_idx + 1]
                pixel_565 = low_byte | (high_byte << 8)
                pixel_idx += 2

                # Write to bitmap
                self.bitmap[x, y] = pixel_565
                self.pixels_written += 1

        # Optional: Verify CRC
        # crc_received = self.buffer[pixel_idx]
        # crc_calculated = calculate_crc(self.buffer[0:pixel_idx])
        # if crc_received != crc_calculated:
        #     print("Warning: CRC mismatch")

        print(f"Successfully parsed {self.pixels_written} pixels")
