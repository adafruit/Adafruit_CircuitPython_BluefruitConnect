# SPDX-FileCopyrightText: 2019 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_bluefruit_connect.quaternion_packet`
====================================================

Bluefruit Connect App Quaternion data packet.

* Author(s): Dan Halbert for Adafruit Industries

"""

from __future__ import annotations

import struct

from ._xyz_packet import _XYZPacket


class QuaternionPacket(_XYZPacket):
    """Device Motion data to describe device attitude. This data is derived
    from Accelerometer, Gyro, and Magnetometer readings."""

    # Use _XYZPacket to handle x, y, z, and add w.

    _FMT_PARSE: str = "<xxffffx"
    PACKET_LENGTH: int = struct.calcsize(_FMT_PARSE)
    # _FMT_CONSTRUCT doesn't include the trailing checksum byte.
    _FMT_CONSTRUCT: str = "<2sffff"
    _TYPE_HEADER: bytes = b"!Q"

    def __init__(self, x: float, y: float, z: float, w: float) -> None:
        """Construct a QuaternionPacket from the given x, y, z, and w float values."""
        super().__init__(x, y, z)
        self._w = w

    def to_bytes(self) -> bytes:
        """Return the bytes needed to send this packet."""
        partial_packet = struct.pack(
            self._FMT_CONSTRUCT, self._TYPE_HEADER, self._x, self._y, self._z, self._w
        )
        return partial_packet + bytes((self.checksum(partial_packet),))

    @property
    def w(self) -> float:
        """The w value."""
        return self._w


# Register this class with the superclass. This allows the user to import only what is needed.
QuaternionPacket.register_packet_type()
