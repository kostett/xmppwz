xmppwz
======

XMPP-bot which sends METAR weather data by city code

Installing:
- JID setup: register it, add ICQ/MRIM/AOL/etc transport (if necessary), fill info and logout
- install python2 (I'm used 2.7.6), xmpppy (in Arch Linux) or python-xmpp (in Debian)
- put xmppwz.conf to /etc/xmppwz.conf and fill in JID and password
- put xmppwz.py wherever you want and do it executable (chmod +x xmppwz.py)
- run xmppwz.py

How to make it daemonize? Google knows, but I'm add "/usr/bin/python2.7 /usr/bin/local/xmppwz.py &" in /etc/rc.local before "exit 0".

Usage for clients: CODE

You can find out code of your city airport here - http://www.rap.ucar.edu/weather/surface/stations.txt

Active bot is metarbot@jabberon.ru and in ICQ 9423231. Enjoy!
