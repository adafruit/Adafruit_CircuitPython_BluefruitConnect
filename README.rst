Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-bluefruitconnect/badge/?version=latest
    :target: https://circuitpython.readthedocs.io/projects/bluefruitconnect/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://discord.gg/nBQh6qu
    :alt: Discord

.. image:: https://travis-ci.com/adafruit/Adafruit_CircuitPython_BluefruitConnect.svg?branch=master
    :target: https://travis-ci.com/adafruit/Adafruit_CircuitPython_BluefruitConnect
    :alt: Build Status

This module helps you to communicate with the Adafruit Bluefruit Connect app or use its protocols.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Usage Example
=============

Normally this library is used with the
`Adafruit_CircuitPython_BluefruitConnect
<https://github.com/adafruit/Adafruit_CircuitPython_BluefruitConnnect>`_
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

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_ble/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Building locally
================

Zip release files
-----------------

To build this library locally you'll need to install the
`circuitpython-build-tools <https://github.com/adafruit/circuitpython-build-tools>`_ package.

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install circuitpython-build-tools

Once installed, make sure you are in the virtual environment:

.. code-block:: shell

    source .env/bin/activate

Then run the build:

.. code-block:: shell

    circuitpython-build-bundles --filename_prefix adafruit-circuitpython-bluefruitconnect --library_location .

Sphinx documentation
-----------------------

Sphinx is used to build the documentation based on rST files and comments in the code. First,
install dependencies (feel free to reuse the virtual environment from above):

.. code-block:: shell

    python3 -m venv .env
    source .env/bin/activate
    pip install Sphinx sphinx-rtd-theme

Now, once you have the virtual environment activated:

.. code-block:: shell

    cd docs
    sphinx-build -E -W -b html . _build/html

This will output the documentation to ``docs/_build/html``. Open the index.html in your browser to
view them. It will also (due to -W) error out on any warning like Travis will. This is a good way to
locally verify it will pass.
