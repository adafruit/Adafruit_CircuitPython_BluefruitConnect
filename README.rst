Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-bluefruitconnect/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/bluefruitconnect/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_BluefruitConnect/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_BluefruitConnect/actions/
    :alt: Build Status

This module helps you to communicate with the Adafruit Bluefruit Connect app or use its protocols.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-bluefruitconnect/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-bluefruitconnect

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-bluefruitconnect

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-bluefruitconnect

Usage Example
=============

Normally this library is used with the
`Adafruit_CircuitPython_BluefruitConnect
<https://github.com/adafruit/Adafruit_CircuitPython_BluefruitConnect>`_
library
(``adafruit_bluefruit_connect``). The included examples use that library.
Below is a simple standalone example.

.. code-block:: python

    from adafruit_bluefruit_connect.color_packet import ColorPacket
    from adafruit_bluefruit_connect.gyro_packet import GyroPacket

    # [uart setup omitted]

    color_packet = ColorPacket((70,75,80))
    gyro_packet = GyroPacket.from_bytes(packet_buf)
    uart.write(gyro_packet.to_bytes())

Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/bluefruitconnect/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_BluefruitConnect/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
