#!/usr/bin/env python3

import nestedpacket

eth_pkt = nestedpacket.EthPreamble()
eth_pkt.randomize()
print(eth_pkt.bytes_str())

printer = nestedpacket.textboxprinter.TextBoxPrinter(25, 35)
print(printer.sprint(eth_pkt))

eth_pkt.randomize()
print(printer.sprint(eth_pkt))


eth_pkt = nestedpacket.EthMacFrame()
eth_pkt.randomize()
print(printer.sprint(eth_pkt))

eth_pkt.randomize()
print(printer.sprint(eth_pkt))

