# refer
  1. [DHT Protocol](http://www.bittorrent.org/beps/bep_0005.html)
  2. [Extension Protocol](http://www.bittorrent.org/beps/bep_0010.html)
  3. [Extension for Peers to Send Metadata Files](http://www.bittorrent.org/beps/bep_0009.html)
  4. [khashmir](https://github.com/wiedi/khashmir)
  5. [magnetico](https://github.com/boramalper/magnetico)

# explain
  1. encode_format, for easy, I choose `JSON`
  2. listen, just use HttpServer, so that it may migrate into other http project
     speed? current not taken into account.
  3. DHT Protocol
    - ping # head
    - find_node # get to know cloest node or the node(return itself)
    - get_peers # 
    - DHT table, redis_dict
    - hashinfo/metadata, redis_key_value
