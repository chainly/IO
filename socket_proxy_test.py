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

# tcp        0      0 127.0.0.1:5555          127.0.0.1:40446         TIME_WAIT   -   
# This will raise 
# socket.error: [Errno 98] Address already in use
# conn.close() before sock.close()
# time_wait
# vi /etc/sysctl.conf 
# net.ipv4.tcp_tw_recycle = 1 
# /sbin/sysctl -p
sock.bind(('',5555))

# python    8372                 cool    6u     sock                0,8       0t0     199688 protocol: TCP
fd = sock.fileno() # 6
sock.listen(5) # backlog
# python    8372                 cool    6u     IPv4             199688       0t0        TCP *:5555 (LISTEN)

import urllib2
def http_parse(data):
    """
    GET /http://www.qq.com/ HTTP/1.1
    Host: 127.0.0.1:5555
    Connection: keep-alive
    Upgrade-Insecure-Requests: 1
    User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
    Accept-Encoding: gzip, deflate, sdch, br
    Accept-Language: zh-CN,zh;q=0.8
    """
    lines = data.split('\r\n')
    #print(lines)
    action, url, ver = lines[0].split(None,2)
    url = url.lstrip('/')
    lines[0] = ' '.join((action, urlparse.urlparse(url).path, ver))
    lines[1] = 'Host: %s'% urlparse.urlparse(url).netloc
    print('url:%s'%url)
    print('data:%s'%lines)
    return url,'\r\n'.join(lines)
import urlparse,re
def socket_client(url,data):
    ParseResult = urlparse.urlparse(url)
    # stuck in favicon.ico
    if ParseResult.path == '/favicon.ico':
        #HTTP/1.1 404 Not Found
        #Server: nginx/1.10.1
        #Date: Thu, 22 Jun 2017 11:36:00 GMT
        #Content-Type: text/html
        #Content-Length: 571
        #Connection: keep-alive        
        data = '\r\n'.join(['HTTP/1.1 404 Not Found', 'Server: nginx/1.10.1', 'Date: Thu, 22 Jun 2017 11:36:00 GMT', 'Content-Type: text/html', 'Content-Length: 571', 'Connection: keep-alive'])
    if ParseResult.scheme not in ["https",'http']:
        data = 'HTTP/1.1 404 Not Found\r\n'

    host,port = urllib2.splitport(ParseResult.netloc)
    if port:
        port = int(port)
    else:
        if ParseResult.scheme == 'https':
            port = 443
        else:
            port = 80
        
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host,port))
    s.sendall(data)
    data = s.recv(100000)
    s.close()
    return data
# for single one
while True:
    try:
        conn, addr = sock.accept()
        data = conn.recv(1024)
        print(data)
        # after client close, it will continue  send EMPTY(''),
        # that means EMPTY data is treated as connect closed
        #if not data:
        #    conn.close()
        url,data = http_parse(data)
        """
        HTTP/1.1 200 OK
        Server: X2_Platform
        Connection: keep-alive
        Date: Thu, 22 Jun 2017 10:36:45 GMT
        Cache-Control: max-age=600
        {'content-encoding': 'gzip',
        'transfer-encoding': 'chunked', 
        'expires': 'Thu, 22 Jun 2017 10:38:57 GMT'
        }

        """
        #ret = urllib2.urlopen(url.rstrip('\r\n')).read()
        ret = socket_client(url, data)
        conn.sendall(ret)
    except socket.timeout:
        continue
    except Exception as err:
        print(err)
        conn.close()
 
        
sock.close()
