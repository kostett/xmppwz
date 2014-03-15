#!/usr/bin/python2
# -*- coding: utf-8 -*-

'''xmppwz - XMPP-bot which sends METAR weather data.
licence GPL v.3, where it was stolen - don't remember, rewrite from ipbot'''

import xmpp
import urllib2
import ConfigParser
import re

config = ConfigParser.ConfigParser()
config.read('/etc/xmppwz.conf')

# work with cfg
user=(config.get('account', 'login'))
password=(config.get('account', 'password'))
presence=(config.get('presence','presence'))

jid=xmpp.protocol.JID(user)
client=xmpp.Client(jid.getDomain())
client.connect()
client.auth(jid.getNode(),password,"METAR weather bot")

# sending init presence
def status(xstatus):
    status=xmpp.Presence(status=xstatus,show=presence,priority='1')
    client.send(msging)

# subscribe all
def presence(conn,mess):
    if ( mess.getType() == "subscribe" ):
        conn.send(xmpp.Presence(to=mess.getFrom(), typ='subscribed'))

def message(conn,mess):
    global client
    command = mess.getBody() 
    command = command.strip()
    check = re.compile(r'^[A-Za-z\s]*$')
    if ( len(command) == 4 and check.match(command) ):
        strURL='http://weather.noaa.gov/pub/data/observations/metar/decoded/' + command.upper() + '.TXT'
        req = urllib2.Request(strURL)
        try:    
            resp = urllib2.urlopen(req)
        except urllib2.URLError, e:
            if e.code == 404: 
                client.send(xmpp.Message(mess.getFrom(),"Sorry, but weather is not available. Probably you input incorrect CODE or its weather not cached."))
            else:
                client.send(xmpp.Message(mess.getFrom(),"Sorry, but weather is not available. METAR weather caching site seems down."))
        else:
            # 200, 301
            if ( urllib2.urlopen(strURL).getcode() not in [200, 301] ):
                client.send(xmpp.Message(mess.getFrom(),"Sorry, but weather is not available. METAR weather caching site seems down."))
            else:
                f = urllib2.urlopen(urllib2.Request(strURL))
                response = f.read()
                f.close()
                client.send(xmpp.Message(mess.getFrom(),response))
    else:
        client.send(xmpp.Message(mess.getFrom(),"Usage: CODE\nYou can find out code of your city airport here - http://www.rap.ucar.edu/weather/surface/stations.txt"))

client.RegisterHandler('message',message)
client.RegisterDisconnectHandler(client.reconnectAndReauth())
client.sendInitPresence()
client.RegisterHandler('presence', presence)

while True:
    client.Process(1)
