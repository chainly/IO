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

sock.bind(('',5555))
# python    8372                 cool    6u     sock                0,8       0t0     199688 protocol: TCP
fd = sock.fileno() # 6
sock.listen(5) # backlog
# python    8372                 cool    6u     IPv4             199688       0t0        TCP *:5555 (LISTEN)
print(sock.getsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE)) # 1

# telnet 127.0.0.1 5555
# Connected to 127.0.0.1.
# telnet    8444                 cool    3u     IPv4             202973       0t0        TCP localhost:33728->localhost:5555 (ESTABLISHED)

# ref: https://github.com/chainly/shadowsocks/blob/master/shadowsocks/eventloop.py#L193-L223

import urllib2, urlparse, re

def headers_parse(data):
    data,rest = data.split('\r\n\r\n',1)
    data_lines = data.split('\r\n')
    action, url_path, ver = data_lines[0].split(None,2)    
    headers = {}
    [ headers.setdefault(*[ i.strip() for i in item.split(':',1)]) for item in data_lines[1:] ] 
    return action, url_path, ver, headers, rest
def headers_unparse(action, url_path, ver, headers, rest):
    data = '%s %s %s\r\n' % (action, url_path, ver) + \
        '\r\n'.join([ '%s: %s'%(k, headers[k]) for k in headers]) + '\r\n\r\n' + rest 
    return data
def parse_request(conn):
    # see httplib.HTTPConnection.request
    # when should we treat Http request is header/done
    # header xx/r/n...../r/n
    # /r/n
    # data lenght{} = header['content-length']
    
    # find /r/n/r/n
    data = ''
    while True:
        buf = conn.recv(10)
        if buf:
            data += buf
            if '\r\n\r\n' in data:
                break
        else:
            break
    # Content-Length
    action, url_path, ver, headers, rest_readed = headers_parse(data)
    if 'Content-Length' in headers:
        rest_length = int(headers["Content-Length"]) - len(rest_readed)
        buf = conn.recv(rest_length)
        data += buf
    #'Transfer-Encoding: chunked'
    if 'Transfer-Encoding' in headers and headers["Transfer-Encoding"] == 'chunked':
        #rest_data = '\r\n\r\n' 
        rest_data = ''
        # header, rest_data
        #data, rest_readed = data.split('\r\n\r\n',1)
        #data += '\r\n\r\n' 
        while True:
            # '\r\n' required
            if not '\r\n' in rest_readed:
                buf = conn.recv(1)
                if buf:
                    rest_readed += buf
                    continue
                else:
                    raise socket.error('READ INTERRUPTTED')
            rest_read_need_str, rest_readed = rest_readed.split('\r\n',1)
            print(rest_read_need_str, rest_readed)
            # binascii
            # int('4a0',16)
            rest_read_need_int = int(rest_read_need_str, 16)
            # 0\r\n\r\n done
            if rest_read_need_int == 0:
                # the last \r\n
                last_end_2 = conn.recv(2)
                assert last_end_2 == '\r\n', 'BAD_EOF'
                # Content-Encoding: gzip  # gzip,deflate,compress
                # http://guojuanjun.blog.51cto.com/277646/667067
                # https://stackoverflow.com/a/8506931/6493535 # zlib
                # python3 # gzip.decompress(str)
                # https://stackoverflow.com/a/2695575/6493535
                # all
                if 'Content-Encoding' in headers and headers["Content-Encoding"] == 'gzip':
                    import zlib
                    rest_data = zlib.decompress(rest_data, 16+zlib.MAX_WBITS)
                    rest_data_length = len(rest_data)
                    headers.pop('Content-Encoding',None)
                # ERR_INVALID_CHUNKED_ENCODING
                headers.pop('Transfer-Encoding',None)
                headers["Content-Length"] = rest_data_length
                data = headers_unparse(action, url_path, ver, headers, rest_data)
                break
            if len(rest_readed) >= rest_read_need_int:
                rest_data += rest_readed[:rest_read_need_int]
                rest_readed = rest_readed[rest_read_need_int:] 
                continue
            else:
                # '\r\n'
                rest_read_required = rest_read_need_int - len(rest_readed) + 2
                buf = conn.recv(rest_read_required)
                assert buf != rest_read_required, 'DATA_NOT_ENOUGH'
                rest_data += buf[:-2]
                rest_readed = ''
                continue

    return data
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
    
    ('recieved:', 
    'GET /Skins/custom/images/logo.gif HTTP/1.1\r\nHost: 127.0.0.1:5555\r\nConnection: keep-alive\r\nPragma: no-cache\r\nCache-Control: no-cache\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36\r\nAccept: image/webp,image/*,*/*;q=0.8\r\nReferer: http://127.0.0.1:5555/http://www.cnblogs.com/kuoaidebb/p/4703015.html\r\nAccept-Encoding: gzip, deflate, sdch, br\r\nAccept-Language: zh-CN,zh;q=0.8\r\n\r\n'
    )

    """
    global WEB
    
    action, url_path, ver, headers, rest_readed = headers_parse(data)
    url = url_path.lstrip('/')
    pres = urlparse.urlparse(url)
    if pres.scheme:
        # scheme, netloc, url, query, fragment = data
        WEB = urlparse.urlunsplit((pres.scheme,pres.netloc,'','',''))
    else:
        # /favicon.ico come first
        if not WEB:
            return None,None
        url = urlparse.urljoin(WEB, url)
        pres = urlparse.urlparse(url)
    lines = []
    lines.append(' '.join((action, pres.path, ver)))
    headers["Host"] = pres.netloc
    if "Referer" in headers:
        headers["Referer"] = urlparse.urlparse(headers["Referer"]).path
    [ lines.append(': '.join((k,headers[k]))) for k in headers]
    lines.append('')
    lines.append('')
    return url,'\r\n'.join(lines)
def rep_404():
    return '\r\n'.join(['HTTP/1.1 404 Not Found', 'Server: nginx/1.10.1', 'Date: Thu, 22 Jun 2017 11:36:00 GMT', 'Content-Type: text/html', 'Connection: keep-alive'])  + '\r\n\r\n'
def socket_client(url,data):
    """
    GET /kuoaidebb/p/4703015.html HTTP/1.1\r\n
    Host: www.cnblogs.com\r\n
    Connection: keep-alive\r\n
    Pragma: no-cache\r\n
    Cache-Control: no-cache\r\n
    Upgrade-Insecure-Requests: 1\r\n
    User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\n
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n
    Accept-Encoding: gzip, deflate\r\n
    Accept-Language: zh-CN,zh;q=0.8\r\n\r\n

    'GET /kuoaidebb/p/4703015.html HTTP/1.1\r\nHost: www.cnblogs.com\r\nConnection: keep-alive\r\nPragma: no-cache\r\nCache-Control: no-cache\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: zh-CN,zh;q=0.8\r\n\r\n'    
    """
    ParseResult = urlparse.urlparse(url)
    # stuck in favicon.ico
    if ParseResult.path == 'favicon.ico':
        #HTTP/1.1 404 Not Found
        #Server: nginx/1.10.1
        #Date: Thu, 22 Jun 2017 11:36:00 GMT
        #Content-Type: text/html
        #Connection: keep-alive        
        data = '\r\n'.join(['HTTP/1.1 404 Not Found', 'Server: nginx/1.10.1', 'Date: Thu, 22 Jun 2017 11:36:00 GMT', 'Content-Type: text/html', 'Connection: keep-alive'])  + '\r\n\r\n'
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
    ret = parse_request(s)
    s.close()
    return ret
# for single one
global WEB
WEB = None
while True:
    try:
        conn, addr = sock.accept()
        data = parse_request(conn)
        print('recieved:',data)
        # after client close, it will continue  send EMPTY(''),
        # that means EMPTY data is treated as connect closed
        #if not data:
        #    conn.close()
        url,data = http_parse(data)
        if not url:
            sock.sendall(rep_404())
            continue
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
        print('parsed:',url,data)
        #ret = urllib2.urlopen(url.rstrip('\r\n')).read()
        print('present:',url,data)
        
        ret = socket_client(url, data)
        print('get:',ret)
        conn.sendall(ret)
    except socket.timeout:
        continue
    except Exception as err:
        print('err:',err)
        conn.close()
 
        
sock.close()
