"""Header for UDP Datagrams"""

import random

from .nestedpacket import NestedPacket
from .nestedpacket import UnpackResult


class UdpDatagram(NestedPacket):
    """UDP Header"""

    def __init__(self):
        super().__init__()
        self.src_port = 0
        self.dest_port = 0
        self.length = 0
        self.checksum = 0

        self.add_header_field('src_port',    start_bit=0,  last_bit=15)
        self.add_header_field('dest_port',   start_bit=16, last_bit=31)
        self.add_header_field('length',      start_bit=32, last_bit=47)
        self.add_header_field('checksum',    start_bit=48, last_bit=63)

        self.set_trans_type_name("UDP-Datagram")

    # def create_nested_packet(self):
    #     return EthMacFrame()

    def do_randomize(self):
        self.src_port   = random.randint(0,0xFFFF)
        self.dest_port  = random.randint(0,1)
        self.checksum   = random.randint(0,0x1FFF)

    def get_field_value_str(self, field_name):
        if field_name == 'src_port':
            return f'{ self.src_port :d}'
        elif field_name == 'dest_port':
            return f'{ self.dest_port :d}'
        else:
            return super().get_field_value_str(field_name)
