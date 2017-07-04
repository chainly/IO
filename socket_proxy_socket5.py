#coding: utf-8
import time
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

# http://www.cnblogs.com/hdtianfu/archive/2012/10/20/2732675.html
def get_specific_random_listen_port(port=0):
    sock = socket.socket(family = socket.AF_INET, # AF_UNIX(socket file), AF_INET(ipv4), AF_INET6(ipv6)
                         type = socket.SOCK_STREAM, # SOCK_STREAM(TCP),
                                                    # SOCK_DGRAM(UDP),
                                                    # SOCK_RAW(raw), ...;
                                                    # proto =  usually zero
                         )
    
    # server close firstly and in timewait
    # set is so that when we cancel out we can reuse port
    # And slove this problem
    # tcp        0      0 127.0.0.1:5555          127.0.0.1:40446         TIME_WAIT   -   
    # This will raise 
    # socket.error: [Errno 98] Address already in use
    # conn.close() before sock.close()
    # time_wait
    # vi /etc/sysctl.conf 
    # net.ipv4.tcp_tw_recycle = 1 
    # /sbin/sysctl -p
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # set keepalive
    # ref: https://stackoverflow.com/questions/12248132/how-to-change-tcp-keepalive-timer-using-python-script
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    # the interval of inactivity to start send KEEPALIVE(berkeley 14400)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)
    # the interval to send next if previous KEEPALIVE timeout(berkeley 75)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5)
    # the num of KEEPALIVE to send before mark it failed(berkeley 8)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
    
    sock.bind(('',port))
    # python    8372                 cool    6u     sock                0,8       0t0     199688 protocol: TCP
    #fd = sock.fileno() # 6
    sock.listen(10) # backlog
    # python    8372                 cool    6u     IPv4             199688       0t0        TCP *:5555 (LISTEN)
    #print(sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)) # 1
    #time.sleep(120)
    
    # telnet 127.0.0.1 5555
    # Connected to 127.0.0.1.
    # telnet    8444                 cool    3u     IPv4             202973       0t0        TCP localhost:33728->localhost:5555 (ESTABLISHED)
    return sock

sock = get_specific_random_listen_port(5555)
#nsock = sock
#print(sock.getsockname())
#sock = get_specific_random_listen_port()
#print(sock.getsockname())
#print(nsock.getsockname())
# ref: https://github.com/chainly/shadowsocks/blob/master/shadowsocks/eventloop.py#L193-L223
import select
eloop = select.epoll()
# python    8372                 cool    7u  a_inode               0,11         0      10655 [eventpoll]
fd_callback = {} # conn_num: conn, callback
if not sock in fd_callback:
    eloop.register(sock.fileno())
    fd_callback[sock.fileno()] = 'server.deal_conn'
import binascii
METHODS = None
# fp : connected? # for whether negotiated a method
#      _write? # reply
#      _read? # data
#      proxy # I'am proxy?
#      proxy_host 
#      proxy_port 
BUF_DATA = {} 


# *** SSL required, we need other example ***
"""
(8, 4, 'write_read_get', '\x05\x01\x00\x03\x11www.google.com.hk\x01\xbb', '\x05\x00\x00\x01127.0.0.1\x15\xb3', None)
[(8, 5)]
(8, '\x16\x03\x01\x00\xc8\x01\x00\x00\xc4\x03', 1)
[(8, 5)]
(8, '\x03\x96\xb35\x0b\xb2\xdf\xa5k\xd6', 1)
[(8, 5)]
(8, '`x;?A\x93\xf3)\x9a\xf5', 1)
[(8, 5)]
(8, "'\xe4\xb3\xd0\xcf\xbb-\x08\xea\xc2", 1)
[(8, 5)]
(8, '\xfc\x8f\x84\x00\x00\x1c\x9a\x9a\xc0+', 1)
[(8, 5)]
(8, '\xc0/\xc0,\xc00\xcc\xa9\xcc\xa8', 1)
[(8, 5)]
(8, '\xc0\x13\xc0\x14\x00\x9c\x00\x9d\x00/', 1)
[(8, 5)]
(8, '\x005\x00\n\x01\x00\x00\x7f::', 1)
[(8, 5)]
(8, '\x00\x00\xff\x01\x00\x01\x00\x00\x00\x00', 1)
[(8, 5)]
(8, '\x16\x00\x14\x00\x00\x11www.', 1)
[(8, 5)]
(8, 'google.com', 1)
[(8, 5)]
(8, '.hk\x00\x17\x00\x00\x00#\x00', 1)
[(8, 5)]
(8, '\x00\x00\r\x00\x14\x00\x12\x04\x03\x08', 1)
[(8, 5)]
(8, '\x04\x04\x01\x05\x03\x08\x05\x05\x01\x08', 1)
[(8, 5)]
(8, '\x06\x06\x01\x02\x01\x00\x05\x00\x05\x01', 1)
[(8, 5)]
(8, '\x00\x00\x00\x00\x00\x12\x00\x00\x00\x10', 1)
[(8, 5)]
(8, '\x00\x0e\x00\x0c\x02h2\x08ht', 1)
[(8, 5)]
(8, 'tp/1.1uP\x00\x00', 1)
[(8, 5)]
(8, '\x00\x0b\x00\x02\x01\x00\x00\n\x00\n', 1)
[(8, 5)]
(8, '\x00\x08\xba\xba\x00\x1d\x00\x17\x00\x18', 1)
[(8, 5)]
(8, '\n\n\x00\x01\x00\x15\x03\x01\x00\x02', 1)
[(8, 5)]
(8, '\x02F', 1)
"""

while True:
    events = eloop.poll(timeout=5)
    if events:
        print(repr(events)) # [(6,1)] 
        """
        event
        POLL_NULL = 0x00
        POLL_IN = 0x01
        POLL_OUT = 0x04
        POLL_ERR = 0x08
        POLL_HUP = 0x10
        POLL_NVAL = 0x20
        
        *** events should treat as byte 0000 0000(00 NVAL HUP  ERR OUT 0 IN),
        *** set 1 to be True
        ***
        """
        # if evenets not be dealed, it repeats.
        for fp,event in events:
            if fp not in BUF_DATA: 
                BUF_DATA[fp] = {}
                BUF_DATA[fp]['connected'] = False
                BUF_DATA[fp]['_write'] = ''
                BUF_DATA[fp]['_read'] = ''
                BUF_DATA[fp]['proxy'] = False
                BUF_DATA[fp]['proxy_host'] = ''
                BUF_DATA[fp]['proxy_port'] = 0
            # server conn deal
            if fp == sock.fileno():
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
                    fd_callback[conn_num] = conn, conn.recv               
            # connected deal
            else:
                # we can't go predict it's fd,
                # use {fd: callback} required
                # [(8, 4)]
                # select.POLLIN set
                if event & select.POLLIN:
                    pdata = fd_callback[fp][1](10) # include \r\n
                    print(fp, pdata,fd_callback[fp][0].getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE))
                    if BUF_DATA[fp]['proxy']:
                        raise NotImplementedError 
                        """
                        (10, 4, 'write_read_get', 
                        'GET /generate_204 HTTP/1.1\r\nHost: www.gstatic.com\r\nConnection: keep-alive\r\nPragma: no-cache\r\nCache-Control: no-cache\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: zh-CN,zh;q=0.8\r\n\r\n', '\x05\x00\x00\x01127.0.0.1\x15\xb3', None)
                        """   
                        proxy_handler.read()
                    else:
                        # http://www.mojidong.com/network/2015/03/07/socket5-1/
                        # https://www.ietf.org/rfc/rfc1928.txt
                        # SwitchyOmega
                        # '\x05\x01\x00'
                        # VER  \x05  1B this version of the protocol
                        # NMETHODS \x01 1B numbers of supported method
                        # METHODS \x00 [1-255] supported method
                        # X'00' NO AUTHENTICATION REQUIRED
                        # return VERMETHODS 
                        # we can't tell wheather is connected from readin_data
                        # so BUF_DATA[fp]['connected'] flag is required
                        if not BUF_DATA[fp]['connected']:
                            METHODS = pdata[2:3]
                            BUF_DATA[fp]['_write'] = '\x05%s'%METHODS
                        else:
                            # \x05\x01\x00\x03\x11www.g
                            # oogle.com.
                            # hk\x01\xbb
                            # VER \x05
                            # CMD \x01 CONNECT  BIND X'02'  UDP ASSOCIATE X'03'
                            # RSV \x00 RESERVED
                            # ATYP \x03 DNS \x01 IPV4 \x04 IPV6 
                            # len(DST.ADDR)
                            # DST.ADDR 
                            # DST.PORT int(binascii.hexlify(DST.PORT),16)
                            # return VER | REP |  RSV  | ATYP | BND.ADDR | BND.PORT
                            #         \x05\x00\x00\x01127.0.0.1|    2 (binascii.a2b_hex(hex(6666)[2:]))
                            BUF_DATA[fp]['_read'] += pdata
                            if len(BUF_DATA[fp]['_read']) >= 5:
                                length = int(binascii.hexlify(BUF_DATA[fp]['_read'][4:5]),16)
                                if len(BUF_DATA[fp]['_read']) == 5 + length + 2:
                                    BUF_DATA[fp]['proxy_host'] = BUF_DATA[fp]['_read'][5:-2]
                                    BUF_DATA[fp]['proxy_port'] = int(binascii.hexlify(BUF_DATA[fp]['_read'][-2:]),16)
                                    BUF_DATA[fp]['_write'] = BUF_DATA[fp]['_read']
                                    BUF_DATA[fp]['_read'] = ''

                            # '\x05\x00\x00\x01127.0.0.1%s'%(binascii.a2b_hex(hex(5555)[2:])
                    # (8, 'test\r\n')
                    # for telnet
                    # data end with '\r\n'
                    # ctr self_define
                    # close EOF with ''
                    # close conn, else recive '' continuously even conn disappearred
                    # ==> that why we need to change which EVENT should fp register 
                    #     or you will recieve write_event but you don't want to write(waster resource)
                    if pdata == '':
                        fd_callback[fp][0].close()
                        eloop.unregister(fp)                    
                        fd_callback.pop(fp, None)            
                        print(fp, event, 'closed')
                # telnet quit Connection closed.
                # tcp        0      0 127.0.0.1:34572         127.0.0.1:5555          FIN_WAIT2   -
                # tcp        0      0 127.0.0.1:5555          127.0.0.1:34572         CLOSE_WAIT  13792/python
                # 407302       0t0        TCP localhost:5555->localhost:34578 (CLOSE_WAIT)
                # conn close deal
                # [(8, 5)]
                #elif event == 5:
                # select.POLLIN done and select.POLLOUT wanted
                elif event & select.POLLOUT:
                    print(fp, event, 'write') 
                    if BUF_DATA[fp]['_write']:
                        if BUF_DATA[fp]['proxy']:                        
                            """
                            (10, 4, 'write_read_get', 
                            'GET /generate_204 HTTP/1.1\r\nHost: www.gstatic.com\r\nConnection: keep-alive\r\nPragma: no-cache\r\nCache-Control: no-cache\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: zh-CN,zh;q=0.8\r\n\r\n', '\x05\x00\x00\x01127.0.0.1\x15\xb3', None)
                            """   
                            raise NotImplementedError
                            proxy_handler.write() 
                        else:   
                            if not BUF_DATA[fp]['connected']:
                                ret = fd_callback[fp][0].sendall(BUF_DATA[fp]['_write'])
                                print(fp, event, 'write_get',BUF_DATA[fp]['_write'], ret) 
                                BUF_DATA[fp]["_write"] = ''
                                BUF_DATA[fp]['connected'] = True
                                #time.sleep(60)
                            else:
                                # generate an random port
                                nsock = get_specific_random_listen_port()
                                nfp = nsock.fileno()
                                nport = nsock.getsockname()[1]
                                fd_callback[fp] 
                                BUF_DATA[nfp] = {
                                    "connected": False,
                                    "_write": '',
                                    "_read": '',
                                    "proxy": True,
                                    "proxy_host": BUF_DATA[fp]['proxy_host'],
                                    "proxy_port": BUF_DATA[fp]['proxy_port'],
                                    }
                                ret = fd_callback[fp][0].sendall('\x05\x00\x00\x01127.0.0.1%s'%(binascii.a2b_hex(hex(nport)[2:])))
                                print(fp, event, 'write_set_nsocket','\x05\x00\x00\x01127.0.0.1%s'%(binascii.a2b_hex(hex(5555)[2:])), ret) 
                                BUF_DATA[fp]['_write'] = ''
                                #time.sleep(60)
                    time.sleep(2)
                # I can't comfirm it before writing a client
                # ref: http://scotdoyle.com/python-epoll-howto.html
                elif event & select.EPOLLHUP:
                    # close conn, else no FIN reply
                    fd_callback[fp][0].close()
                    eloop.unregister(fp)                    
                    fd_callback.pop(fp, None)
                    print(fp, event, 'EPOLLHUP')
                else:
                    # close conn, else no FIN reply
                    fd_callback[fp][0].close()
                    eloop.unregister(fp)                    
                    fd_callback.pop(fp, None)
                    print(fp, event, 'unknow')

    else:
        print(fd_callback)


