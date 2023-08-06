#!/usr/bin/env python3

import nestedpacket

pkt_1_byte_str = """
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
"""
pkt_1_bytes = [int(x, base=16) for x in pkt_1_byte_str.split()]

eth_pkt = nestedpacket.EthPreamble()
eth_pkt.unpack(pkt_1_bytes)

printer = nestedpacket.TextBoxPrinter(25, 35)
print(printer.sprint(eth_pkt))

if eth_pkt.nested_packet.check_fcs():
    print("FCS check PASS")
else:
    print("FCS check FAIL")

eth_pkt.set_field_value("tos", 0xaa)
if eth_pkt.nested_packet.check_fcs():
    print("after tos change: FCS check PASS")
else:
    print("after tos change: FCS check FAIL")


eth_pkt.nested_packet.update_fcs()
print(printer.sprint(eth_pkt))

print(f'ttl: { eth_pkt.get_field_value("ttl") }')
print(f'ip_da: { eth_pkt.get_field_value("ip_da") }')
