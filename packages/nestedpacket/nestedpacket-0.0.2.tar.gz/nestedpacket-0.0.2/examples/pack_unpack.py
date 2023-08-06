#!/usr/bin/env python3

import nestedpacket

eth_pkt = nestedpacket.EthPreamble()
eth_pkt.randomize()

printer = nestedpacket.TextBoxPrinter(25, 35)
print(printer.sprint(eth_pkt))

byte_list = eth_pkt.pack()
eth_pkt2 = nestedpacket.EthPreamble()
eth_pkt2.unpack(byte_list)

print(printer.sprint(eth_pkt2))

