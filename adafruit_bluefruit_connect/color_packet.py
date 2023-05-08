# SPDX-FileCopyrightText: 2019 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_bluefruit_connect.color_packet`
====================================================

Bluefruit Connect App color data packet.

* Author(s): Dan Halbert for Adafruit Industries

"""

from __future__ import annotations

import struct

from .packet import Packet

try:
    from typing import Optional, Tuple  # adjust these as needed
except ImportError:
    pass


class ColorPacket(Packet):
    """A packet containing an RGB color value."""

    _FMT_PARSE: str = "<xx3Bx"
    PACKET_LENGTH: int = struct.calcsize(_FMT_PARSE)
    # _FMT_CONSTRUCT doesn't include the trailing checksum byte.
    _FMT_CONSTRUCT: str = "<2s3B"
    _TYPE_HEADER: bytes = b"!C"

    def __init__(self, color: Tuple) -> None:
        """Construct a ColorPacket from a 3-element :class:`tuple` of RGB
        values, or from an int color value 0xRRGGBB.

        :param tuple/int color: an RGB :class:`tuple` ``(red, green, blue)``
          or an int color value ``0xRRGGBB``
        """
        if isinstance(color, int):
            self._color: Tuple = tuple(color.to_bytes(3, "big"))
        elif len(color) == 3 and all(0 <= c <= 255 for c in color):
            self._color = color
        else:
            raise ValueError("Color must be an integer 0xRRGGBB or a tuple(r,g,b)")

    @classmethod
    def parse_private(cls, packet: bytes) -> Optional[Packet]:
        """Construct a ColorPacket from an incoming packet.
        Do not call this directly; call Packet.from_bytes() instead.
        pylint makes it difficult to call this method _parse(), hence the name.
        """
        return cls(struct.unpack(cls._FMT_PARSE, packet))

    def to_bytes(self) -> bytes:
        """Return the bytes needed to send this packet."""
        partial_packet = struct.pack(
            self._FMT_CONSTRUCT, self._TYPE_HEADER, *self._color
        )
        return self.add_checksum(partial_packet)

    @property
    def color(self) -> tuple:
        """A :class:`tuple` ``(red, green blue)`` representing the color the
        user chose in the BlueFruit Connect app."""
        return self._color


# Register this class with the superclass. This allows the user to import only what is needed.
ColorPacket.register_packet_type()
