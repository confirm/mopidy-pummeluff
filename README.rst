Mopidy Pummeluff
================

Pummeluff is a `Mopidy <http://www.mopidy.com/>`_ extension which allows you to control Mopidy via RFID tags. It is as simple as that:

- Register an action to an RFID tag
- Touch that tag on the RFID reader and the action will be executed 

Thus, the Mopidy Pummeluff extension adds the following features to Mopidy:

- A radically simple web UI which can be used to manage the RFID tags
- A daemon which continuously reads RFID tags in the background and executes the assigned actions

There are several actions included, such as replacing the tracklist with a desired URI, setting the volume to a specific level or controlling the playback state.

Hardware
========

Requirements
------------

To get the whole thing working, you need at least the following hardware:

- A Raspberry Pi 3 Model B
- An ``RC522`` RFID module (`RC522 on AliExpress <https://www.aliexpress.com/wholesale?SearchText=rc522>`_ for approx. *USD 1*)
- RFID tags (``ISO 14443A`` & ``Mifare`` should work, `14443A tags on AliExpress <https://www.aliexpress.com/wholesale?SearchText=14443A+lot>`_ for approx. *0.4 USD* per tag)
- Female dupont jumper wires (`female dupont jumper cables on AliExpress <https://www.aliexpress.com/wholesale?SearchText=dupont>`_ for approx. *1 USD*)

Optionally you can also add two buttons to the RPi, which can be used for power & playback control:

- Two momentary push buttons (`momentary push buttons on AliExpress <https://www.aliexpress.com/wholesale?SearchText=momentary+push+button>`_ for approx. *USD 1-2*) 

Pummeluff also supports a status LED, which lights up when Pummeluff (i.e. Mopidy) is running. You can go with a separate LED, just make sure it can handle 3.3V or add a resistor. There are also push buttons with integrated LED's available, for example `these 5V momentary push buttons on AliExpress <https://www.aliexpress.com/item/16mm-Metal-brass-Push-Button-Switch-flat-round-illumination-ring-Latching-1NO-1NC-Car-press-button/32676526568.html>`_.

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

Connecting the buttons (optional)
---------------------------------

You can connect two buttons to the RPi:

- ``RPi pin 5`` - Power button: Shutdown the Raspberry Pi into halt state & wake it up again from halt state
- ``RPi pin 7`` - Playback button: Pause and resume the playback

The buttons must shortcut their corresponding pins against ``GND`` (e.g. pin ``6``) when pressed. This means you want to connect one pin of the button (i.e. ``C``) to RPI's ``GND``, and the other one (i.e. ``NO``) to RPi's pin ``5`` or ``7``.

Connecting the status LED (optional)
------------------------------------

If you want to have a status LED which is turned on when the RPi is running, you can connect an LED to a ``GND`` pin (e.g. pin ``6``) & to pin ``8``.

Installation
============

Prepare Raspberry Pi
--------------------

Before you can install and use Mopidy Pummeluff, you need to configure your Raspberry Pi properly.

We want to enable the ``SPI`` interface and give the ``mopidy`` user access to it. This is required for the communication to the RFID module. Enter this command:

.. code-block:: bash

    sudo raspi-config

In the configuraton utility, **Enable the SPI** under ``5 Interfacing Options – P4 SPI``. 

After that, add your ``mopidy`` user to the ``spi`` and ``gpio`` group:

.. code-block:: bash

    sudo usermod -a -G spi,gpio mopidy

If you're planning to use a button or RFID tag to shutdown the system, you also need to create a sudo rule, so that the ``mopidy`` user can shutdown the system without a password prompt:

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
You should see a ``pummeluff`` web client which can be used to regsiter new RFID tags.