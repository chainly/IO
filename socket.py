#coding: utf-8

# https://docs.python.org/2/library/socket.html?highlight=socket#module-socket
import socket
socket.setdefaulttimeout(100)
print(socket.getdefaulttimeout())
"""
socket.getaddrinfo('baidu.com',80)
[(2, 1, 6, '', ('123.125.114.144', 80)),
 (2, 2, 17, '', ('123.125.114.144', 80)),
 (2, 3, 0, '', ('123.125.114.144', 80)),
 (2, 1, 6, '', ('111.13.101.208', 80)),
 (2, 2, 17, '', ('111.13.101.208', 80)),
 (2, 3, 0, '', ('111.13.101.208', 80)),
 (2, 1, 6, '', ('220.181.57.217', 80)),
 (2, 2, 17, '', ('220.181.57.217', 80)),
 (2, 3, 0, '', ('220.181.57.217', 80)),
 (2, 1, 6, '', ('180.149.132.47', 80)),
 (2, 2, 17, '', ('180.149.132.47', 80)),
 (2, 3, 0, '', ('180.149.132.47', 80))
 ]
"""
sock = socket.socket(family = socket.AF_INET, # AF_UNIX(socket file), AF_INET(ipv4), AF_INET6(ipv6)
                     type = socket.SOCK_STREAM, # SOCK_STREAM(TCP),
                                                # SOCK_DGRAM(UDP),
                                                # SOCK_RAW(raw), ...;
                                                # proto =  usually zero
                     )

sock.bind(('',5555))
# python    8372                 cool    6u     sock                0,8       0t0     199688 protocol: TCP
fd = sock.fileno() # 6
sock.listen(5) # backlog
# python    8372                 cool    6u     IPv4             199688       0t0        TCP *:5555 (LISTEN)
