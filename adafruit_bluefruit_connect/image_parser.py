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
        self.header_buffer = bytearray()
        self.partial_pixel = bytearray()  # For incomplete pixel at chunk boundary
        self.header_parsed = False
        self.width = 0
        self.height = 0
        self.color_space = 0
        self.expected_total_size = 0
        self.bytes_received = 0
        self.current_x = 0
        self.current_y = 0
        self.crc_byte = None

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
        chunk_idx = 0

        # Parse header if we haven't yet
        if not self.header_parsed:
            # Add to header buffer
            bytes_needed = 7 - len(self.header_buffer)
            bytes_to_take = min(bytes_needed, len(chunk_data))
            self.header_buffer.extend(chunk_data[chunk_idx : chunk_idx + bytes_to_take])
            chunk_idx += bytes_to_take
            self.bytes_received += bytes_to_take

            # Check if we have complete header
            if len(self.header_buffer) >= 7:
                # Check magic bytes
                if self.header_buffer[0] != 0x21 or self.header_buffer[1] != 0x49:
                    raise ValueError("Invalid magic bytes")

                # Get color space
                self.color_space = self.header_buffer[2]

                if self.color_space != 16:
                    raise ValueError(f"Only 16-bit 565 format supported, got {self.color_space}")

                # Get width (uint16 little endian)
                self.width = self.header_buffer[3] | (self.header_buffer[4] << 8)

                # Get height (uint16 little endian)
                self.height = self.header_buffer[5] | (self.header_buffer[6] << 8)

                # Calculate expected total size
                bytes_per_pixel = 2  # 16-bit = 2 bytes
                pixel_data_size = self.width * self.height * bytes_per_pixel
                self.expected_total_size = 7 + pixel_data_size + 1  # header + pixels + CRC

                self.header_parsed = True
                print(f"Header parsed: {self.width}x{self.height}, {self.color_space}-bit")
                print(f"Expected total size: {self.expected_total_size} bytes")

                # Clear header buffer to free memory
                self.header_buffer = bytearray()

        # Process pixel data
        if self.header_parsed and chunk_idx < len(chunk_data):
            # Handle partial pixel from previous chunk
            if len(self.partial_pixel) > 0:
                bytes_needed = 2 - len(self.partial_pixel)
                bytes_to_take = min(bytes_needed, len(chunk_data) - chunk_idx)
                self.partial_pixel.extend(chunk_data[chunk_idx : chunk_idx + bytes_to_take])
                chunk_idx += bytes_to_take
                self.bytes_received += bytes_to_take

                # If we now have a complete pixel, write it
                if len(self.partial_pixel) == 2:
                    pixel_565 = self.partial_pixel[0] | (self.partial_pixel[1] << 8)
                    self.bitmap[self.current_x, self.current_y] = pixel_565

                    # Advance position
                    self.current_x += 1
                    if self.current_x >= self.width:
                        self.current_x = 0
                        self.current_y += 1

                    self.partial_pixel = bytearray()

            # Process remaining complete pixels in this chunk
            while chunk_idx + 1 < len(chunk_data):
                # Check if we've finished all pixels
                pixels_written = self.current_y * self.width + self.current_x
                total_pixels = self.width * self.height

                if pixels_written >= total_pixels:
                    # We're at the CRC byte
                    self.crc_byte = chunk_data[chunk_idx]
                    self.bytes_received += 1
                    chunk_idx += 1
                    break

                # Read complete pixel
                low_byte = chunk_data[chunk_idx]
                high_byte = chunk_data[chunk_idx + 1]
                pixel_565 = low_byte | (high_byte << 8)

                self.bitmap[self.current_x, self.current_y] = pixel_565

                # Advance position
                self.current_x += 1
                if self.current_x >= self.width:
                    self.current_x = 0
                    self.current_y += 1

                chunk_idx += 2
                self.bytes_received += 2

            # Handle incomplete pixel at end of chunk
            if chunk_idx < len(chunk_data):
                pixels_written = self.current_y * self.width + self.current_x
                total_pixels = self.width * self.height

                if pixels_written < total_pixels:
                    # Save partial pixel for next chunk
                    self.partial_pixel.extend(chunk_data[chunk_idx:])
                    self.bytes_received += len(chunk_data) - chunk_idx
                elif self.crc_byte is None:
                    # This must be the CRC byte
                    self.crc_byte = chunk_data[chunk_idx]
                    self.bytes_received += 1

        # Check if we're complete
        if self.bytes_received >= self.expected_total_size:
            pixels_written = self.current_y * self.width + self.current_x
            print(f"Successfully parsed {pixels_written} pixels")

            # Optional: Verify CRC
            if self.crc_byte is not None:
                # crc_calculated = calculate_crc(...)
                # if self.crc_byte != crc_calculated:
                #     print("Warning: CRC mismatch")
                pass

            self.reset()
            return True

        print(f"Progress: {self.bytes_received}/{self.expected_total_size} bytes received")
        return False
