#!/bin/bash

NETDEV="enp0s3"

ip link set dev $NETDEV up
ip addr a dev $NETDEV 10.152.152.13/18
ip route add dev $NETDEV 10.152.152.10
echo "nameserver 10.152.152.10" >/etc/resolv.conf

export all_proxy="socks5://10.152.152.10:9100"

#gpg  --keyserver hkp://keys.gnupg.net:80 --keyserver-options http-proxy=127.0.0.1:8081 --recv-keys 465022E743D71E39

cat >/etc/sudoers.d/keep_proxy_env.conf <<EOF
Defaults env_keep += "ftp_proxy http_proxy https_proxy no_proxy all_proxy"
EOF

cat >/etc/netctl/ethernet-static <<EOF
Description=''
Interface=$NETDEV
Connection=ethernet
IP=static
Address=('10.152.152.13/18')
Gateway='10.152.152.10'
DNS=('10.152.152.10')
EOF
