Purpose
=======

Pummeluff is an audio music box for kids. 

It is based on [Mopidy](https://www.mopidy.com/) and additional self-written extensions, which enable the support of the RFID card reader and its management.

Setup
=====

Hardware
--------

To setup Pummeluff, you need to following hardware:

- [Raspberry Pi 3](https://www.raspberrypi.org/)
- [RC522 RFID reader](https://www.aliexpress.com/wholesale?SearchText=rc522)

Connect the RC522 RFID reader on the following ports:

- RC522 PIN `1` / `SDA` ––– RPi PIN `24` / `SPI0 CS0`
- RC522 PIN `2` / `SCK` ––– RPi PIN `23` / `SPI0 SCLK`
- RC522 PIN `3` / `MOSI` ––– RPi PIN `19` / `SPI0 MOSI`
- RC522 PIN `4` / `MISO` ––– RPi PIN `21` / `SPI0 MISO`
- RC522 PIN `5` / `IRQ` ––– _do not connect_
- RC522 PIN `6` / `GND` ––– RPi PIN `20` / `GND`
- RC522 PIN `7` / `RST` ––– RPi PIN `22`
- RC522 PIN `8` / `3.3V` ––– RPi PIN `17` / `3.3V PWR`

Rasbian
-------

Download and install [Raspbian](https://raspbian.org/) on an SD card.  
Boot the RPi, login with the credentials (`pi`/`raspberry`) and run the following commands as `root` (run `sudo su -` to become `root`):

```
raspi-config
```

Change the following settings:

- `2 Network Options`
    - `N1 Hostname`: Enter the desired hostname
    - `N2 Wi-fi`: Enter the WLAN settings
- `4 Localisation Options`
    - Change the desired settings
- `5 Interfacing Options`
    - `P4 SPI`: Enable the SPI interface
- `7 Advanced Options`
    - `A3 Memory Split`: Set GPU memory to `8` MB

Now enable SSH:

```
systemctl enable ssh
systemctl start ssh
```

Also change the password of the `pi` user:

```
passwd
```

If you want to rename the `pi` user, execute the following commands (a bit hacky, but the most straight-forward way):

```
export NEW_USER="dbarton"

sed -i "s/^pi:/${NEW_USER}/" /etc/passwd    # Rename POSIX pi user
sed -i "s/^pi:/${NEW_USER}/" /etc/group     # Rename POSIX pi group
sed -i "s/pi$/${NEW_USER}/" /etc/group      # Rename pi membership of additional POSIX groups
sed -i "s/^pi:/${NEW_USER}/" /etc/shadow    # Rename shadow entry

mv /home/pi /home/${NEW_USER}               # Move home directory

cd /etc/sudoers.d/                          # Update sudoers nopasswd rule
mv 010_pi-nopasswd ${NEW_USER}
sed -i "s/^pi/${NEW_USER}/" ${NEW_USER} 
```

Now update the system:

```
apt update
apt dist-upgrade
```

Finally, reboot the machine to check if everything is still working:

```
reboot
```

Mopidy
------

To install [Mopidy](https://www.mopidy.com/), you can execute the following steps. Please note these steps are mainly based on the [official source installation docs](http://docs.mopidy.com/en/latest/installation/source/).

First of all, install all requirements for Mopidy:

```
# Install python pip and development requirements, required by Mopidy and extensions.
apt install build-essential python-dev python-pip

# Install GStreamer, required by Mopidy itself.
apt install python-gst-1.0 \
    gir1.2-gstreamer-1.0 \
    gir1.2-gst-plugins-base-1.0 \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-tools

# Install Python virtualenv, required for our setup.
pip install virtualenv
```

Now prepare our Mopidy environment:

```
groupadd -g 666 mopidy
useradd -u 666 -g 666 -c "Mopidy User" -d /opt/mopidy -m -s /bin/bash mopidy
```

Let's create our python venv and install mopidy:

```
su - mopidy

virtualenv mopidy
source mopidy/bin/activate

pip install mopidy
```