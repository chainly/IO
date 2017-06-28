#coding: utf-8

# https://docs.python.org/2/library/socket.html?highlight=socket#module-socket
import socket

# blocking, non-blocking, or timeout
# socket.setblocking(True) a shorthand for this
# https://docs.python.org/3/library/socket.html#notes-on-socket-timeouts
socket.setdefaulttimeout(None)
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
# server close firstly and in timewait
# set is so that when we cancel out we can reuse port
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# set keepalive
# ref: https://stackoverflow.com/questions/12248132/how-to-change-tcp-keepalive-timer-using-python-script
sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
# the interval of inactivity to start send KEEPALIVE(default to 14400)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)
# the interval to send next if previous KEEPALIVE timeout
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
# the num of KEEPALIVE to send before mark it failed
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)

sock.bind(('',5555))
# python    8372                 cool    6u     sock                0,8       0t0     199688 protocol: TCP
fd = sock.fileno() # 6
sock.listen(5) # backlog
# python    8372                 cool    6u     IPv4             199688       0t0        TCP *:5555 (LISTEN)
print(sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)) # 0
time.sleep(20)


