#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sys, os, signal, time, re
import xmpp, urllib2, ConfigParser

def iqCB(conn,iq_node):
    reply=iq_node.buildReply('result')
    conn.send(reply)

def messageCB(conn,msg):
    command = msg.getBody()
    if ( command is not None ):
        command = command.strip()
        check = re.compile(r'^[0-9A-Za-z\s]*$')
        if ( len(command) == 4 and check.match(command) ):
            strURL = 'http://weather.noaa.gov/pub/data/observations/metar/decoded/' + command.upper() + '.TXT'
            req = urllib2.Request(strURL)
            try:
                resp = urllib2.urlopen(req)
            except urllib2.URLError, e:
                if e.code == 404:
                    conn.send(xmpp.Message(msg.getFrom(),"Sorry, but weather is not available. Probably you input incorrect CODE or its weather not cached."))
                else:
                    conn.send(xmpp.Message(msg.getFrom(),"Sorry, but weather is not available. METAR weather caching site seems down."))
            else:
                # 200, 301
                if ( urllib2.urlopen(strURL).getcode() not in [200, 301] ):
                    conn.send(xmpp.Message(msg.getFrom(),"Sorry, but weather is not available. METAR weather caching site seems down."))
                else:
                    f = urllib2.urlopen(urllib2.Request(strURL))
                    response = f.read()
                    f.close()
                    conn.send(xmpp.Message(msg.getFrom(),response))
        else:
            conn.send(xmpp.Message(msg.getFrom(),"Usage: CODE\nYou  can find out code of your city airport here - http://www.rap.ucar.edu/weather/surface/stations.txt"))

def presenceCB(conn,msg):
    if ( msg.getType() == "subscribe" ):
        conn.send(xmpp.Presence(to=msg.getFrom(), typ='subscribed'))
        conn.send(xmpp.Presence(to=msg.getFrom(), typ='subscribe'))
    
def StepOn(conn):
    global metarbotlastping
    if time.time() - metarbotlastping > 30:
        metarbotlastping = time.time()
        ping = xmpp.Protocol('iq',typ='get',payload=[xmpp.Node('ping',attrs={'xmlns':'urn:xmpp:ping'})])
        res = conn.SendAndWaitForResponse(ping, 1)
    try:
        conn.Process(1)
    except KeyboardInterrupt:
        return 0
    return 1
    
def GoOn(conn):
    while StepOn(conn): pass
    conn.disconnect()
        
def main():
    config = ConfigParser.ConfigParser()
    config.read('/etc/xmppwz.conf')
    user=(config.get('account', 'login'))
    password=(config.get('account', 'password'))
    presence=(config.get('presence','presence'))
    jid=xmpp.protocol.JID(user)
    # cl = xmpp.Client(jid.getDomain()) # enable debug
    cl = xmpp.Client(jid.getDomain(), debug=[]) # disable debug
    if cl.connect() == "":
        print "not connected"
        sys.exit(0)
    if cl.auth(jid.getNode(),password,"METAR weather bot") is None:
        print "authentication failed"
        sys.exit(0)
    cl.UnregisterDisconnectHandler(cl.DisconnectHandler)
    cl.RegisterDisconnectHandler(cl.reconnectAndReauth())
    cl.RegisterHandler('presence', presenceCB)
    cl.RegisterHandler('iq',iqCB)
    cl.RegisterHandler('message', messageCB)
    cl.sendInitPresence()
    GoOn(cl)

metarbotlastping = time.time()    
main()
