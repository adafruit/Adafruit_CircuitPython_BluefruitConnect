# SPDX-FileCopyrightText: 2019 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_bluefruit_connect._xyz_packet`
====================================================

Bluefruit Connect App superclass for all data packets with (x, y, z) values

* Author(s): Dan Halbert for Adafruit Industries

"""

from __future__ import annotations

import struct

from .packet import Packet


class _XYZPacket(Packet):
    """A packet of x, y, z float values. Used for several different Bluefruit controller packets."""

    _FMT_PARSE: str = "<xxfffx"
    PACKET_LENGTH: int = struct.calcsize(_FMT_PARSE)
    # _FMT_CONSTRUCT doesn't include the trailing checksum byte.
    _FMT_CONSTRUCT: str = "<2sfff"
    # _TYPE_HEADER is set by each concrete subclass.

    def __init__(self, x: float, y: float, z: float) -> None:
        # Construct an _XYZPacket subclass object
        # from the given x, y, and z float values, and type character.
        self._x = x
        self._y = y
        self._z = z

    def to_bytes(self) -> bytes:
        """Return the bytes needed to send this packet."""
        partial_packet = struct.pack(
            self._FMT_CONSTRUCT, self._TYPE_HEADER, self._x, self._y, self._z
        )
        return self.add_checksum(partial_packet)

    @property
    def x(self) -> float:
        """The x value."""
        return self._x

    @property
    def y(self) -> float:
        """The y value."""
        return self._y

    @property
    def z(self) -> float:
        """The z value."""
        return self._z
