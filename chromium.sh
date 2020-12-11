#!/bin/bash

exec chromium  --proxy-server=socks4://10.152.152.10:9050  --user-data-dir=$HOME/.config/chromium

