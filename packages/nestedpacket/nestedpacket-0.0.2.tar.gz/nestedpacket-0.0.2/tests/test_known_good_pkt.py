import pytest
from nestedpacket import NestedPacket
from nestedpacket import EthPreamble, EthMacFrame
from nestedpacket import TcpPacket

@pytest.fixture()
def good_packet_1():
    eth_pkt = EthPreamble()
    eth_pkt.unpack([int(x, base=16) for x in """
        55 55 55 55 55 55 55 d5
        b2 d9 b1 29 68 62 27 72 f0 9b ff dd
        08 00
        4c bb 00 87 67 1b 21 43 0f 11 00 00 a3 57 74 a0
        62 f7 e8 c3 d0 72 dd 34 43 e9 02 fe ec 1c 85 ea
        d2 02 28 cb 04 ce 5b fd bc c1 a0 55 91 c2 21 65
        6b 1c 31 5e 00 57 69 3b
        be 98 d7 a2 67 b5 7c c3 4d 34 90 d4 17 88 e6 76
        2c d5 11 49 dc 05 fa 96 8b 1e 3d 55 70 23 cc fc
        b0 5c 56 0c 4f 6a b3 3d e1 64 e2 6a b7 88 9f 26
        5b cf 4f d3 f9 a3 1f 9e 27 0e 7c 7c a4 28 ec 09
        d0 c3 60 1e 12 81 00 1e b5 8a af 17 ee 75 72
        62 38 2f b2
        """.split()])
    return eth_pkt


@pytest.fixture()
def corrupt_packet_1():
    eth_pkt = EthPreamble()
    eth_pkt.unpack([int(x, base=16) for x in """
        55 55 55 55 55 55 55 d5
        b2 d9 b1 29 68 62 27 72 f0 9b ff dd
        08 00
        4c bb 00 87 67 1b 21 43 0f 11 00 00 a3 57 74 a0
        62 f7 e8 c3 d0 72 dd 34 43 e9 02 fe ec 1c 85 ea
        d2 02 28 cb 04 ce 5b fd bc c1 a0 55 91 c2 21 65
        6b 1c 31 5e 00 57 69 3b
        be 98 d7 a2 67 b5 7c c3 4d 34 90 d4 17 88 e6 76
        2c d5 11 49 dc 05 fa 96 8b 1e 3d 55 70 23 cc fc
        b0 5c 56 0c 4f 6a b3 3d e1 64 e2 6a b7 88 9f 26
        5b cf 4f d3 f9 a3 1f 9e 27 0e 7c 7c a4 28 ec 09
        d0 c3 60 1e 12 81 00 1e b5 8a af 17 ef 75 72
        62 38 2f b2
        """.split()])
    return eth_pkt

@pytest.fixture()
def good_packet_2():
    eth_pkt = EthPreamble()
    eth_pkt.unpack([int(x, base=16) for x in """
        55 55 55 55 55 55 55 d5
        90 35 6b a0 cd 79 cc cd ef a5 d3 ee
        86 dd
        69 ed 04 f9 00 6a 06 62 05 28 b0 df 0d 65 6f 9d
        7b 97 34 6e 6a b7 eb 45 ea 4c d7 1c a8 21 d4 b1
        47 3f b3 aa 99 fc 16 bc
        76 7d 9b ea 79 8b 06 55 ca ad 2b cd c0 39 00 c8
        c8 2b 9b 88 3d de de 0a f9 a4 9b 82 33 14 ee 9e
        1e 04 22 30 39 14 c9 06 26 d7 6f 91 ea 1f 62 92
        53 81 2e 35 cb f8 92 ee a0 20 14 21 69 d1 16 97
        7a 46 06 d3 7f 07 1e 83 4c 4b ff 10 7d 59 f8 47
        e5 7b 35 bf 93 2c 6e 1d ac 83 1b 5b 01 30 75 17
        b5 4c 85 58 c7 97 1d 03 c8 25
        f6 66 63 64
        """.split()])
    return eth_pkt


def test_known_good_fcs_1(good_packet_1):
    assert good_packet_1.get_nested_packet(EthMacFrame).calc_fcs() == 0x62382fb2

def test_known_good_fcs_2(good_packet_2):
    assert good_packet_2.get_nested_packet(EthMacFrame).calc_fcs() == 0xf6666364

def test_known_corrupt_fcs(corrupt_packet_1):
    assert not corrupt_packet_1.check_fcs()

def test_ipv4_get_field(good_packet_1):
    assert good_packet_1.get_field_value("ttl") == 0x0F

def test_udp_get_field(good_packet_1):
    assert good_packet_1.get_field_value("dest_port") == 12638

def test_ipv6_get_field(good_packet_2):
    assert good_packet_2.get_field_value("tos") == 0x9E

def test_field_change_fcs_corrupt(good_packet_1):
    good_packet_1.set_field_value("tos", 0xaa)
    assert not good_packet_1.check_fcs()

def test_field_change_update_fcs(good_packet_1):
    good_packet_1.set_field_value("tos", 0xaa)
    good_packet_1.update_fcs()
    assert good_packet_1.check_fcs()

def test_known_good_tcp_checksum(good_packet_2):
    tcp_header = good_packet_2.get_nested_packet(TcpPacket)
    assert tcp_header.calc_checksum() == 0xC82B

def test_field_change_checksum_corrupt(good_packet_2):
    good_packet_2.set_field_value("src_port", 20222)
    tcp_header = good_packet_2.get_nested_packet(TcpPacket)
    assert not tcp_header.check_checksum()

def test_field_change_checksum_good(good_packet_2):
    good_packet_2.set_field_value("src_port", 20222)
    tcp_header = good_packet_2.get_nested_packet(TcpPacket)
    tcp_header.update_checksum()
    assert tcp_header.check_checksum()




log_pkt_1 = """
  |--------------------------------------------------------------------|
  |                        <sw_eMAC-tx-pkt:0000>                       |
  |                                                                    |
  |        length: 161 bytes   start: 80.12us   end: 81.40us           |
  |--------------------------------------------------------------------|
  |                             eth_packet                             |
  |                                                                    |
  |             preamble ->  [55 55 55 55 55 55 55]                    |
  |                  sfd ->  0xd5                                      |
  |                                                                    |
  |         header[0]  55 55 55 55 55 55 55 d5                         |
  |                                                                    |
  |--------------------------------------------------------------------|
  |                          pkt_eth_mac_frame                         |
  |                                                                    |
  |                   da ->  b2-d9-b1-29-68-62                         |
  |                   sa ->  27-72-f0-9b-ff-dd                         |
  |                                                                    |
  |         header[0]  b2 d9 b1 29 68 62 27 72 f0 9b ff dd             |
  |                                                                    |
  |--------------------------------------------------------------------|
  |                        pkt_eth_mac_data_unit                       |
  |                                                                    |
  |             eth_type ->  II_ETYPE_IPV4                             |
  |                                                                    |
  |         header[0]  08 00                                           |
  |                                                                    |
  |--------------------------------------------------------------------|
  |                              pkt_ipv4                              |
  |                                                                    |
  |           ip_version ->  4                                         |
  |                ip_da ->  98.247.232.195                            |
  |                ip_sa ->  163.87.116.160                            |
  |        header_length ->  0xc (48 bytes)                            |
  |                  tos ->  0xbb                                      |
  |         total_length ->  135 bytes                                 |
  |                   id ->  0x671b                                    |
  |                   df ->  0                                         |
  |                   mf ->  1                                         |
  |      fragment_offset ->  0x0143                                    |
  |                  ttl ->  0x0f                                      |
  |             protocol ->  II_IP_PROTO_UDP                           |
  |             checksum ->  0x0000                                    |
  |              options ->  [d0 72 dd..b fd bc c1 a0 55 91 c2 21 65]  |
  |                                                                    |
  |         header[0]  4c bb 00 87 67 1b 21 43 0f 11 00 00 a3 57 74 a0 |
  |        header[16]  62 f7 e8 c3 d0 72 dd 34 43 e9 02 fe ec 1c 85 ea |
  |        header[32]  d2 02 28 cb 04 ce 5b fd bc c1 a0 55 91 c2 21 65 |
  |                                                                    |
  |--------------------------------------------------------------------|
  |                               pkt_udp                              |
  |                                                                    |
  |             src_port ->  27420                                     |
  |            dest_port ->  12638                                     |
  |               length ->  87                                        |
  |             checksum ->  0x693b                                    |
  |                                                                    |
  |         header[0]  6b 1c 31 5e 00 57 69 3b                         |
  |                                                                    |
  |--------------------------------------------------------------------|
  |                     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 |
  |                                                                    |
  |        payload[0]  be 98 d7 a2 67 b5 7c c3 4d 34 90 d4 17 88 e6 76 |
  |       payload[16]  2c d5 11 49 dc 05 fa 96 8b 1e 3d 55 70 23 cc fc |
  |       payload[32]  b0 5c 56 0c 4f 6a b3 3d e1 64 e2 6a b7 88 9f 26 |
  |       payload[48]  5b cf 4f d3 f9 a3 1f 9e 27 0e 7c 7c a4 28 ec 09 |
  |       payload[64]  d0 c3 60 1e 12 81 00 1e b5 8a af 17 ee 75 72    |
  |                                                                    |
  |--------------------------------------------------------------------|
  |                          pkt_eth_mac_frame                         |
  |                                                                    |
  |              padding ->  []                                        |
  |                  crc ->  0x62382fb2                                |
  |                                                                    |
  |           tail[0]  62 38 2f b2                                     |
  |                                                                    |
  |--------------------------------------------------------------------|
"""

log_pkt_2 = """
  |--------------------------------------------------------------------|
  |                        <sw_eMAC-tx-pkt:0006>                       |
  |                                                                    |
  |        length: 172 bytes   start: 86.77us   end: 88.15us           |
  |--------------------------------------------------------------------|
  |                             eth_packet                             |
  |                                                                    |
  |             preamble ->  [55 55 55 55 55 55 55]                    |
  |                  sfd ->  0xd5                                      |
  |                                                                    |
  |         header[0]  55 55 55 55 55 55 55 d5                         |
  |                                                                    |
  |--------------------------------------------------------------------|
  |                          pkt_eth_mac_frame                         |
  |                                                                    |
  |                   da ->  90-35-6b-a0-cd-79                         |
  |                   sa ->  cc-cd-ef-a5-d3-ee                         |
  |                                                                    |
  |         header[0]  90 35 6b a0 cd 79 cc cd ef a5 d3 ee             |
  |                                                                    |
  |--------------------------------------------------------------------|
  |                        pkt_eth_mac_data_unit                       |
  |                                                                    |
  |             eth_type ->  II_ETYPE_IPV6                             |
  |                                                                    |
  |         header[0]  86 dd                                           |
  |                                                                    |
  |--------------------------------------------------------------------|
  |                              pkt_ipv6                              |
  |                                                                    |
  |           ip_version ->  6                                         |
  |                ip_da ->  ea4c:d71c:a821:d4b1:473f:b3aa:99fc:16bc   |
  |                ip_sa ->  528:b0df:d65:6f9d:7b97:346e:6ab7:eb45     |
  |                  tos ->  0x9e                                      |
  |           flow_label ->  0xd04f9                                   |
  |       payload_length ->  106 bytes                                 |
  |          next_header ->  II_IP_PROTO_TCP                           |
  |                  ttl ->  0x62                                      |
  |                                                                    |
  |         header[0]  69 ed 04 f9 00 6a 06 62 05 28 b0 df 0d 65 6f 9d |
  |        header[16]  7b 97 34 6e 6a b7 eb 45 ea 4c d7 1c a8 21 d4 b1 |
  |        header[32]  47 3f b3 aa 99 fc 16 bc                         |
  |                                                                    |
  |--------------------------------------------------------------------|
  |                               pkt_tcp                              |
  |                                                                    |
  |             src_port ->  30333                                     |
  |            dest_port ->  39914                                     |
  |               seq_no ->  2039154261                                |
  |               ack_no ->  3400346573                                |
  |               offset ->  12                                        |
  |                 rsvd ->  0x00                                      |
  |                  urg ->  1                                         |
  |                  ack ->  1                                         |
  |                  psh ->  1                                         |
  |                  rst ->  0                                         |
  |                  syn ->  0                                         |
  |                  fin ->  1                                         |
  |               window ->  200                                       |
  |             checksum ->  0xc82b                                    |
  |           urgent_ptr ->  39816                                     |
  |              options ->  [3d de de..9 06 26 d7 6f 91 ea 1f 62 92]  |
  |                                                                    |
  |         header[0]  76 7d 9b ea 79 8b 06 55 ca ad 2b cd c0 39 00 c8 |
  |        header[16]  c8 2b 9b 88 3d de de 0a f9 a4 9b 82 33 14 ee 9e |
  |        header[32]  1e 04 22 30 39 14 c9 06 26 d7 6f 91 ea 1f 62 92 |
  |                                                                    |
  |--------------------------------------------------------------------|
  |                     0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 |
  |                                                                    |
  |        payload[0]  53 81 2e 35 cb f8 92 ee a0 20 14 21 69 d1 16 97 |
  |       payload[16]  7a 46 06 d3 7f 07 1e 83 4c 4b ff 10 7d 59 f8 47 |
  |       payload[32]  e5 7b 35 bf 93 2c 6e 1d ac 83 1b 5b 01 30 75 17 |
  |       payload[48]  b5 4c 85 58 c7 97 1d 03 c8 25                   |
  |                                                                    |
  |--------------------------------------------------------------------|
  |                          pkt_eth_mac_frame                         |
  |                                                                    |
  |              padding ->  []                                        |
  |                  crc ->  0xf6666364                                |
  |                                                                    |
  |           tail[0]  f6 66 63 64                                     |
  |                                                                    |
  |--------------------------------------------------------------------|
"""
