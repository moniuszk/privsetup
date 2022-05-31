#!/usr/bin/env python3

import concurrent.futures
import http.client
import urllib.request
import time
import requests
import socket
import subprocess


TOTEST = []
for line in open("proxy-list-raw.txt").read().split("\n"):
    x = line.split(" ")[0]
    TOTEST.append(x)


def main(port, addr):
    ret = -1
    cmd = "socat -v TCP4-LISTEN:%s,fork,reuseaddr SOCKS4:10.152.152.10:%s,socksport=9050" % (port, addr)
    p = subprocess.Popen(["bash", "-xc", cmd], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)

    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('localhost', port))
            s.close()
            break
        except socket.error:
            time.sleep(1)

    try:
        proxy = {"http": "http://127.0.0.1:%s" % port}
        url = 'http://www.6obcy.org'
        r = requests.get(url,  proxies=proxy, timeout=60)
        ret = r.status_code
        if r.status_code != 200:
            return ret;

        url = 'http://www.duckduckgo.com'
        r = requests.get(url,  proxies=proxy, timeout=60)
        ret = r.status_code
        if r.status_code != 200:
            return ret;

        conn = http.client.HTTPConnection("localhost", port, timeout=60)
        conn.putrequest("CONNECT", "server.6obcy.pl:7010",
                        skip_host=True, skip_accept_encoding=True)
        conn.putheader("Host", "server.6obcy.pl:7010")
        conn.putheader("Proxy-Connection", "keep-alive")
        conn.endheaders()
        response = conn.getresponse()
        ret = response.status
    except requests.exceptions.ReadTimeout:
        ret = -2
    except requests.exceptions.ProxyError:
        ret = -3
    except requests.exceptions.ConnectionError:
        ret = -4
    except http.client.RemoteDisconnected:
        ret = -4
    except socket.timeout:
        ret = -5
    except:
        ret = -99
    finally:
        p.kill()
        p.wait()
    return ret


PORT = 12003
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    future_to_url = {executor.submit(
        main, PORT + num, url): url for num, url in enumerate(TOTEST)}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            if data == 200:
                print('%s' % (url))
