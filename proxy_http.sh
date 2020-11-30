#!/bin/sh

IP=$(cut -d" " -f1 proxy-list.txt  | shuf | head -n1)
geoiplookup $(echo $IP | cut -d":" -f1)
echo "chromium --proxy-server=127.0.0.1:8080  --user-data-dir=$HOME/.config/chromium_proxy"
socat  TCP4-LISTEN:8080,fork,reuseaddr SOCKS4:10.152.152.10:${IP},socksport=9050
