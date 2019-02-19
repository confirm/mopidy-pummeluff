Hardware
========

Overview
--------

To setup Pummeluff, you need to following hardware:

- [Raspberry Pi 3](https://www.raspberrypi.org/)
- [RC522 RFID reader](https://www.aliexpress.com/wholesale?SearchText=rc522)

Connect RFID reader
-------------------

Connect the RC522 RFID reader on the following ports:

- RC522 PIN `1` / `SDA` ––– RPi PIN `24` / `SPI0 CS0`
- RC522 PIN `2` / `SCK` ––– RPi PIN `23` / `SPI0 SCLK`
- RC522 PIN `3` / `MOSI` ––– RPi PIN `19` / `SPI0 MOSI`
- RC522 PIN `4` / `MISO` ––– RPi PIN `21` / `SPI0 MISO`
- RC522 PIN `5` / `IRQ` ––– _do not connect_
- RC522 PIN `6` / `GND` ––– RPi PIN `20` / `GND`
- RC522 PIN `7` / `RST` ––– RPi PIN `22`
- RC522 PIN `8` / `3.3V` ––– RPi PIN `17` / `3.3V PWR`
