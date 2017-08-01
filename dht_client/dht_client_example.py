# coding: utf8
import os
import sys
import typing
import socket
import socks
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
from dht_client import bencode

# Nid = os.urandom(20)
Nid = b'\x17\xb3\xebF\x13~\x93\x05\xcb\xa2BG\xd1\xb3\xac\x1d\xce\xac\x8b\xee'
socket.setdefaulttimeout(30)
# proxy
#socks.set_default_proxy(socks.SOCKS5, "localhost", 11111)
#socket.socket = socks.socksocket

# socket_clint
def socket_clint(conn, data, BUFFSIZE=1024):
    print(conn, data)
    ret = b''
    # [Errno 111] Connection refused for tcp
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)    
    try:
        s.connect(conn)
    except (socket.error, socket.timeout) as e:
        print(e)
        return None
    #s.sendall(data)
    s.sendto(data, conn)
    # manually s.recv(100)
    # tcp     4142      0 10.8.1.238:41278        101.37.97.51:80         
    # CLOSE_WAIT  7823/python          关闭 (0.00/0/0)
    # ==> we read from buf
    buf = None
    while 1:
        #buf = s.recv(1024)
        try:
            buf, conn2 = s.recvfrom(BUFFSIZE)
        except OSError as err:
            if err.errno == 10040:
                # udp will raise OSError if BUFFSIZE < buf
                # (10040, '一个在数据报套接字上发送的消息大于内部消息缓冲区或其他一些网络限制，
                # 或该用户用于接收数据报的缓冲区比数据报小。', None, 10040, None)
                print(err.args)
                s.close()
                BUFFSIZE += 1024
                return socket_clint(conn, data, BUFFSIZE)
            else:
                raise
        except socket.timeout:
            break
        # but = '' ==> buf is empty ==> done
        # tcp mark something as EOF, or content_length
        # udp recieve all once
        if buf:
            print(buf)
            ret += buf
            break
        else:
            break  
    print(conn, ret)
    return ret, conn2
# query
def __build_FIND_NODE_query(id_, target=os.urandom(20)):
    """ Reference Implementation:
    bencode.dumps({
        b"y": b"q",
        b"q": b"find_node",
        b"t": b"aa",
        b"a": {
            b"id": id_,
            b"target": self.__random_bytes(20)
        }
    })
    """
    # b'd1:ad2:id20:\x17\xb3\xebF\x13~\x93\x05\xcb\xa2BG\xd1\xb3\xac\x1d\xce\xac\x8b\xee6:target20:4RZZj-^\x12\xf0\x1f#y\x9b\xbe\x1d\xd3\xd3?\xff6e1:q9:find_node1:t2:aa1:y1:qe'
    """ Optimized Version: """
    return b"d1:ad2:id20:%s6:target20:%se1:q9:find_node1:t2:aa1:y1:qe" % (
        id_,
        target
    )

# answer
def datagram_received(data, addr) -> None:
    # Ignore nodes that "uses" port 0, as we cannot communicate with them reliably across the different systems.
    # See https://tools.cisco.com/security/center/viewAlert.x?alertId=19935 for slightly more details
    if addr[1] == 0:
        return

    #if self._transport.is_closing():
        #return

    try:
        message = bencode.loads(data)
        print(message)
        # {b'ip': b'q\xd0p\x82\tI', b'r': {b'id': b'2\xf5NisQ\xffJ\xec)\xcd\xba\xab\xf2\xfb\xe3F|\xc2g', b'nodes': b"4\x1c\xa4\xe1l\xd6\xaeR\x90I\xf1\xf1\xbb\xe9\xeb\xb3\xa6\xdb<\xbe\xb9)\xab\x03\xb6\xeb\x1c\x01\xc1^4\xcc\xa5i\xa1\x1b9j\xa81\xb9\xe6\x83\xf0\xd1r\xb1\xe4<\x7fj\xbaN\xf0\xb9\x0b\xa7`\xc6\xd6\x1e\x7f/>\x11\x05\xad\xaa\\\xe2y\x85jn%\x12b<\xc5q\x84\xd8\xe5\x05\x0e\xfcT9s\x89\x11:\x81c\xd1T%OpQ\xe5$qaEMBF0B429D429E0XXX\x1d\x96s9\x80\x9eE'66\x0e\x0c\xe4\xfb4\xd3u\xc8_\x8e\x80n[w\x1ey\xd8I\x057\xc7[\xb9\xde\x81\x19\x11\xaa\xe1\xc5\xc4\xb4\xfc'G\xfb\xff\xca\x9f\x1be\xb8\xae\xa4Y\xa9\x84\x91\x1a\xe1\x12F\x1akh\x03k\x85\x94YX\xc2\xdb\xadg\x85\x05 \x85\xbb.\x97\x96\xc9\x88c3\x8cl\xd6\xaeR\x90I\xf1\xf1\xbb\xe9\xeb\xb3\xa6\xdb<\x87\x0c\xe1]{8/C\xaeA\xc6\x0c+\xab\x86\x0e\x9b;w\x9d\x0c\xcdR\x98\xb1W\x85\xcb\xf9X|snW;\x80\xd3\x96J\xa7\xd2~&\x96\xbe\xcc=\x8cib\xfb\x16\xc0\xa1\x16|\xf4\x90B>\x81\xe1\xe1\x9e`\x9e\x03d\xbf\xa7\xb7\x18tU\x85ol\xb4\xcf\x95\xf0\xda\rI\x1c{]\x98\x7f\x8a\xc0:\xe7\xf5\xea\xef}[H\x7fG\xb2#\x842D5vv\x9b\xffP\x02c6\x05v\xb61B\xa3\x9e^\xaf\x14\nn\xcbvZ=vb\xb1\x84\xc27\xc4\x91q\x85(s\x0c\xa0d7*1\x94ov\x17\xe5/\xa1`\xe5m_8\x16R7\xaf\xf5\xcf\\z\xa8\xa2r\x11\xa1\xd6\xed\xd3\xf6\x8dm\xdbm\x8b\x8aCt\xf9\xff\x965\x1a"}, b't': b'aa', b'y': b'r'}

    except bencode.BencodeDecodingError:
        raise

    if isinstance(message.get(b"r"), dict) and type(message[b"r"].get(b"nodes")) is bytes:
        return __on_FIND_NODE_response(message)
    elif message.get(b"q") == b"get_peers":
        __on_GET_PEERS_query(message, addr)
    elif message.get(b"q") == b"announce_peer":
        __on_ANNOUNCE_PEER_query(message, addr)

def __decode_nodes(infos: bytes): # -> typing.List[typing.Tuple[NodeID, NodeAddress]]
    """ Reference Implementation:
    nodes = []
    for i in range(0, len(infos), 26):
        info = infos[i: i + 26]
        node_id = info[:20]
        node_host = socket.inet_ntoa(info[20:24])
        node_port = int.from_bytes(info[24:], "big")
        nodes.append((node_id, (node_host, node_port)))
    return nodes
    """
    # https://github.com/kosqx/better-bencode
    """ Optimized Version: """
    # Because dot-access also has a cost
    inet_ntoa = socket.inet_ntoa
    int_from_bytes = int.from_bytes
    return [
        (infos[i:i+20], (inet_ntoa(infos[i+20:i+24]), int_from_bytes(infos[i+24:i+26], "big")))
        for i in range(0, len(infos), 26)
    ]      

# b'd1:rd2:id20:<\x00rsH\xb3\xb8\xedp\xba\xa1\xe1A\x1b8i\xd8H\x13!5:nodes208:\xe4\xc4\xc7I\x02\x8a\x8b\xa8#\xab\xdc\xdcS\xf8\x9c\xe5\xa2\x11\x81\x8cmV\xbe\x97X@\xe4\xc4\xc7I\x02\x8a\x8b\xa8#\xab\xdc\xdcS\xf8\x9c\xe5\xa2\x11\x81\x8cmV\xbe\x97X@\xe4\xc4\xc7I\x02\x8a\x8b\xa8#\xab\xdc\xdcS\xf8\x9c\xe5\xa2\x11\x81\x8cmV\xbe\x97X@\xe4\xc4\xc7I\x02\x8a\x8b\xa8#\xab\xdc\xdcS\xf8\x9c\xe5\xa2\x11\x81\x8cmV\xbe\x97X@\xe4\xc4\xc7I\x02\x8a\x8b\xa8#\xab\xdc\xdcS\xf8\x9c\xe5\xa2\x11\x81\x8cmV\xbe\x97X@\xe4\xc4\xc7I\x02\x8a\x8b\xa8#\xab\xdc\xdcS\xf8\x9c\xe5\xa2\x11\x81\x8cmV\xbe\x97X@\xe4\xc4\xc7I\x02\x8a\x8b\xa8#\xab\xdc\xdcS\xf8\x9c\xe5\xa2\x11\x81\x8cmV\xbe\x97X@\xe4\xc4\xc7I\x02\x8a\x8b\xa8#\xab\xdc\xdcS\xf8\x9c\xe5\xa2\x11\x81\x8cmV\xbe\x97X@e1:t2:aa1:v4:JB\x00\x001:y1:re'
def __on_FIND_NODE_response(message):  # pylint: disable=invalid-name
    # Well, we are not really interested in your response if our routing table is already full; sorry.
    # (Thanks to Glandos@GitHub for the heads up!)
    #if len(self._routing_table) >= self.__n_max_neighbours:
        #return

    try:
        nodes_arg = message[b"r"][b"nodes"]
        assert type(nodes_arg) is bytes and len(nodes_arg) % 26 == 0
    except (TypeError, KeyError, AssertionError):
        return

    try:
        nodes = __decode_nodes(nodes_arg)
    except AssertionError:
        return

    nodes = [n for n in nodes if n[1][1] != 0]  # Ignore nodes with port 0.
    return nodes
    #self._routing_table.update(nodes[:self.__n_max_neighbours - len(self._routing_table)])

# magneticod
def main():
    # __bootstrap
    BOOTSTRAPPING_NODES = [
        #("www.baidu.com", 80),
        ("router.bittorrent.com", 6881),
        ("dht.transmissionbt.com", 6881)
    ]
    # query BOOTSTRAPPING_NODES
    data = __build_FIND_NODE_query(Nid)
    for conn in BOOTSTRAPPING_NODES:
        ret, addr = socket_clint(conn, data)
        if ret:
            nodes = datagram_received(ret, addr)
            print(len(nodes), nodes)
            # 16 [(b'4\x1c\xa4\xe1l\xd6\xaeR\x90I\xf1\xf1\xbb\xe9\xeb\xb3\xa6\xdb<\xbe', ('185.41.171.3', 46827)),
            #(b'\x1c\x01\xc1^4\xcc\xa5i\xa1\x1b9j\xa81\xb9\xe6\x83\xf0\xd1r', ('177.228.60.127', 27322)),
            #(b'N\xf0\xb9\x0b\xa7`\xc6\xd6\x1e\x7f/>\x11\x05\xad\xaa\\\xe2y\x85', ('106.110.37.18', 25148)),
            #(b'\xc5q\x84\xd8\xe5\x05\x0e\xfcT9s\x89\x11:\x81c\xd1T%O', ('112.81.229.36', 29025)),
            #(b'EMBF0B429D429E0XXX\x1d\x96', ('115.57.128.158', 17703)),
            #(b'66\x0e\x0c\xe4\xfb4\xd3u\xc8_\x8e\x80n[w\x1ey\xd8I', ('5.55.199.91', 47582)),
            #(b"\x81\x19\x11\xaa\xe1\xc5\xc4\xb4\xfc'G\xfb\xff\xca\x9f\x1be\xb8\xae\xa4", ('89.169.132.145', 6881)),
            #(b'\x12F\x1akh\x03k\x85\x94YX\xc2\xdb\xadg\x85\x05 \x85\xbb', ('46.151.150.201', 34915)),
            #(b'3\x8cl\xd6\xaeR\x90I\xf1\xf1\xbb\xe9\xeb\xb3\xa6\xdb<\x87\x0c\xe1', ('93.123.56.47', 17326)),
            #(b'A\xc6\x0c+\xab\x86\x0e\x9b;w\x9d\x0c\xcdR\x98\xb1W\x85\xcb\xf9', ('88.124.115.110', 22331)),
            #(b'\x80\xd3\x96J\xa7\xd2~&\x96\xbe\xcc=\x8cib\xfb\x16\xc0\xa1\x16', ('124.244.144.66', 16001)),
            #(b'\xe1\xe1\x9e`\x9e\x03d\xbf\xa7\xb7\x18tU\x85ol\xb4\xcf\x95\xf0', ('218.13.73.28', 31581)),
            #(b'\x98\x7f\x8a\xc0:\xe7\xf5\xea\xef}[H\x7fG\xb2#\x842D5', ('118.118.155.255', 20482)),
            #(b'c6\x05v\xb61B\xa3\x9e^\xaf\x14\nn\xcbvZ=vb', ('177.132.194.55', 50321)),
            #(b'q\x85(s\x0c\xa0d7*1\x94ov\x17\xe5/\xa1`\xe5m', ('95.56.22.82', 14255)),
            #(b'\xf5\xcf\\z\xa8\xa2r\x11\xa1\xd6\xed\xd3\xf6\x8dm\xdbm\x8b\x8aC', ('116.249.255.150', 13594))]

            break


if __name__ == '__main__':
    import unittest
    class MainTestCase(unittest.TestCase):
        def testmain(self):
            self.assertEqual(main(), None)
    unittest.main()
