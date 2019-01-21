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
`adafruit_bluefruit_connect.packet`
====================================================

Bluefruit Connect App packet superclass

* Author(s): Dan Halbert for Adafruit Industries

"""

import struct

class Packet:
    """
    A Bluefruit app controller packet. A packet consists of these bytes, in order:

      - '!' - The first byte is always an exclamation point.
      - *type* - A single byte designating the type of packet: 'A', 'B', etc.
      - *data ...* - Multiple bytes of data, varying by packet type.
      - *checksum* - A single byte checksum, computed by adding up all the data bytes and
          inverting the sum.

    This is an abstract class.
    """

    # All concrete subclasses should define these class attributes. They're listed here
    # as a reminder and to make pylint happy.
    _FMT_CONSTRUCT = None
    _FMT_PARSE = None
    PACKET_LENGTH = None
    _TYPE_CHAR = None


    _type_to_class = dict()

    @classmethod
    def register_packet_type(cls):
        """Register a new packet type, using this class and its `cls._TYPE_CHAR`
        The ``parse()`` method will then be able to recognize this type of packet.
        """

        Packet._type_to_class[cls._TYPE_CHAR] = cls

    @classmethod
    def from_bytes(cls, packet):
        """Create an appropriate object of the correct class for the given packet bytes.
        Validate packet type, length, and checksum.
        """

        packet_class = cls._type_to_class.get(packet[1], None)
        if not packet_class:
            raise ValueError("Unknown packet type '{}'".format(packet[1]))

        # In case this was called from a subclass, make sure the parsed
        # type matches up with the current class.
        if not issubclass(packet_class, cls):
            raise ValueError('Packet type is not a {}'.format(cls.__name__))

        if len(packet) != packet_class.PACKET_LENGTH:
            raise ValueError("Wrong length packet")

        if cls.checksum(packet) != packet[-1]:
            raise ValueError("Bad checksum")

        # A packet class may do further validation of the data.
        return packet_class.parse_private(packet)

    @classmethod
    def parse_private(cls, packet):
        """Default implementation for subclasses.
        Assumes arguments to ``__init__()`` are exactly the values parsed using
        ``cls._FMT_PARSE``. Subclasses may need to reimplement if that assumption
        is not correct.

        Do not call this directly. It's called from ``cls.from_bytes()``.
        """
        cls.__init__(*struct.unpack(cls._FMT_PARSE, packet))

    @staticmethod
    def checksum(packet):
        """Compute checksum for packet."""
        return ~sum(packet[2:-1]) & 0xff

    def set_checksum(self, packet):
        """Set checksum byte with proper checksum value."""
        packet[-1] = self.checksum(packet)
