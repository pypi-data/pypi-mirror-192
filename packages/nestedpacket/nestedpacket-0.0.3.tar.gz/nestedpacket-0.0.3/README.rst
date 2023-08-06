NestedPacket: Headers and Trailers and more
===========================================

**NestedPacket** is a framework and packet library for digital design verification. It is useful for generating meaningful random packet traffic and for unpacking collected byte streams. The base class ``NestedPacket`` is used to define the headers and trailers for each packet layer.

.. code-block:: python

    from nestedpacket.ethernet import EthPacket
    from nestedpacket import TextBoxPrinter

    eth_pkt = EthPacket()
    eth_pkt.randomize()
    byte_list = eth_pkt.pack()

    print(byte_list)

    eth_pkt_2 = EthPacket()
    eth_pkt_2.unpack(byte_list)

    printer = TextBoxPrinter(25, 35)
    print(printer.sprint(eth_pkt_2))


Console output: (note the preamble is short because its length is randomized)

.. code-block:: console

    [85, 85, 85, 85, 85, 213, 72, 137, 105, 49, 163, 120, 204, 27, 164, 237, 180, 72,
     8, 0, 74, 145, 0, 0, 14, 55, 23, 28, 206, 17, 0, 0, 46, 22, 51, 170, 44, 251, 28,
     ...
     141, 214, 90, 99, 94, 139, 211, 133, 110, 172, 124, 163, 37, 174, 42, 83, 179, 43,
     53, 101, 191, 123, 228, 34, 114, 127, 198, 15, 169, 225, 95, 126, 22]

    |-------------------------------------------------------------------|
    |                          Eth-Packet-0002                          |
    |                                                                   |
    |  length: 521 bytes                                                |
    |-------------------------------------------------------------------|
    |                             EthPacket                             |
    |                                                                   |
    |                  preamble ->  55 55 55 55 55                      |
    |                       sfd ->  0xd5                                |
    |                                                                   |
    |     header[0]  0x55 55 55 55 55 d5                                |
    |-------------------------------------------------------------------|
    |                            EthMacFrame                            |
    |                                                                   |
    |                 dest_addr ->  0x48896931a378                      |
    |                  src_addr ->  0xcc1ba4edb448                      |
    |                                                                   |
    |     header[0]  0x48 89 69 31 a3 78 cc 1b a4 ed b4 48              |
    |-------------------------------------------------------------------|
    |                           EthMacDataUnit                          |
    |                                                                   |
    |                  eth_type ->  0x800                               |
    |                                                                   |
    |     header[0]  0x08 00                                            |
    |-------------------------------------------------------------------|
    |                             Ipv4Packet                            |
    |                                                                   |
    |                ip_version ->  0x4                                 |
    |             header_length ->  0xa                                 |
    |                       tos ->  0x91                                |
    |              total_length ->  0x0                                 |
    |                        id ->  0xe37                               |
    |                        df ->  0x0                                 |
    |                        mf ->  0x0                                 |
    |           fragment_offset ->  0x171c                              |
    |                       ttl ->  0xce                                |
    |                  protocol ->  0x11                                |
    |                  checksum ->  0x0                                 |
    |                     ip_sa ->  46.22.51.170                        |
    |                     ip_da ->  44.251.28.125                       |
    |                   options ->  [45 08 a7..8 08 12 47 66 78 61 d7]  |
    |                                                                   |
    |     header[0]  0x4a 91 00 00 0e 37 17 1c ce 11 00 00 2e 16 33 aa  |
    |    header[16]  0x2c fb 1c 7d 45 08 a7 51 8e 46 45 95 91 30 e5 48  |
    |    header[32]  0xe8 08 12 47 66 78 61 d7                          |
    |-------------------------------------------------------------------|
    |                            UdpDatagram                            |
    |                                                                   |
    |                  src_port ->  41467                               |
    |                 dest_port ->  0                                   |
    |                    length ->  0x0                                 |
    |                  checksum ->  0x146a                              |
    |                                                                   |
    |     header[0]  0xa1 fb 00 00 00 00 14 6a                          |
    |-------------------------------------------------------------------|
    |                   0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15  |
    |                                                                   |
    |    payload[0]  0x26 7a 42 64 11 1a 8d f8 81 68 e6 fb 03 fc 34 66  |
    |   payload[16]  0x5a 68 ab 08 e0 f1 7b 05 60 43 a2 a4 4b 2e 8e 29  |
    |   payload[32]  0xfc bc 88 80 42 42 2a 95 c4 84 69 e5 31 3d 62 8a  |
    |   payload[48]  0xf8 b8 fd 33 3f 53 83 2a 4b c2 d1 76 fd 25 b9 66  |
    |   payload[64]  0x93 43 83 98 e7 4d 4e 3d b6 45 c7 87 97 cf 4f a5  |
    |   payload[80]  0x2d 8d 83 dd f8 e6 69 ee 00 b3 9d 35 69 ce 76 b2  |
    |   payload[96]  0x31 92 4f 56 0b 28 ce 4c d7 9c 07 d5 f3 81 a8 82  |
    |  payload[112]  0xba 71 0a 28 53 ec af 95 4c 10 87 75 0e 1c 16 e5  |
    |  payload[128]  0x45 fe 8e ec e3 2a 23 5f 17 95 84 0f 4a 16 d2 d6  |
    |  payload[144]  0xe4 40 7c 43 84 b6 ed 72 73 04 4d ee 9a 8f 5c f4  |
    |  payload[160]  0xe1 43 74 b3 04 b8 cb 86 e6 4b 9c b5 9e 00 1e 5a  |
    |  payload[176]  0x47 c0 f3 23 31 e1 b9 62 ad 07 34 80 8e 5e 9d e5  |
    |  payload[192]  0x51 32 c7 3d 12 40 39 d4 5e 17 a5 95 2b e1 49 e8  |
    |  payload[208]  0xbb ff c2 c4 71 3d ad 28 27 45 45 3b 5d 0a 77 ed  |
    |  payload[224]  0x39 fa d8 7a d5 78 21 f9 9a a6 38 da 2d ed 96 05  |
    |  payload[240]  0xdd 95 e6 83 85 e3 b7 a7 74 15 77 73 26 76 d0 db  |
    |  payload[256]  0xc0 c4 22 64 64 13 26 e6 09 28 1e da 84 5c 11 ea  |
    |  payload[272]  0x3e ea 4a 8d 08 5a 8b 7b 76 64 54 e4 df 15 59 40  |
    |  payload[288]  0x3f cd b9 4a 55 fe 56 7b 33 d3 2f e8 e6 4b cd 38  |
    |  payload[304]  0xe6 42 f6 48 c5 80 56 e8 80 19 5a 4a e2 d2 3c 61  |
    |  payload[320]  0x0e 3e 29 70 99 1c a9 b1 bf 49 dd 77 a8 83 40 e9  |
    |  payload[336]  0x17 a6 26 6b 6d 2d 0b e4 32 05 2e 63 a7 96 e5 2b  |
    |  payload[352]  0x30 34 0a 6c de 6a d5 60 76 80 47 f2 25 b5 91 41  |
    |  payload[368]  0xed 49 88 c6 f5 43 51 7c d3 11 30 b0 b1 a3 f3 e3  |
    |  payload[384]  0x9a 11 1d af df 98 d2 b3 76 51 af 73 da f4 3d c8  |
    |  payload[400]  0x75 21 9d 8c 28 da d3 06 32 30 44 14 c4 58 55 3c  |
    |  payload[416]  0xcb 33 bb 2a 8d d6 5a 63 5e 8b d3 85 6e ac 7c a3  |
    |  payload[432]  0x25 ae 2a 53 b3 2b 35 65 bf 7b e4 22 72 7f c6 0f  |
    |  payload[448]  0xa9                                               |
    |-------------------------------------------------------------------|
    |                            EthMacFrame                            |
    |                                                                   |
    |                       fcs ->  0xe15f7e16                          |
    |                                                                   |
    |-------------------------------------------------------------------|
