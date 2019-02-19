Configuration
=============

The configuration of Mopidy can be stored wherever you want. However, I'd recommend to store it in `/etc/mopidy/mopidy.conf`. If you want to use that, create the directory with the correct permissions:

```
mkdir /etc/mopidy
chown mopidy: /etc/mopidy
```

When you run Mopidy the first time, an initial configuration will be created.

You might want to set the following configuration parameters:

- `http.hostname = 0.0.0.0` to bind HTTP listener to all interfaces
- `mpd.hostname = 0.0.0.0` to bind MPD listener to all interfaces
