#!/bin/bash
while :; do
 ps ax | grep -v grep | grep xmppwz.py > /dev/null || pon 3g
 sleep 40
done
