# SPDX-FileCopyrightText: 2021 Tony Hansen
#
# SPDX-License-Identifier: MIT

"""
`adafruit_bluefruit_connect.raw_text_packet`
====================================================

Bluefruit Connect App raw text data packet.

Note that the raw text data packet is different from those used by the
Controller module (e.g. Accelerometer, Control Pad, and Color Picker).
Those use the bytes "!x" (where x is specific to the type of packet),
followed by data specific to the packet, followed by a checksum.
The UART text sender instead sends the bytes followed by a newline.
There is no length indicator, no checksum, etc. Of course, that also
precludes the use of an "!" at the beginning of the string.

Consequently, this packet type is MUCH simpler than the other packet types.

* Author(s): Tony Hansen

"""

from .packet import Packet


class RawTextPacket(Packet):
    """A packet containing a text string."""

    _TYPE_HEADER = b"RT"

    def __init__(self, text):
        """Construct a RawTextPacket from a binary string."""
        if isinstance(text, bytes):
            self._text = text.strip()
        else:
            raise ValueError("Text must be a bytes string")

    @property
    def text(self):
        """Return the text associated with the object."""
        return self._text


# Register this class with the superclass. This allows the user to import only what is needed.
RawTextPacket.register_packet_type()
