Run Mopidy
==========

Run Mopidy via CLI
------------------

You can run Mopidy from the CLI by executing:

```
su - mopidy
source mopidy/bin/activate
mopidy --config /etc/mopidy/mopidy.conf
```

Run Mopidy as service
---------------------

To run Mopidy as service, copy the [mopidy systemd service unit](systemd/mopidy.service) to `/etc/systemd/system/mopidy.service` and run the following commands:

```
systemctl daemon-reload
systemctl enable mopidy
```

From now on you can easily `start`, `stop` or `restart` Mopidy:

```
systemctl start mopidy
systemctl stop mopidy
systemctl restart mopidy
```