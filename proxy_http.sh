#!/bin/bash

set -ex

SRC_DIR=$(dirname $(readlink -f "${BASH_SOURCE[0]}"))
cd $SRC_DIR/../proxy-list

PORT=$1

touch last.txt
sed -i "/^$/d" last.txt

IP=$(grep -v -f last.txt filt.txt | cut -d" " -f1 | shuf -n1)
echo $IP >>last.txt
geoiplookup $(echo $IP  | cut -d":" -f1)
echo "chromium --proxy-server=127.0.0.1:$1  --user-data-dir=$HOME/.config/chromium_proxy_$1"
socat -v TCP4-LISTEN:$1,fork,reuseaddr SOCKS4:10.152.152.10:${IP},socksport=9050
