# The MIT License (MIT)
#
# Copyright (c) 2019 Dan Halbert for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_bluefruit_connect.quaternion_packet`
====================================================

Bluefruit Connect App Quaternion data packet.

* Author(s): Dan Halbert for Adafruit Industries

"""

import struct

from .xyz_packet import XYZPacket

class QuaternionPacket(XYZPacket):
    """A packet of x, y, z float values. Used for several different Bluefruit controller packets."""

    # Use XYZPacket to handle x, y, z, and add w.

    _FMT_CONSTRUCT = '<ssffffx'
    _FMT_PARSE = '<xxffffx'
    PACKET_LENGTH = struct.calcsize(_FMT_CONSTRUCT)
    _TYPE_CHAR = 'Q'

    def __init__(self, x, y, z, w):
        """Construct a QuaternionPacket from the given x, y, z, and w float values."""
        super().__init__(x, y, z)
        self._w = w

    def to_bytes(self):
        """Return the bytes needed to send this packet.
        """
        packet = struct.pack(self._FMT_CONSTRUCT, b'!', self._TYPE_CHAR,
                             self._x, self._y, self._z, self._w)
        self.set_checksum(packet)
        return packet

    @property
    def w(self):
        """The w value."""
        return self._w

# Register this class with the superclass. This allows the user to import only what is needed.
QuaternionPacket.register_packet_type()
