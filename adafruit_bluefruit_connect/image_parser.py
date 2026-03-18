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
    Writes pixels to bitmap as data arrives without buffering the full image.
    """

    def __init__(self, bitmap, debug=False):
        """Initialize the parser.

        :param Bitmap bitmap: The Bitmap object to write image data into
        :param bool debug: Whether to enable debug prints
        """
        self.bitmap = bitmap
        self.debug = debug
        self.reset()

    def reset(self):
        """Reset the parser state for a new image."""
        self._header_buffer = bytearray()
        self._partial_pixel = bytearray()  # For incomplete pixel at chunk boundary
        self._header_parsed = False
        self._width = 0
        self._height = 0
        self._color_space = 0
        self._expected_total_size = 0
        self._bytes_received = 0
        self._current_x = 0
        self._current_y = 0
        self._crc_byte = None

    def add_chunk(self, chunk_data):
        """
        Add a chunk of data to the parser.

        :param chunk_data: bytes or bytearray containing a chunk of image data.
            Raises ValueError if the data format is invalid

        :return: True if the complete image has been received and parsed, False if more data needed
        """
        chunk_idx = 0

        # Parse header if we haven't yet
        if not self._header_parsed:
            # Add to header buffer
            bytes_needed = 7 - len(self._header_buffer)
            bytes_to_take = min(bytes_needed, len(chunk_data))
            self._header_buffer.extend(chunk_data[chunk_idx : chunk_idx + bytes_to_take])
            chunk_idx += bytes_to_take
            self._bytes_received += bytes_to_take

            # Check if we have complete header
            if len(self._header_buffer) >= 7:
                # Check magic bytes
                if self._header_buffer[0] != 0x21 or self._header_buffer[1] != 0x49:
                    raise ValueError("Invalid magic bytes")

                # Get color space
                self._color_space = self._header_buffer[2]

                if self._color_space != 16:
                    raise ValueError(f"Only 16-bit 565 format supported, got {self._color_space}")

                # Get width (uint16 little endian)
                self._width = self._header_buffer[3] | (self._header_buffer[4] << 8)

                # Get height (uint16 little endian)
                self._height = self._header_buffer[5] | (self._header_buffer[6] << 8)

                # Calculate expected total size
                bytes_per_pixel = 2  # 16-bit = 2 bytes
                pixel_data_size = self._width * self._height * bytes_per_pixel
                self._expected_total_size = 7 + pixel_data_size + 1  # header + pixels + CRC

                self._header_parsed = True
                if self.debug:
                    print(f"Header parsed: {self._width}x{self._height}, {self._color_space}-bit")
                    print(f"Expected total size: {self._expected_total_size} bytes")

                # Clear header buffer to free memory
                self._header_buffer = bytearray()

        # Process pixel data
        if self._header_parsed and chunk_idx < len(chunk_data):
            # Handle partial pixel from previous chunk
            if len(self._partial_pixel) > 0:
                bytes_needed = 2 - len(self._partial_pixel)
                bytes_to_take = min(bytes_needed, len(chunk_data) - chunk_idx)
                self._partial_pixel.extend(chunk_data[chunk_idx : chunk_idx + bytes_to_take])
                chunk_idx += bytes_to_take
                self._bytes_received += bytes_to_take

                # If we now have a complete pixel, write it
                if len(self._partial_pixel) == 2:
                    pixel_565 = self._partial_pixel[0] | (self._partial_pixel[1] << 8)
                    self.bitmap[self._current_x, self._current_y] = pixel_565

                    # Advance position
                    self._current_x += 1
                    if self._current_x >= self._width:
                        self._current_x = 0
                        self._current_y += 1

                    self._partial_pixel = bytearray()

            # Process remaining complete pixels in this chunk
            while chunk_idx + 1 < len(chunk_data):
                # Check if we've finished all pixels
                pixels_written = self._current_y * self._width + self._current_x
                total_pixels = self._width * self._height

                if pixels_written >= total_pixels:
                    # We're at the CRC byte
                    self._crc_byte = chunk_data[chunk_idx]
                    self._bytes_received += 1
                    chunk_idx += 1
                    break

                # Read complete pixel
                low_byte = chunk_data[chunk_idx]
                high_byte = chunk_data[chunk_idx + 1]
                pixel_565 = low_byte | (high_byte << 8)

                self.bitmap[self._current_x, self._current_y] = pixel_565

                # Advance position
                self._current_x += 1
                if self._current_x >= self._width:
                    self._current_x = 0
                    self._current_y += 1

                chunk_idx += 2
                self._bytes_received += 2

            # Handle incomplete pixel at end of chunk
            if chunk_idx < len(chunk_data):
                pixels_written = self._current_y * self._width + self._current_x
                total_pixels = self._width * self._height

                if pixels_written < total_pixels:
                    # Save partial pixel for next chunk
                    self._partial_pixel.extend(chunk_data[chunk_idx:])
                    self._bytes_received += len(chunk_data) - chunk_idx
                elif self._crc_byte is None:
                    # This must be the CRC byte
                    self._crc_byte = chunk_data[chunk_idx]
                    self._bytes_received += 1

        # Check if we're complete
        if self._bytes_received >= self._expected_total_size:
            pixels_written = self._current_y * self._width + self._current_x
            if self.debug:
                print(f"Successfully parsed {pixels_written} pixels")

            # Optional: Verify CRC
            if self._crc_byte is not None:
                # crc_calculated = calculate_crc(...)
                # if self.crc_byte != crc_calculated:
                #     print("Warning: CRC mismatch")
                pass

            self.reset()
            return True

        if self.debug:
            print(f"Progress: {self._bytes_received}/{self._expected_total_size} bytes received")
        return False
