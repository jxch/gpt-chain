import socket
import socks
import urllib.request


# data = urllib.request.urlopen("http://www.youtube.com").read()
# print(data)

def proxy(host="localhost", port=10808):
    socks.setdefaultproxy(socks.SOCKS5, host, port)
    socket.socket = socks.socksocket
