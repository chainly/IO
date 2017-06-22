#coding: utf-8

# https://docs.python.org/2/library/socket.html?highlight=socket#module-socket
import socket
socket.setdefaulttimeout(30)
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

import time
#time.sleep(5)

# telnet 127.0.0.1 5555
# Connected to 127.0.0.1.
# telnet    8444                 cool    3u     IPv4             202973       0t0        TCP localhost:33728->localhost:5555 (ESTABLISHED)


# ref: https://github.com/chainly/shadowsocks/blob/master/shadowsocks/eventloop.py#L193-L223
import select
eloop = select.epoll()
# python    8372                 cool    7u  a_inode               0,11         0      10655 [eventpoll]
fd_callback = {}
if not fd in fd_callback:
    eloop.register(fd)
    fd_callback[fd] = None
    
while True:
    events = eloop.poll(timeout=5)
    if events:
        print(events) # [(6,1)] 
        """
        event
        POLL_NULL = 0x00
        POLL_IN = 0x01
        POLL_OUT = 0x04
        POLL_ERR = 0x08
        POLL_HUP = 0x10
        POLL_NVAL = 0x20
        """
        # if evenets not be dealed, it repeats.
        for fp,event in events:
            # server conn deal
            if fp == fd:
                conn, addr = sock.accept()
                print(conn, addr)
                # python    8935                 cool    8u     IPv4             228681       0t0        TCP localhost:5555->localhost:33814 (ESTABLISHED)
                # after connected, whatever we get new fd,
                # additional data sent to this conn, 
                # so we have to register this conn
                #eloop.register(conn.fileno())
                # change to fd callback related
                conn_num = conn.fileno()
                if not conn_num in fd_callback:
                    print(conn, conn_num)
                    eloop.register(conn_num)
                    fd_callback[conn_num] = conn.recv                
            # connected deal
            else:
                # we can't go predict it's fd,
                # use {fd: callback} required
                # [(8, 4)]
                # data deal
                if event == 4:
                    print(fp, fd_callback[fp](1024))
                    # (8, 'test\r\n')
                    
                # telnet quit Connection closed.
                # tcp        0      0 127.0.0.1:34572         127.0.0.1:5555          FIN_WAIT2   -
                # tcp        0      0 127.0.0.1:5555          127.0.0.1:34572         CLOSE_WAIT  13792/python
                # 407302       0t0        TCP localhost:5555->localhost:34578 (CLOSE_WAIT)
                # conn close deal
                # [(8, 5)]
                elif event == 5:
                    fd_callback.pop(fp, None)
                    print(fp, event, 'poped')
                    time.sleep(10)
                    eloop.unregister(fp)

    else:
        print(fd_callback)
