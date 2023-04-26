# SPDX-FileCopyrightText: 2019 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_bluefruit_connect.location_packet`
====================================================

Bluefruit Connect App geographical location packet.

* Author(s): Dan Halbert for Adafruit Industries

"""

from __future__ import annotations

import struct

from .packet import Packet


class LocationPacket(Packet):
    """A packet of latitude, longitude, and altitude values."""

    _FMT_PARSE: str = "<xxfffx"
    PACKET_LENGTH: int = struct.calcsize(_FMT_PARSE)
    # _FMT_CONSTRUCT doesn't include the trailing checksum byte.
    _FMT_CONSTRUCT: str = "<2sfff"
    _TYPE_HEADER: bytes = b"!L"

    def __init__(self, latitude: float, longitude: float, altitude: float) -> None:
        """Construct a LocationPacket from the given values."""
        self._latitude = latitude
        self._longitude = longitude
        self._altitude = altitude

    def to_bytes(self) -> bytes:
        """Return the bytes needed to send this packet."""
        partial_packet = struct.pack(
            self._FMT_CONSTRUCT,
            self._TYPE_HEADER,
            self._latitude,
            self._longitude,
            self._altitude,
        )
        return self.add_checksum(partial_packet)

    @property
    def latitude(self) -> float:
        """The latitude value."""
        return self._latitude

    @property
    def longitude(self) -> float:
        """The longitude value."""
        return self._longitude

    @property
    def altitude(self) -> float:
        """The altitude value."""
        return self._altitude


# Register this class with the superclass. This allows the user to import only what is needed.
LocationPacket.register_packet_type()
