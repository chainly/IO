# coding: utf8
import os
import sys
import typing
import socket
import socks

# https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
from dht_client import bencode

# Nid = os.urandom(20)
Nid = b'\x17\xb3\xebF\x13~\x93\x05\xcb\xa2BG\xd1\xb3\xac\x1d\xce\xac\x8b\xee'
socket.setdefaulttimeout(10)
# proxy
#socks.set_default_proxy(socks.SOCKS5, "localhost", 11111)
#socket.socket = socks.socksocket

# socket_client
def socket_client(conn, data, BUFFSIZE=1024):
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
        except socket.timeout:
            raise        
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

        # but = '' ==> buf is empty ==> done
        # tcp mark something as EOF, or content_length
        # udp recieve all once
        if buf:
            #print(buf)
            ret += buf
            break
        else:
            break  
    # print(conn, ret)
    if not s._closed: s.close()
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
def __build_PING_query(id_):
    # b'd1:rd2:id20:\xb6\x93}dak\x94.\xe5\xc2\x9e^\x01\xf8_\x9fX\x92\xcb)2:ip4:q\xd0p\x82e1:t2:aa1:v4:UTv_1:y1:re'
    pingQuery = {b"t":b"aa", b"y":b"q", b"q":b"ping", b"a":{b"id":id_}}
    return bencode.dumps(pingQuery)

def __build_GET_PEERS_query(id_, info_hash):
    # 
    get_peers = {b"t":b"aa", b"y":b"q", b"q":b"get_peers", b"a": {b"id":id_, b"info_hash":info_hash}}
    return bencode.dumps(get_peers)   
def __on_ANNOUNCE_PEER_query(id_, ):
    pass
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
        # {b'ip': b'q\xd0p\x82\tI', 
        #b'r': {b'id': b'2\xf5NisQ\xffJ\xec)\xcd\xba\xab\xf2\xfb\xe3F|\xc2g', 
        #b'nodes': b"4\x1c\xa4\xe1l\xd6\xaeR\x90I\xf1\xf1\xbb\xe9\xeb\xb3\xa6\xdb<\xbe\xb9)\xab\x03\xb6\xeb\x1c\x01\xc1^4\xcc\xa5i\xa1\x1b9j\xa81\xb9\xe6\x83\xf0\xd1r\xb1\xe4<\x7fj\xbaN\xf0\xb9\x0b\xa7`\xc6\xd6\x1e\x7f/>\x11\x05\xad\xaa\\\xe2y\x85jn%\x12b<\xc5q\x84\xd8\xe5\x05\x0e\xfcT9s\x89\x11:\x81c\xd1T%OpQ\xe5$qaEMBF0B429D429E0XXX\x1d\x96s9\x80\x9eE'66\x0e\x0c\xe4\xfb4\xd3u\xc8_\x8e\x80n[w\x1ey\xd8I\x057\xc7[\xb9\xde\x81\x19\x11\xaa\xe1\xc5\xc4\xb4\xfc'G\xfb\xff\xca\x9f\x1be\xb8\xae\xa4Y\xa9\x84\x91\x1a\xe1\x12F\x1akh\x03k\x85\x94YX\xc2\xdb\xadg\x85\x05 \x85\xbb.\x97\x96\xc9\x88c3\x8cl\xd6\xaeR\x90I\xf1\xf1\xbb\xe9\xeb\xb3\xa6\xdb<\x87\x0c\xe1]{8/C\xaeA\xc6\x0c+\xab\x86\x0e\x9b;w\x9d\x0c\xcdR\x98\xb1W\x85\xcb\xf9X|snW;\x80\xd3\x96J\xa7\xd2~&\x96\xbe\xcc=\x8cib\xfb\x16\xc0\xa1\x16|\xf4\x90B>\x81\xe1\xe1\x9e`\x9e\x03d\xbf\xa7\xb7\x18tU\x85ol\xb4\xcf\x95\xf0\xda\rI\x1c{]\x98\x7f\x8a\xc0:\xe7\xf5\xea\xef}[H\x7fG\xb2#\x842D5vv\x9b\xffP\x02c6\x05v\xb61B\xa3\x9e^\xaf\x14\nn\xcbvZ=vb\xb1\x84\xc27\xc4\x91q\x85(s\x0c\xa0d7*1\x94ov\x17\xe5/\xa1`\xe5m_8\x16R7\xaf\xf5\xcf\\z\xa8\xa2r\x11\xa1\xd6\xed\xd3\xf6\x8dm\xdbm\x8b\x8aCt\xf9\xff\x965\x1a"}
        #, b't': b'aa', b'y': b'r'}
    except bencode.BencodeDecodingError:
        raise
    
    # KRPC Protocol, http://www.bittorrent.org/beps/bep_0005.html
    # find_node Responses
    # Response = {"t":"aa", "y":"r", "r": {"id":"0123456789abcdefghij", "nodes": "def456..."}}
    # error
    # {b'e': [203, b'Send your own ID, not mine'], b't': b'aa', b'v': b'lt\r ', b'y': b'e'}
    if message[b'y'] == b'e':
        return None
    # the compact node info for the target node or the K (8) closest good nodes in its own routing table.
    if isinstance(message.get(b"r"), dict) and message[b"r"].get(b'values'):
        return __on_GET_PEERS_response(message)
    if isinstance(message.get(b"r"), dict) and type(message[b"r"].get(b"nodes")) is bytes:
        if message[b"y"] == b'r':
            return __on_FIND_NODE_response(message)
    # get_peers for info_hash stored or the K (8) closest good nodes in its own routing table.
    #if isinstance(message.get(b"r"), dict) and type(message[b"r"].get(b"nodes")) is bytes:
        #if message[b"y"] == b'r':
            #return __on_FIND_NODE_response(message)
    # who is downloading the info_hash
    #elif message.get(b"q") == b"announce_peer":
        #if message[b"y"] == b'q':
            #return __on_ANNOUNCE_PEER_response(message)
    # ping/pong
    elif message.get(b"q") == b"ping":
        if message[b"y"] == b'r':
            return __on_PING_response(message)
    else:
        return message
        # raise AssertionError('404')
    
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
    if len(infos) == 6:
        return (inet_ntoa(infos[:4]), int_from_bytes(infos[4:], "big"))
    
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
        raise

    try:
        nodes = __decode_nodes(nodes_arg)
    except AssertionError:
        raise

    nodes = [n for n in nodes if n[1][1] != 0]  # Ignore nodes with port 0.
    return nodes
    #self._routing_table.update(nodes[:self.__n_max_neighbours - len(self._routing_table)])

def __on_PING_response(message):
    # {b'ip': b'q\xd0p\x82\x08\x81', b'r': {b'id': b'\xf7hX\x90,\xfbn\x8ar\xbe]\x99\x13\xb3\xc7\x191i\xd5\x0c'}, b't': b'aa', b'v': b'LT\x00\t', b'y': b'r'}
    return message
def __on_GET_PEERS_response(message):
    """
    {b'ip': b'q\xd0p\x82\x0e\x99', b'r': {b'id': b'\x99\xd48\x8a)/\xb5\xdceF\x03\xd32\x9d\x87\xe2i/\xacX', 
    b'nodes': b'\x83\xb4\\\xa5\xd9\x12\x14\x8d\xef\x01\xda\x1f\x00\xc9%\xbd\x04\xb9D\xa0\xbaH\xf3\x9a\x0f\x81\xf6\xac=\xb3\xe9\xd18\xf7\xdf\xc2\xf6e0\n\t\xc74zh\xda\xc1Q\xa2\xb4I\xca\xf6\xac=\xb4\x92\x1b!m\xba-2\xa3(\xc2\xfa\\\x8a\xc6\x8a=M\xbd\xb7\x18\r\x99\xf6\xac=\xb5jd\xebj"L\xddy
    \xec\xde2\xb1\x13|6\xc1%\x9c\x03\xf9e_\xf6\xac=\xb6\x81\x9c\x94\xa6\'\xd4\xbc\x904\x1a.\x7f\xfc\xe5\x8c{y-\x90\xab\x14\x8f\xf6\xac=\xb7\x08sl\xdb\xed\xd5$\xf3\xdb\xc6\xeaa4\x0e\x15\xc3\x92\x93\x1a<\x1c\xc1\xf6\xac=\xa0\xaeQ.\xaf<\xbe\xe6P\x9e\xba\x961\x83\x82\x9b)_\xd4\x1e\xb4tq\xf6\xac=\xa160\xc1u
    \xf8\xa2.\xbd\x07\x00*\xcdf\x1d\x12\xc0\x8a\xb4s\x85f\xb0', b'token': b'Ev06jeab', 
    b'values': [b'crYqzD', b'504rHz', b'R7NMTo', b'3SVhZF', b'mLiO46', b'hamV5H', b'715dXL', b'e4yHk5', b'VyuJWR', b'6q02Dq', b'W363Bs', b'o91433', b'G75OOM', b'w19v4g', b'a53dqQ']},
    b't': b'aa', b'v': b'LT\x00\t', b'y': b'r'}
    """
    values = [__decode_nodes(i) for i in message[b'r'][b"values"]]
    print(values)
    raise SystemExit(values)
    return values

def __on_ANNOUNCE_PEER_response(message):
    return message
# magneticod
def main():
    # __bootstrap
    BOOTSTRAPPING_NODES = [
        #("www.baidu.com", 80),
        ("router.bittorrent.com", 6881),
        ("dht.transmissionbt.com", 6881)
    ]
    # query BOOTSTRAPPING_NODES
    # find_node
    data = __build_FIND_NODE_query(Nid)
    for conn in BOOTSTRAPPING_NODES:
        try:
            ret, addr = socket_client(conn, data)
        except Exception as err:
            print(err)
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
        
    assert nodes, '404'
    MIN_XOR = 2**160
    
    while nodes:
        tid, conn = nodes.pop()
        # ping
        data = __build_PING_query(tid)
        try:
            ret, addr = socket_client(conn, data)
        except Exception as err:
            print(err)
            continue
        if ret:
            msg = datagram_received(ret, addr)
            # get_peers
            info_hash = b'\xb5\xc5\x0c\x9a\x17\x83qv\x96q\x8b\xb4\xeb\x15\xcb\xf2~\x06\x169'
            data = __build_GET_PEERS_query(tid, info_hash)
            try:
                ret, addr = socket_client(conn, data)
            except Exception as err:
                print(err)
            else:
                try:
                    values = datagram_received(ret, addr)
                except SystemExit as err:
                    print('featching', err.args)
                    for connect in err.args[0]:
                        fetch_metadata_from_peer(connect, info_hash)
                    raise
                else:
                    if values:
                        #nodes = values + nodes
                        #print('added,', values)
                        for nid, nconn in values:
                            cur_XOR = int.from_bytes(info_hash, 'big') ^ int.from_bytes(nid, 'big')
                            print(cur_XOR)
                            if cur_XOR <= MIN_XOR:
                                MIN_XOR = cur_XOR
                                nodes.append((nid, nconn))
                                print('added', nid, nconn)
                            
def fetch_metadata_from_peer(connect,  info_hash):
    data = b"\x13BitTorrent protocol%s%s%s" % (  # type: ignore
                b"\x00\x00\x00\x00\x00\x10\x00\x01",
                info_hash,
                os.urandom(20)
            )
    try:
        message, addr = socket_client(connect, data)
    except Exception as err:
        print(err)
    else:
        # b'\x13Bit\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\xa1El\x00'
        if message[1:20] != b"BitTorrent protocol":
            print('bad protocol')
        __on_bt_handshake(connect, message)
        
def __on_bt_handshake( conn, message):
    """ on BitTorrent Handshake... send the extension initiate_the_bittorrent_handshake! """
    if message[25] != 16:
        logging.info("Peer does NOT support the extension protocol")

    msg_dict_dump = bencode.dumps({
            b"m": {
                b"ut_metadata": 1
            }
        })
    # In case you cannot read hex:
    #   0x14 = 20  (BitTorrent ID indicating that it's an extended message)
    #   0x00 =  0  (Extension ID indicating that it's the initiate_the_bittorrent_handshake message)
    data = b"%b\x14%s" % (  # type: ignore
                                            (2 + len(msg_dict_dump)).to_bytes(4, "big"),
            b'\0' + msg_dict_dump
            )
    try:
        message, addr = socket_client(connect, data)
    except Exception as err:
        print(err)
    else:
        print(message)
                
if __name__ == '__main__':
    #import unittest
    #class MainTestCase(unittest.TestCase):
        #def testmain(self):
            #self.assertEqual(main(), None)
    #unittest.main()
    main()
