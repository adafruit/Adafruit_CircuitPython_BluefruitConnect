# SPDX-FileCopyrightText: 2019 Dan Halbert for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_bluefruit_connect.button_packet`
====================================================

Bluefruit Connect App Button data packet (button_name, pressed/released)


* Author(s): Dan Halbert for Adafruit Industries

"""

from __future__ import annotations

import struct

from .packet import Packet

try:
    from typing import Optional  # adjust these as needed
except ImportError:
    pass


class ButtonPacket(Packet):
    """A packet containing a button name and its state."""

    BUTTON_1: str = "1"
    """Code for Button 1 on the Bluefruit LE Connect app Control Pad screen."""
    BUTTON_2: str = "2"
    """Button 2."""
    BUTTON_3: str = "3"
    """Button 3."""
    BUTTON_4: str = "4"
    """Button 4."""
    # pylint: disable= invalid-name
    UP: str = "5"
    """Up Button."""
    DOWN: str = "6"
    """Down Button."""
    LEFT: str = "7"
    """Left Button."""
    RIGHT: str = "8"
    """Right Button."""

    _FMT_PARSE: str = "<xxssx"
    PACKET_LENGTH: int = struct.calcsize(_FMT_PARSE)
    # _FMT_CONSTRUCT doesn't include the trailing checksum byte.
    _FMT_CONSTRUCT: str = "<2sss"
    _TYPE_HEADER: bytes = b"!B"

    def __init__(self, button: str, pressed: bool) -> None:
        """Construct a ButtonPacket from a button name and the button's state.

        :param str button: a single character denoting the button
        :param bool pressed: ``True`` if button is pressed; ``False`` if it is
                             released.
        """
        # This check will catch wrong length and also non-sequence args (like an int).
        try:
            assert len(button) == 1
            assert isinstance(button, str)
        except Exception as err:
            raise ValueError("Button must be a single char.") from err

        self._button: str = button
        self._pressed: bool = pressed

    @classmethod
    def parse_private(cls, packet: bytes) -> Optional[Packet]:
        """Construct a ButtonPacket from an incoming packet.
        Do not call this directly; call Packet.from_bytes() instead.
        pylint makes it difficult to call this method _parse(), hence the name.
        """
        button, pressed = struct.unpack(cls._FMT_PARSE, packet)
        if not pressed in b"01":
            raise ValueError("Bad button press/release value")
        return cls(chr(button[0]), pressed == b"1")

    def to_bytes(self) -> bytes:
        """Return the bytes needed to send this packet."""
        partial_packet: bytes = struct.pack(
            self._FMT_CONSTRUCT,
            self._TYPE_HEADER,
            bytes(self._button, "utf-8"),
            b"1" if self._pressed else b"0",
        )
        return self.add_checksum(partial_packet)

    @property
    def button(self) -> str:
        """A single character string (not bytes) specifying the button that
        the user pressed or released."""
        return self._button

    @property
    def pressed(self) -> bool:
        """``True`` if button is pressed, or ``False`` if it is released."""
        return self._pressed


# Register this class with the superclass. This allows the user to import only what is needed.
ButtonPacket.register_packet_type()
