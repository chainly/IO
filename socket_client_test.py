#coding: utf-8
import socket
"""
@req python2.7
@next python2/3
"""

"""
Transfer-Encoding: [client]chunked for without Content-Length/[server]a large amount of data is being returned to the client 
            - http://www.httpwatch.com/httpgallery/chunked/
            - http://www.cnblogs.com/jcli/archive/2012/10/19/2730440.html
            - http://blog.csdn.net/whatday/article/details/7571451
            ==> HEADER\r\n\r\nINT\r\nDATA.....\r\n.....\r\n0\r\n
            # 30表示ascii字符0，http解释为长度是0（也说明了这是最后一个chunk），后面紧跟0d0a，然后正文部分为空，再接0d 0a表示结束
'HTTP/1.1 200 OK\r\nDate: Fri, 30 Jun 2017 06:58:35 GMT\r\nContent-Type: text/html; charset=utf-8\r\nTransfer-Encoding: chunked\r\nConnection: keep-alive\r\nVary: Accept-Encoding\r\nCache-Control: private, max-age=10\r\nExpires: Fri, 30 Jun 2017 06:58:45 GMT\r\nLast-Modified: Fri, 30 Jun 2017 06:58:35 GMT\r\nX-UA-Compatible: IE=10\r\nX-Frame-Options: SAMEORIGIN\r\nContent-Encoding: gzip\r\n\r\n4a0\r\n\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03\xacV[o\x1bE\x14~N\xa5\xfe\x87\xe9JVAt\xbd\xb1S\'v\xc8\xbaJb7\tu.\x8a\x139\xe5\xc5\x1a\xef\x8e\xbdc\xcf\xce,;\xe3\xeb\x13W\x01*\xa8\x02\xa2*JD\xa1y@\x15\x82\x96\xaa **\xc4\x9f\xa9\x9d\xe4_0\xb3k\xbbv\x08J\x82\x90-\xcd\xec\xd9s\xce\xf7\x9d\xcb\x9c\xd9\xabW\xe6\xaee\xd6\x17\xb7\xeend\x81#\\\x92\xbezeN\xad\x80@Z1\xb5\x8e\xa3[T\x0b\x84\x08\xdaju\x91\x80\xc0r\xa0\xcf\x910\xb5\xba(\xebI\xcd\x18\xbe\xa0\xd0E\xa6\xd6\xc0\xa8\xe91_h\xc0bT *\x15\x9b\xd8\x16\x8ei\xa3\x06\xb6\x90\x1e<\xdc\x00\x98b\x81!\xd1\xb9\x05\t2c\x1a\x08\xfc\x08,\x08Jo\xb4\x85\xc3(\xe0\xcc\xaa!\xd1{\xfc\xa8w\xef\xbb\xe5\xad\xad\x8d\xe3\xa7\xbf\xf7\x9e}\x08tp\xb2\xb7{\xf4\xd9\xb3\xa3\xfd\x8f\x8f\x7f\xfdV\xfe\xa5\xa4\xfb\xe5~\xf7\xc9a\xf7\xe0\xe79#t!}\x11Lk@\xb4=\xc9I\xa0\x960,\xce5\xe0#bj\\\xb4\t\xe2\x0eB\x92\xa4\xe3\xa3\xb2\xa9\x19\xa5:\xb5\xa5\xcc(\x11V\xd1-\xe6\xba\x8cF\xa5\xc1\xad\x86\xe9\x16o\xef\xb8\xcd\xceT\xb3\xf5.C\xd6vs-{\'>\xb51\xdf\xb1\xf4j\xaaQ\xda).N\xaf\x96\xc8;\tV_\xb5b2\x19}\\l\x9b\xda*\xc4tQ\x81^\x94\x04\xafa\xca\x8d\x05RG\xf9Z\xbbOI\xef?\xf6\xd9\x14\xc9\xdd\xcd\xad\xa5D\xbeZ(\xccg\x96\xacz>\xb9\xa4\x97\x0b\x85\xeat\xbc\\IT\x92|\xbae\xa7tg\x13\xea\x95\xc9Sl\\V\xc2\xd2]\x00\xab\x01\x17\xd9\x18\x9a\x1a\xa3\xa4\r\xb8\xe5#D\x01\xa46x\xc3\x85\xad\xb0B\xb3`f:\xe9\xb5\xde\xfc\x7f\xd8\xeb!z?\x88\x8c\xe8@2Y\x80\x89\xe2\x8a\x9e+\xb4;k\xeb\xa4Q\xbe\x1d\xa7\x8b30\x97X\xd1\xc5\xba\xf0d\xc7\xb5\x9d\x98\x08R:\xac\xa5\xaa\xac\xa9m\xe6\xf3\x03R\xd0\xf3\x08\xb6\xa0\xc0\x8c\x1a>\xe7o\xb5\\\xd2\xe7\x07\x89@>\x85\x02\r\xe89Bx\xb3\x86\xd1l6\xa3\x16UU\xe6QYf\xa3Vg\x10\xdb\xa8TR\xf6gae\xce\xc6\xb2G\xb0\xb26\x16\xdb\x9b+\x97@\xb2\xa3\xcazX\x9e\x7f\x024I\xd3\x85\x14\x97\x11\x17#@#\xd2\x0b\x83\x8d\xd8\xf4Ae\x88\xb2\xe2\xd8\x13\x80\xfb\x96\xac\x9b1h\xf7\x11\xfbP\xc1\xa8\xbeWG~;Z\x1d\xef\xe1*l\xc0PAK\xcf\xf5U\xd3\x00\xbc\xf6\xfb/\xba\r\xe8\x03\xab\xee\xfbr&,H\xa4y\xcf\x03&\xb8>\xa4z\xfd\x06\xb0JEDa\x89\xa0\xa2\x0b\x85S\x85-\xb3\x0c\tGo+K\xccs\xac\x82)\xb2\xfb\xb2!\xf2\xe9x\xce:\xcaU\xd5v\xd9\x98\x9ek\xfb\x9d\xf9\xb5\x85x\xb5\xb4\x96b\xae\xa0\xde\xfark\nmO\xde\x11S\x996\xe6\xa4\xeclO\x96\x12^2v~\xc0\x12\xd6\x18\xcc\xc5\x12\xb3\xdbj\x1d\xcc@\xc1<\xa5\t\xa5LJ\xaf\xe9\xba\xcd(\xd2u\xa5b\xe3Fp\x1c\x1d\xe6"mL }!_\x89&\x862\x15\xc2\x96\xea\xc4P\x0c\x03!\xa15\x95>\x99\rv\xe1.\x90l\xb0[\x19\xfa\x0cm\xc3t\xe5\x83ck\xd5\xb9\x90\x16\xd8\x85\x15\x99:\xa9\xc2\xa2\x15\\\xd6\x80<G\xa6v\xfc\xd7n\xf7\xe0\xe1\xab\x17/O\x1e\xfd\xa6\x06\xb5\x8albbBR\x9a8\x1d\x9e\x13K\xf7i.\x07\xf1\xc4\x8a\xe1\x1aF\x01,\x029\x1f\xc4\xea\xca\xf9(B\xf9\x85\xc385\xfa\x15\x13Y\x86X\x00\x1dO\xbfz\xf1~\xef\xe1~\xef\xa3\xe7\xdd?\xbf9y\xf9\x95\xbc\x12\xa4\xe6\xd1\xe3{\xdd?\xeew\x7f<\x90\x8a\xf1\xa0"\xea\x17\xd0\x9f3d\xa6\xd3*\x02D\xedY0Lw\xff>\x91\xc6\xbd\xef?=9\xdc\xeb~\xfdE\xf7\xf3\xa7\xe1\x1e\x04\x81\xbe\xae\x11\x85\r\\\x81\x82\x85\xa5S\t\xa9\x93\xc1\x8b\x1c\x96\'5\x9c)\x83\xb4(\x8c\xa2|U\xe4X\xa0\xa0\t\x06Iq\x11\xad\x9f\x93\t-=r\xd1\xa9\xc8\xa5\xdf\xb3\xbd\xbb\xed\xcb\xfa\x1e\xcb\xf2\x0f\x0fd\xa9\xcf\x81\xa0\xea\x9eW\x93h\x0c#\x18T\x94\x95\x19!\xac9\n\xc9%&\x1eCTssCz\xe0Q\xc8\xbd\xd6-\xe6\t\xf9\x1d\x90\xee=\xf8\xe5d\xff\xfe\xd1O\xbb\xe7\xc0\xab\xaf\x0bh]\n\xde\xe5\x95\xf1)\'\xabnD\xb2\xa9H*\x19I\xdd\x8cdg"\xc9dd!\xa66\xa9\xf9HRJ\xe4\xe3\xcdH*3\xdch\xe9\xe3\x0fv\x8f\x9e\xbf<\x87\x9b\xbaK\xfeS\xea\x95a\xfa\xf8\xc9\xe1\xc9\xde\'\xe1\xf8P\xbdy\x86\xf7bpP\x87\x180<d;\xab\xb9\x0b#\xfd\r\x00\x00\xff\xff\r\n47b\r\n\xccX\xedOZW\x18\xff\xbc&\xfd\x1fN\\\xbaa\xd7\xc1E\xc0\xae\xda\x90t\xa6/\x89\xed\\&\x8d_\x9a\x18\x84\x8b%E \xf7\xc2\xda\xf4\x13\x88\x82]UlV\xa5V\xd7b\xac\xcci\x14\x97\xd9N^\xaa\x7fL9\x87\xcb\xa7\xfe\x0b{\x9es\xee\xe5\xc5X`K?\x8cp\t\x9c\xf3<\xcfy\xde\x7f\xcf\x81\x9f\xc4\x9b\x82\x8e\x02\xa7I\xf5V\x00\x98\xd1\xdc\t\xb8jF\x0f\x80Jh\xe3\x04\xb7w\xca\x1f\xfc\xef\xd9\xd1\xe3\xac\xeeoT\x97\x92\xcd\xae\xb6D\x03\xbc\xc8x\xf1\xe9\x82\x91c4\xe2\x8e\xa8\xa2\xfexWj\xed\xa0\xe3\xaa\xb1}U\r\xbb\x83|\x9d/\x8dc\xfeB"E\x83P\xa5"\xe9`\x96\xec\xbb\xf2UpB\r\x0f\x12h\xf5@~\x06\x9b[\x89\xf8=\x00R:\'[IUw\xb3\xc0)u`\xe4h\x04\xe8g0j\xf9\x19m\xbf\x08\x8c\x8e\x06\x07\xefHuC\xcehP\xdcV\xa3\t\xb5n\xd7[\x911\x0f\xe7\xcb\xda\xdc\x0e\xcb\xa6\x05\xf9)j\xd1\x84\t}sXKl\x0b\x8a&8\xc2\xe6\xdc\nF\xb82$F\xfa\xc6\x86\x1e\x04_H\xb9\x81\x115Z\xa0\xc1\xc3\x1d\xec\x85\xcb\x81?\xd0\xe3\xfc\x14\x14\x02Z\xfa=\xea)\x990\x1apn!\x12p\xa5u\xb9\x81\x8a_\x18\xb8\x08\xc3\x03?\x8eC\xcaxT\t\xd4s\xaf\xce\xd0\xd7uy\x84-\xf6\xcb\x92M\xb2:\xccx!\xeai\x7f%\x11\xa5\x8a\xd1\xe2H\xd4\x9a\x9f\x90(n\x05\xa7\x01#\xb0\xcd\x9b\xa8\xd9\xf70<\x18\x96\x18.\xd1\x95\x12\x06Mp\x02\x0e\xadjD\t\x05\'\x9d\xd2#I"\xda\xdb\xbf!m\xc4\x82\x81\x81a\'[\x8fi\'\xcf\xe8\xfa6\x8d\xbf\x048\xac\x1c\xed\xd0|\x81e\xde\xd52\x87Z.\x0e\xca\xb2\xfcs\xed8Q\xdb}\x81\xe8\xf6d\x97\xa5\xd3tu\xfbcy\xbe\x06\x8c\xb98=\x88k\x9b\xb3\x9c\xf1\xe9\xe8\xc8\xd0\xf0uW\xc3X\x9a~F\xe7g\x81\r\xb7\x8bk\xf4\xe8\xa8\xfa|\x9b\xa6\xde\xb3\xe5\x83\x0f\xb1\xe9\xea~\x8c.,#2\xe7\x0fA\x1c=\xf8\x93\xbd\xc8\xd7R\x0b4\xb9*\xc4)2L\x93\xd0\xed+G{@5)G>\xc4\xe2h\x1f[)\xb0\xbf\x96A\xc2UKX\xd8P)\xfdB\xdf\xfc\x816$WQ\xcb\xcc;\x1a[E\x15\xe3):w @\x9e\x1e\xcf\xd1\xad\x14\x8b\xed\x00A-\xb3\x0f\xc0\x8c\x87\xe6\x0bti^\x98}\xf7\xa7\xdb\xb0\xf2\xe3\xc8\xa8K\x04IK\xbcg{\x9b\xa0\xb4>\xcd\x9cl\xb0x\x1e(\xb4\x182\xb0L\x8e\xce\xa1\xf4\x9b\xd7]\xb0(\xe2\x0c\xb7\x80)\x99\x84\xa2\x91\x16\xe5\xca;\x95\xd2f5\x1b\xa7\xb9i\xb0\xeac\xf9\xa5\xbe\xd5\x1cs=|\x9e\x90W\x0cyaEv\x82\xc5\xd0\x89\x14\xc8`\xd1\x16\xf8\x15\nhC\x81\x902@\xbe\xfcN\xc2\xd7`\x8f\xf3k\xbd\x19\xb4\xa7\x02=\xc9\x05\x95`\\,V\xb3\xf5\x9er/x\x0b\x9c9\x00\x8b\xf8\xfd\xae*+\xdf^\x9b\x84Z\x1d wB\x8f\xfd\x81\x80\xdb\xe20K\xc44\xe6\x0fzC\x0fU\xf2\x83\x8b\xf4\x9bm\x83dld\xac\xdf\xdeK`\x18\x0f\xc8c\xf2\xc4\xb0?bq\xd8.\x9bm\xfd\xc44|\xcbu\xe7\xf6%\x12\xf0?\x90\xc9M\xd9\xf3 \xd4K\x86\xee+0VX\xecv\xb3d\xee\xb3K6\xb3\xb5\xcfAF\xdd>\xb7\xe2\xd7\xd9\xf0\xf0k\x1e\x8f\x1c\x86\x83/Z.\xe2O|\xba\xb2\xa9\xad\xe5\x92Au\xfe\x1c\xaf\nt\xa5N\xffy<\x8a\xa9\xf2\xbfu)>B\x8d\x7f\xedM1\xef~\xd2\xa7>\x1f\xd0ze_W\xbe\'\x90\xc4&h\xad\x97\xf0\x1f\x9e\xde\x81\xf3\xe7\x08\xbc\xb0X\xea\xa1\xe8\xc0/\n\x0b\x9am0({\x9aD5$\x99q*3\x19\xc5\xa2\x8b\xbd\xd0A,\x17D\xb8\xa4^\x14$\xc4\x89OEV\xc3\xa1\xa0*w\x9d-\xdd\xa5a\xe3\x80\x88<\x15n\x08\xe76(\xb2\xe7g\x93]\xba\xd2\xdf^\x86nv\xa7\xf3x\x88\x1e\xde\xf7\x07\xe4\xee4C\x85\xf4\xd8|\x16\xfd\xce\xf2\xe27\x9d"\x8d\xa7b\xe2um\xa0"G\xa2\x8a\x91\xda\xcd\xe7a\xf3lLF\x88\x83\xd2#\xabD\xaa\xa5_\x1b\xb0GO\x12\xd5D\x8e\xcd\xa4+\x05~;<HT\x8aI\xc0\x88Ja\x96e\xb2\xec\xd5:\xa2C\xaaH\x17Kt\t\xb7\x00 j[{\xb8\xb8\xf6\x8a\xfd\xb6\xc5^\xe3[{;\xc3V\x10h*\xa5E\x18\x8bh9F\x7f\x7fZ\xdb(r\xfaX-\xbe\x00[\xec\xc91bP19\x11\x9d\xacN\x17\x00\x19\xe8\xe2k\xba\x96\xfd\x07\x00\x00\xff\xff\r\n4ed\r\n\xacY[o\xdaf\x18\xbe\xde\xbf\xf0\xd8\x05D\xaa\xc1\x86\x84\x92\x03h\x13\x9d\xa6J\xed4m\xd9v\x199\xb6\xa1(\xd4F\x90f\xa3\x17\x13m\x15\x12\x92\x12\x1a\xa5K\xba*\xdbB\xd7\xad\xd1\xd2\x18\xad\xd9r\x02\xc2\x8f\x99m\xcc\xd5\xfeB\xdf\xef\xe0\x13cK\xa4\xed\x86\xc4\xa7\xf7\xfc}\xef\xf3>\x1f4;\xb4q0\xb0q\x18\xf5\x86\xa5i\xd0\xe6P\xcbj?\xb3\xb4\x97\xb4\xdcs\xaa2\xc5,\xc8r\x81\x15\xf2\xb9%\xd9\xdbUf\xe4\xbb\xa9\xf4\xc8\xb7\x08\xa6\xa4\xc8\x12\xe6Z\xd2\xdd\xfa\xddM\x98\xd0\xcc\xda\x162R{l\xae>1\x9el w\xb4\x17\xe6\xeaI\xff\xa0\x05#\xab\xb9[7\xd6\x9a\xd0\xdd\xf5\xb3uh\xff\xd0\xac\xf5\xf3\r\xbd\xb3g]l!S\xa1m\x9bu\r\x825\x9b\xfe\xc4\xea\xfd`n\xfc\xac\x9f\xd6\xf5\xcesc\xf9h\xb0\x83C\xf3\xcbC\x08\x9c+\xb1Z7_7-\xad\x07\xed\xd6\xeaAS\xff\xd5Up\xba\x86\x06ml\x13\n_\xe7y\xbf\xfd\xaa\xdf>\xd4\xbb=\xd0\x8a_\xae\x98\xdf7\x8d\x937\xfdv\xc3h\x9f\xf7\x0f\xd6Q\x92\xb0\xd2\x99\x08\xb8\xfe\x8fq\x10\xf3j\x89\x86\x80\x81\xb6k5\xf7\x89\xff\x9f\x120\xf1\xff\xb9\xee\xf1\x1bEy\xc8k\x80>\x83\xca\x03\xaa\xd4\x01K\x80n`Z%\xfe8\x92pV\xbd.\x11\xeb\x9dK\xc0\x1b\x05\x0c&\t\x0er\x96#\x896\x080\x9f\x1eC"\xa0\xc8\x88\x954\x9e\x875\xb8\xe3(\x81~\xa3\x98\x1b5\\\x8f(g\x04\xd3|\xfc\xf9\xad[\xa8 I\xdev\xf7\t\xf3\x01z\xcc7Ms\xb7fi\x17\xfd\xaef\x1d\xc3\x8a8&\x88\xd0+\xdb\x93\xcc\xb6\xb1\xb6on\x1fBi\x11m\xe8\xb5\xd3\x8a\xb5\xfa\x1a\x8a<\xc6\x95\xbe\x89s%o\xedB~)\xda\xab\xecA6<\xd8\t\xa0\x13\xb8H\x16\x082lw\x1f\x01o\x86"\xc1\xc1\xcac\xf3\x04t\xed\x89\xc3\t7\xeaGF\xa3e\xbd\xfa\xc9\xa8\x1e\x11p\x87\xf4Q\xac\xabw\xab\xa0K?=\xd7\xdb\x15\xfdl\xd5h@\x1d\xd6\xa0_\x18\x8d\x1dp\xc3\xe8\xfefl\xa1\x85\x8a@\x82Q\xff\x9d\xb8N\x84\x18\x9b/\xfe\xea\xfc\xe8\x01\xcd\xa33\x84\x903\xde!\x1cHk\xfe\xb1n\xb5\xbeu\xa1^!\x85\xa43\x08\x83\xf6\x0e\xc0w\n)\xcf\xab\xb0\'A\xe8\xa7\xdcrv\x06l:qd\x8a9I(\x87K9E\x10\n\x05:hg#n\x04X>\\P\xb2t\xdc\x0e0\xe4\xe8$\x10\x9f\xe0`t\x91s\xd9;p7\xc6M\x90\t\xdc\xad(p\x1f\xd7\xb8\xbd\xe5\xd5\xea\xc4$b\x0fZ\x1c\xcbPT\x87\xae\x1a\x08\x9f\xbb\xc5\xfc\'{\xa3\xa3\xec\xbd\xce\xc7\\{\xa3\x89I\x9f\xbdC\xe16k\x15\xbd\x8dk\xecl\xdd\xa8\xd5\xe1\x12&\x08\x08\xfa\xa8\xed\x14\x1eB6\xf1\x90\x810\xfd\xe0Q\x97l\xb0\xe0\xce\xe8\xdd\x13U\xe5\xd3\xef\xacV\x0b}\xa3\xbd\xb4ZU\xdf\xaeK+\xc1\xa9!"\x16\xd6\x04\x11;XY1\x1a\xdb\xa3%_ZF\xc3U\xd5xhU\x1e\xd9-\xc6\xad$\x9b\xfd@\xb3\xe8|yI\xcdI8\xcah\x80\x88\xa0g\xac\xab\x92%#;\xfa\x94\xce\xf2\xf6\xbcx\xbb\xfcY.\xab\x08\xd0@ew\xd4\xfc\x97)\xd4\xcf\x8f`<\x9dS2\xea\x1c\\\x8a\x0b>Z\x1aQ\xcd\x88\xa4K\x0b\x8brV-\x96G\xc8\xf8PY,\x96g\x85\xec\xa5\xe2\x03\xde6~\x05\xe3\xf0\x87\x8a\xfc\xf5\xe2\x1c@\x80%\xcf\x0b\xf4/\xe1qGM\xd66MpC.\x89\x01\xbcXe\x89y\x9fq\xf9\x18t\x8b\x95\xd0\xf9P*\nS>\xcb%Xn\x9c\x89rS|\xdcF 3\x02!\x0b\x82\x97\x92\x05\xc1Q\xb443x\xb6l\xb5\xda!\xbf\xce9t<j\xf3?\xe1p\x98*\x1bc\x08\x174\xfc\xf6\x10a\xe4\xfd\xc0\xb6\x8f\xb9"\xbd\x8a\xe4\x81\\Jk\x0cSq\xa9~g\xdb\xba\xd8\xc4\x86\xdb\x8e\x07\xde\x0b0\xaa"\xe6s\xe2B2\xf0\x81$\xcd\xaa_\xde\x0f\xd1\xef\xc7\xa6\t\\c\xc8aL \x05]\xcb\xdai\x10\xb2\x8e\xe6\xc3\xfd\xe7\xf2s!\x01Y\x91&\xde\x96\x92\x8b\xc5{\xf25q\x1e\x95c\xf6\xa6\x94\xe4\xe3\xb1\xf1\x89\xc45|:\x04\xa5v\xd3\xf1\xc2~\x07F\xad\xa4\xffd\xc9~\x82\x86\xb6\x8f\xee\x81\xdf\xc1\xf1\xf8dTJdx6\x9a\xe1EV\x8e\xf1<\x9b\x90\xb8(;\xc9\xcd\xf3\xbc\x08?\xd7\xa5x\xd0\xd1\x91.\xcaP\x1c\xd2\r\xf8I\x06Q\x85D\x12\x11Z\x1fS\x1c\x17\x9c\xce\xab\x82\xf4\x05\xa42\x8d\x12\x13r-\x1b\xf3\x9eK\xbd\xf37\xce\x8dP]\x0ca\x0c\xff\xac< Y7\xb43\xe8\xbb^\x8e\xce>Hz\x97\x16@\x89\x1c\'\xf9\xd6\x95\xcd&\x96\xd8B^\x10\xe5;j\x1e\x9f\x1fQ\tW8\x8a#\x9f\xdf\x16\x14!+#ZB\x91\xbf\xc2\x0cc\xda\xf7 46\xed\x7f\x13\xd0\x8a\x02\x9a\xecd\x858\x9f\xcf\xb6\x89A\xbbt3j\xf1n\x90\xaet\xfb&\xbe\xe790\xf3\xdf\xc7t\xda[\x00\x00\x00\xff\xff\r\n2c7\r\n\x94Z\xddk\xd4@\x10\xffW\x16\x047\x82\xe5\xec\x15\x11j9hO\xd0\xa2\xd6\xc3\x9e\xcf!w\xd9p\xa1w\xd9#\x1f\xb5E\x04A\xaa\xe2\x8b\xf4\xb5(\xa8\x08\x15\x11\x1f\x95\xbe\xf4\xaf\xb9\x94\xde\x7f\xe1L\xf6#\x9bd{\xf4\x9e\x12\xf6\xe3\xb73\xb3\xb33\xb3;S\x02\xc1W\xae\xb5;\xe2/i\xc3L\xe8\x95"o\x9fv\xf4\x01\xa2\xf8\xe3\x82\x1e\xc3Mb\xe4\xa6\xe14\xc1\xa9\xe2\x1e\xa2Nv)\x92u4\xbc\xc8\n\xd5*O\xa5\x86?\x17\x10\x92\x06L\xe988\x0c\x97\x18G{n\xb5;\xa1$\xce\xc0\x10\xc3\xf2,\xdeg1r\x1eB{\xe8O\xb8\x0f\x8c\xe2\xebm8\xa4\x9d\xfc\xc3?\x08\x1d\xc5\xf6\x17;\xabH\xbaq%\x01=\x10>\xae,\xe7B\xa8=\xff\xf2\xbd:\x17\xd4\x8bv\x84\xe7\x9f\x7f\xfb;\x7f\xfb\xd3<\x8f\xd6\x9d\x11i\x940\x02Jm~\x83z\xbe\x8b\xca\xa3\x0c\xd1\x80\x1f\x08\xceU{\x86\xaa`\xf66\x97\xc3\xa1mK;\x9f\xaa\xe9h\x9al\xfb\xaa^\xd1VK\xfdq\x01\xadpR\x96\xf1%\x18\xe6\xa6\x92E\x88\xed\xa5\x11\xf7\x06\x96\xfeG\xa0\x0c\xe0\x13\xfb\x1cb\xa4\xc5\x88\xe6q\xa4\xb5\xe3\x88\'\x01o\xc9Ax\xd0\x93\xef\xc1\xb0\xcf\xf2E\x84\xa5}\x11H;A\x16\x15A\x08qn\x91W$\x8c\x861C\xa1\xdb\xad\x10y}\x9b\xdc\xbd\xa3P|\x86\xe1C\xbc\xe9\xf7\xdbN\xa3\xad\xbbji\xc3q\xe5\x0b\x07Z\xbb\x1d\x10\xe9f\xe4?\x1e\xe8\xd1\xd8\x8a\xe6V\x87\x1e\xba\xe7\t\xf4 +\xdb\xe0\xf4\xb7P\x12\x8e6\xe62\xc9_\x90Y\xfcK\xfb\xad\xff\x95\xc5VX\x0fY\xda\x03\xef\xbf\x032CH\xc72\xddD5\x0c\xb7I\xe7\xb3i\xfa\x027\xb3\x800\xa0\xcd\x1d\xac\x11i\x12\xd6\x84.dS)\x060b\x92\x9a\xd5\x97\xd9\x11{\xd2\xc6H\xab\x10\xb8z\xcd\xe0\xee\xf9\xee\x08=B\xe9\x14\xcc,L\x02!\xc7\x96\'\x93\xcd\xf5\xd6\xa7*i\xd3L\xcc\x1b\xe1\x16\x1e\x8e\xed\x94MDi\xd7\x9a\x8e\xc2\xbc\xc2\xb8\xc9\xccJ~\xf4;?\xfe\xb8\xd1\x1a\xad5*\x12V\x10\xe0\x9a\x8eF\xe9\x08j\x8fSu\x14Z`\xf5|\xdd\n\x96\x84E>0\xa9\xde\x8a\xfc0\x01\x1fw\xb8\x1e\x01;K.\xfc\x80\x05^6\x86\xf0U@Vih\xa4\x0b\xc7,He\xd9\x9a6\x8cR\xa05\x1aQ\xe2C>\xce&\xd1\x92\x04\xed\xc2\xc4n1\xb1A\xcb\xe2\xe4\x9f\xb1\xc7vM\x92\x03\xc8\xec\xfc\xf4\xf2\xfc\xec\xe2\xeb\'\xa1Bf\xc1\xc2\x159)\x8bJ^g\x96\x12H\xc0y\xca\xca\xfa\x07S\xef\xba|z\x18\xe35\x90\xdc\x1c\xc2\xef}\x08\xa5\xee\xd5\xeb\xf7l\x07\x06\x01\xedYK>a\xe4\xf2\xfd\xaf\xfc\xcf\xc9\xec\x0co\x82\x17\x9f\xdf\xe4?NMV7Z\xaa\x1e\xa7%\xab\x1a\xff\x03\x00\x00\xff\xff\r\na\r\n\x03\x00\xba\xdf\xb2\xb2\xe9(\x00\x00\r\n0\r\n\r\n'


HTTP/1.1 200 OK
Date: Fri, 30 Jun 2017 07:00:02 GMT
Content-Type: text/html; charset=utf-8
Transfer-Encoding: chunked
Connection: keep-alive
Vary: Accept-Encoding
Cache-Control: private, max-age=10
Expires: Fri, 30 Jun 2017 07:00:12 GMT
Last-Modified: Fri, 30 Jun 2017 07:00:02 GMT
X-UA-Compatible: IE=10
X-Frame-Options: SAMEORIGIN
Content-Encoding: gzip

4a0
�\000\000\000\000\000\000�V[oE~N����JVAt��S'vȺJb7	u.�9��c��,;��W*��*JD�y@��� **ğ���_0�k�vJ��-���s���˜٫W�e���nd�#\��zeN��@Z1���[T
��ju���r�ϑ0��(�I����E�����1_h�bT *���i���
<�\000�b�!ѹ	2c�,Jo���(�̪!�{��w�孭�㧿��}tp��{�ٳ�����V�����~��a���9#t!}Lk@�=�I��0,�5�#bj\�	�B��㣲��:���(V�-溌F�����o���T��.C�vs-{'>�1߱�j�Q�).N���;	V_�b2}\l��*�tQ�^��aʍRG�Z�OI�?����ͭ�D�Z(�g��z>���
��t�\IT�|�e�tg��Sl\V��]\000�����
��#D�6xÅ��B�`f:�����!z?���@2Y��⊞+�;k�Q�
��30�X�ź�dǵ��R:�����m��R������>�o�\���@>�
�9Bx���l6�UU�QYf�VgۨTR�gae�ƲG��6ۛ+�@���zX�4IӅ�#@#�
����Ae���������1h��P���WG~;Z
��*l�PAK��U�\000���/�
����r&,H�y�&�>�z��JEDa���
�S�-�
	Go+K�s��)���!��x�:�U�v٘�k�����x���b����rk
mO�S�6��lO�^2v~������j
�@�<�	�LJ���(�u�b�Fp

�"mL }!_�&�2��P
!�5�>�
v�.�l�[�
m�t�ckչ�؅�:�¢\ր<G�v��n���/O
����lbbBR�8
�K�i.�Ċ�F,9����(B���85�Y�X\000
O�z�~��~���?�9y�������{�?�w<���"�П3d��*D�Y0Lw�>�ƽ�?=9��~�E���
����
\����S	����
�'5�)��(��|U�X��	Iq���	-=rѩȥ߳�����
��d�ρ��W�h
#T��!�9
�%&
CTssCz�QȽ�-�	�
��=��d���O�����
h]
���)'�nD��H*I݌dg"�dd!�6��HRJ���H*3�h��v���<���K�S�a������'��P�y��bpP�0<d;��
#�
\000\000��
47b
�X�OZW��&�N\�a��E��ڐt�/��\&�_���%E ������]UlV�V�b��i��N^�L9�˧�
{�s���X`K?�p	��<�y�ρ�ě���I�V\000���	�jF�Jh��w�������oT��ͮ�D��x�邑c4⎨��xWj�㪱}U
��|�/�c�B"E�P�"�`���UpB
h�@~�[��=\000R:'[IUw��)u`�h�g0j�m����HuC�hP�V�	�n�[�1����˦�)jф	}sXKl
�&8���
F�2$F�Ɔ
_H��5Z���
�ˁ?���Z�=�)�0pn!p�u���_��?�C�xT	�s����uy�-�˒M�:�x!�i%����HԚ��(n�#�͛���0<�.ѕMp�jD	'��#I"�ۿ!mĂ��a'[�i'���6��8�
��|�e��2�Z.ʲ�s�8Q�}���d���tu�cy���8=�k���������uW�X�~F�g�
��k���|��޳����~�.,#2�A
=�����R
4�*�)2L���+G{@5)G>��h[)���A�UKX�P)�B���6$WQ��;[E�):w @�
�ѭ��\000A-�����
ti^�}��۰��ȨKIK�g{���>͜l�x
(�2�L�Ρ��]�(�
��)������;��f5��i��c����
s=|��W
yaEv��Љ�`��
hC��2@��N��`��k���=��`\,V���r/x
�9\000����*+�^��Z
 wB������0K�4�zCU��m�dld���K`�c�İ?bq�.�m��4|�u��%�?��M�� �K��+0VX�v�d�K6���AF�>������k
�
��/Z.�O|�����Au�
�
t�N�y<���u)>B��M1�~ҧ>�ze_W�'��&h����ށ����X���/

�m0({�D5$�q*3Ţ���A,D��^$ĉOEVá�*w�-ݥa〈<n�6(��g�]���^�nv��x�
����4C���|����7�"��b�um�"G������a�lLF���#�D��_�GO�D�ͤ+~;<HT�I��Ja�e���:�C�HKt	�\000 j[{�������^�[{;�Vh*�E�h9FZ�(r�X-�\000[��1bP19��N\000��k���\000\000��
77b
�[o�V�y��
ҜJ���Rz���Ī��l��;��Ԏ���M�������Cek[+��[o���,v����}��9�$�-�^Z����~��!ء���qh�Q�B�ÐU{jT_Rs�U����l@�ȓ�3��K㱸�.�S���Z�KP�饇Hd��>�@{���T_�sۍכP���em~�{}w�?���b}�8|��B���U�p|�8�Y_���S��?Ӧ�5�����.Ά8S�߬�#���W6��y,�M�P|����Fm�~pX��E������Q�h����T���?��WɌ��"� �����$���Xw�Rn�R�f�Ej%K��@�J�� �Zu�D��~B��5�I�YבH\000菶@`d�J*ύ�XH �(�bɴG��i�ݼr
��my�t>\000��vU_.���A�؂�E2B'l�2k����xL�`�m;Ec�
y4���;�w�.�f{�І#w��	X$	[^�ě��`s���
�V��
���ʦ���6�$w������U�٫׊��9�vX�x�U�\000���C���$h�?	������_
I���0s6=����-�?ک^6��9�A�^�4�ܛ�����*�iő�ɢ0ՙ�A�fi����;�J���>��N|�]!(]$9=
��P��m��Mg.�T&$z�rL�Qm�h@|���O�F��=���Fz.��m�^*�k���.h�2��
���N�%h�,20�o�; ����h��~267�L���9���,"`�N���Y����f�jU��F�

1�%��֢#S��,�R�"��6�\000)��(��Y�xuꆜV��]j
S���#f>-+)5?�c��4���I
RZ�My��\)䦆���}�0~
�̃�t���`ұ��'}\�ʚ�	.I��ϼ���}���\
�8�E���z�s\$��fH�@����ޫ-�5�N�5�gǣ�����I�up�Ժ��a�<���N�^Ex\000��5Z[q���c�p�$�1�;��T%���c���8�~󭟞��#�G�1�D-�I�4�>쇓�BR'��
�	�lr�1=(����zΚ�!0�A�
�J��d�������͟�{R�@$N�h8
�C����H8��?��n���I`
�%�3���{��>zC!�/�
�נ�8*�oS��K}��s#�.�t
�.�!Zת�w�=:6H��@���\��u�lFHJ�jƜQ�ő�WEHKؖP�[f�1�z���s�lELLY���gF"�L7���yz�٢�����i���׍Q���&,L�0�Ǭ
��C�*��DA���(�C�ͶEҋ�Y�-�穅_' (
8���6D�Q���y��M�#�RnR�!�2���*�ؽ��|L�ۆԑ���,#��{	�#fzR����`^|�D���V�޺�>zj��Qd(��� &�x�#Qo������m;:��XW��8�&/��.Zض�@3���~Φ��A�|0ı��_�1@L
V!G:
��:�-�oV�)�����iGD*
�Dڟ�P�$��wp�q���I(to/�}��
1(���C�8
���
k���p���"���_�X�qݭ�zXo��de��g(	�����$�|���zf
���,� �_�!H��q'T��v��U�p�i�p�vj��H'a�Mٸ>p�$-^�NG��6��
�W
jϙi�vPpNa�r|&�as��U6�i�;�-�
�i�|���0�tnt��M�і����Ѷ/����Z��
(,�����I�"��W$�y�qS�
��/I)a"�+馡m\��R�ٚ��@[hD�'��ĸ�݀�q�`-��
:��$�������J�����̤<L�4��@R�Z����vW�S9,�O����������.
�Z��g̾Ҫ��X	��E�嚓�� �
'H�j�\000\000��
a
\000�߲��(\000\000
0

񠀹


"""


req = 'GET /kuoaidebb/p/4703015.html HTTP/1.1\r\nHost: www.cnblogs.com\r\nConnection: keep-alive\r\nPragma: no-cache\r\nCache-Control: no-cache\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: zh-CN,zh;q=0.8\r\n\r\n'
#req = 'GET /bundles/blog-common.css?v=m_FXmwz3wxZoecUwNEK23PAzc-j9vbX_C6MblJ5ouMc1 HTTP/1.1\r\nHost: www.cnblogs.com\r\nConnection: keep-alive\r\nPragma: no-cache\r\nCache-Control: no-cache\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: zh-CN,zh;q=0.8\r\n\r\n'
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
    # \r\nhex\r\nlen(data)=hex for Transfer-Encoding
    
    # find \r\n\r\n
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
        while rest_length >0 :
            buf = conn.recv(rest_length)
            if buf:
                data += buf
                rest_length = rest_length - len(buf)
            else:
                raise StopIteration('rest_length remains')
    #'Transfer-Encoding: chunked'
    elif 'Transfer-Encoding' in headers and headers["Transfer-Encoding"] == 'chunked':
        rest_data = ''
        rest_read_required = 0
        while True:
            # '\r\n' required
            if not '\r\n' in rest_readed:
                buf = conn.recv(1024)
                if buf:
                    print(repr(buf))                    
                    rest_readed += buf
                    continue
                else:
                    raise socket.error('READ INTERRUPTTED')
            if rest_read_required > 0:
                rest_data += rest_readed[:rest_read_required]
                rest_readed_tmp = rest_readed[rest_read_required:]
                # still require to read
                if rest_readed_tmp == '':
                    rest_read_required -= len(rest_readed)
                else:
                    rest_read_required = 0
                # remove '\r\n'
                if rest_read_required == 0:
                    rest_data = rest_data[:-2]
                rest_readed = rest_readed_tmp
                continue

            rest_read_need_str, rest_readed = rest_readed.split('\r\n',1)
            #print(rest_read_need_str, rest_readed)
            # binascii
            # int('4a0',16)
            # \r\nhex【\r\n(split)】len(data)=hex【\r\n】0\r\n\r\n
            rest_read_required = int(rest_read_need_str, 16) + 2
            # 0\r\n\r\n done 0\r\n\
            if rest_read_required == 2:
                # the last \r\n
                last_end_len = 2 - len(rest_readed)
                assert last_end_len >= 0 , 'EXCEEDED_EOF:%s'%last_end_len                
                if last_end_len > 0:
                    last_end = conn.recv(last_end_len)
                    assert len(last_end) == last_end_len , 'BAD_EOF:%s'%last_end
                """
                \xff\r\n\x03\x00\xba\xdf\xb2\xb2\xe9(\x00\x00
                \xff\r\na\r\n\x03\x00\xba\xdf\xb2\xb2\xe9(\x00\x00\r\n0\r\n\r\n
                \xff\r\n\x03\x00\xba\xdf\xb2\xb2\xe9(\x00\x00\r\n
                """                
                rest_data = rest_data
                # Content-Encoding: gzip  # gzip,deflate,compress
                # http://guojuanjun.blog.51cto.com/277646/667067
                # https://stackoverflow.com/a/8506931/6493535 # zlib
                # python3 # gzip.decompress(str)
                # https://stackoverflow.com/a/2695575/6493535
                # all
                if 'Content-Encoding' in headers and headers["Content-Encoding"] == 'gzip':
                    print(repr(rest_data))
                    import zlib
                    rest_data = zlib.decompress(rest_data, 16+zlib.MAX_WBITS)
                    rest_data_length = len(rest_data)
                    headers.pop('Content-Encoding',None)
                # ERR_INVALID_CHUNKED_ENCODING
                headers.pop('Transfer-Encoding',None)
                #headers["Content-Length"] = rest_data_length
                headers["Content-Length"] = len(rest_data)
                data = headers_unparse(action, url_path, ver, headers, rest_data)
                break
            if len(rest_readed) >= rest_read_required:
                # remove \r\n
                rest_data += rest_readed[:rest_read_required-2]
                rest_readed = rest_readed[rest_read_required:] 
                rest_read_required = 0
                continue
            else:
                rest_read_required = rest_read_required - len(rest_readed)
                # remove '\r\n'
                if rest_read_required >= 2:
                    rest_data += rest_readed 
                rest_readed = ''
                continue

    return data

def socket_client_block_no_keepalive(req):
    data = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.cnblogs.com', 80))
    s.sendall(req)
    # manually s.recv(100)
    # tcp     4142      0 10.8.1.238:41278        101.37.97.51:80         
    # CLOSE_WAIT  7823/python          关闭 (0.00/0/0)
    # ==> we read from buf
    while 1:
        buf = s.recv(100)
        # but = '' ==> buf is empty ==> done
        if buf:
            data += buf 
        else:
            break
    print(repr(data))
    #s.sendall(req)
    # tcp        0    441 10.8.1.238:41278        101.37.97.51:80         
    # CLOSE_WAIT  7823/python          打开 (1.70/3/0)
    # but nothing in buf ==> we don't have set keepalive, so they don't deal it???
    

def socket_client_block_no_keepalive_transferEncoding(req):
    data = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('www.cnblogs.com', 80))
    s.sendall(req)
    data = parse_request(s)
    print(data)

if __name__ == '__main__':
    #socket_client_block_no_keepalive(req)
    socket_client_block_no_keepalive_transferEncoding(req)
