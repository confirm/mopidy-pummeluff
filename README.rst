Mopidy Pummeluff
================

Pummeluff is a `Mopidy <http://www.mopidy.com/>`_ extension which allows you to control Mopidy via RFID cards. It is as simple as that:

- Register an action to an RFID card
- Touch that card on the RFID reader and the action will be executed 

Thus, the Mopidy Pummeluff extension adds the following features to Mopidy:

- A radically simple web UI which can be used to manage the RFID cards
- A daemon which continuously reads RFID cards in the background and executes the assigned actions

There are several actions included, such as replacing the tracklist with a desired URI, setting the volume to a specific level or controlling the playback state.

Hardware
========

Requirements
------------

To get the whole thing working, you need the following hardware:

- A Raspberry Pi 3 Model B
- An ``RC522`` RFID module (available on `AliExpress <https://www.aliexpress.com/wholesale?SearchText=rc522>`_ for approx. *USD 1*)
- RFID cards, keyfobs or stickers (``ISO 14443A`` and ``Mifare`` should work)

.. note::

    The project will probably run on other RPi models, but I've only tested it on the ``3B``. The RPi ``3B+`` should also work fine, as the GPIO pins are identical. I don't know about RPi ``1`` or ``2``, but you can give it a shot.

Connecting the RC522 module
---------------------------

Please connect the ``RC522`` RFID module to the RPi as follows:

- ``RC522 pin 1 [SDA ]`` ––– ``RPi pin 24 [SPI0 CE0 ]``
- ``RC522 pin 2 [SCK ]`` ––– ``RPi pin 23 [SPI0 SCLK]``
- ``RC522 pin 3 [MOSI]`` ––– ``RPi pin 19 [SPI0 MOSI]``
- ``RC522 pin 4 [MISO]`` ––– ``RPi pin 21 [SPI0 MISO]``
- ``RC522 pin 5 [IRQ ]`` ––– ``RPi pin 18 [ GPIO 24 ]``
- ``RC522 pin 6 [GND ]`` ––– ``RPi pin 20 [   GND   ]``
- ``RC522 pin 7 [RST ]`` ––– ``RPi pin 22 [ GPIO 25 ]``
- ``RC522 pin 8 [3.3V]`` ––– ``RPi pin 17 [3.3V PWR ]``

Please have a look at the `Raspberry Pi SPI pinout <https://pinout.xyz/pinout/spi>`_ if you want to have a graphical view of the RPi GPIO pins. 

.. note::
    
    This connections are only valid for the RPi model ``3B`` and ``3B+``. If you want to use another RPI model, make sure you're using the correct pins.

.. important::

    Some manuals in the internet mention that the ``IRQ`` pin shouldn't be connected.
    However, Mopidy Pummeluff really uses the ``IRQ`` pin for the interrupt, so that less CPU cycles are used for the card reading daemon. If you don't connect the ``IRQ`` pin, Mopidy Pummeluff won't work!

Installation
============

Prepare Raspberry Pi
--------------------

Before you can install and use Mopidy Pummeluff, you need to configure your Raspberry Pi.

We want to enable the ``SPI`` interface and give the ``mopidy`` user access to it. This is required for the communication to the RFID module. Enter this command:

.. code-block:: bash

    sudo raspi-config

In the configuraton utility, **Enable the SPI** under ``5 Interfacing Options – P4 SPI``. 

After that, add your ``mopidy`` user to the ``spi`` and ``gpio`` group:

.. code-block:: bash

    sudo usermod -a -G spi,gpio mopidy

If you're planning to use a card to shutdown the system, you also need to create a sudo rule, so that the ``mopidy`` user can shutdown the system without a password prompt:

.. code-block:: bash

    echo "mopidy ALL = NOPASSWD: /sbin/shutdown" > /etc/sudoers.d/mopidy

Install via pip
---------------

The recommended way to install Mopidy Pummeluff by using ``pip`` and thus by executing the following command:

.. code-block:: bash

    sudo pip install mopidy-pummeluff

.. hint::

    If you get an error that ``spidev`` could not be found, run ``pip install spidev`` first. This is an issue related to the ``pi-rc522`` Pypi package.

Install from source
-------------------

Alternatively, you can also install Mopidy Pummeluff from source, by running this command:

.. code-block:: bash

    sudo su -
    cd /usr/src
    git clone https://github.com/confirm/mopidy-pummeluff.git
    cd mopidy-pummeluff
    python setup.py install

.. hint::

    If you get an error that ``spidev`` could not be found, run ``pip install spidev`` first. This is an issue related to the ``pi-rc522`` Pypi package.

Configuration
=============

Activate and configure the `Mopidy HTTP <https://docs.mopidy.com/en/latest/ext/http/>`_ extension and make sure you can connect to the Web UI. The minimal config looks like this:

.. code-block::

    [http]
    enabled = true
    hostname = 0.0.0.0

Usage
=====

Open the Mopidy Web UI (i.e. ``http://{MOPIDY_IP}:6680/``).
You should see a ``pummeluff`` web client which can be used to regsiter new RFID cards.