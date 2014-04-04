#!/bin/bash
while :; do
 ps ax | grep -v grep | grep xmppwz.py > /dev/null || xmppwz.py &
 sleep 40
done
