#!/usr/bin/env python3

from nestedpacket.ethernet import EthPacket
from nestedpacket import TextBoxPrinter

eth_pkt = EthPacket()
eth_pkt.randomize()  # generate meaningful random field values
eth_pkt.harmonize()  # update dependent fields
byte_list = eth_pkt.pack()

print(byte_list)

eth_pkt_2 = EthPacket()
eth_pkt_2.unpack(byte_list)

printer = TextBoxPrinter(25, 35)
print(printer.sprint(eth_pkt_2))

