#!/usr/bin/env python3

import nestedpacket

eth_pkt = nestedpacket.ethernet.EthPacket()
eth_pkt.randomize()
print(eth_pkt.bytes_str())

printer = nestedpacket.TextBoxPrinter(25, 35)
print(printer.sprint(eth_pkt))

eth_pkt.randomize()
print(printer.sprint(eth_pkt))


eth_pkt = nestedpacket.ethernet.EthMacFrame()
eth_pkt.randomize()
print(printer.sprint(eth_pkt))

eth_pkt.randomize()
print(printer.sprint(eth_pkt))

