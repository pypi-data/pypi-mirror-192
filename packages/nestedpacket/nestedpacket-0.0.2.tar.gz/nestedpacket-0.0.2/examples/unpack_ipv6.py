#!/usr/bin/env python3

import nestedpacket


eth_pkt = nestedpacket.EthPreamble()
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
