Setup
=====

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
# Add GPG key and apt source for mopidy apt repo (required for some extensions).
wget -q -O - https://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/stretch.list
apt update

# Install python pip and development requirements, required by Mopidy and extensions.
apt install build-essential python-dev python-pip

# Install GStreamer, required by Mopidy itself.
apt install gstreamer1.0-alsa \
    python-gst-1.0 \
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
useradd -u 666 -g 666 -G audio -c "Mopidy User" -d /opt/mopidy -m -s /bin/bash mopidy
```

Let's create our python venv and install mopidy:

```
su - mopidy

virtualenv --system-site-packages mopidy
source mopidy/bin/activate

pip install mopidy
```

Spotify Extension
-----------------

If you want to use Spotify within Mopidy, install the [Mopidy Spotify Extension](https://github.com/mopidy/mopidy-spotify):

```
# IMPORTANT: The following command requires the mopidy apt repo from above.
apt install libffi-dev libspotify-dev libspotify12 
sudo -u mopidy /opt/mopidy/mopidy/bin/pip install pyspotify mopidy-spotify
```

After installing spotify, you must authenticate it as described in the [official github repo](https://github.com/mopidy/mopidy-spotify#configuration) and/or on the [mopidy website](https://www.mopidy.com/authenticate/#spotify). The configuration looks like this:

```
[spotify]
username = … your username …
password = … your secret …
client_id = … client_id value you got from mopidy.com …
client_secret = … client_secret value you got from mopidy.com …
```

Iris Extension
--------------

If you want a web interface to control Mopidy, I'd recommend [Iris](https://github.com/jaedb/Iris):

```
sudo -u mopidy /opt/mopidy/mopidy/bin/pip install mopidy-iris
```

After installing Iris, you might want to set the following settings:

```
[iris]
country = CH
locale = de_CH
```