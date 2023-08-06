"""Headers for IPv4, IPv6 and TCP packets"""

import random
import bitstring

from .nestedpacket import NestedPacket
from .nestedpacket import UnpackResult
from .udpdatagram import UdpDatagram

def ipaddr2str(ipaddr):
    return (f'{ (ipaddr>>24)&0xFF }.{ (ipaddr>>16)&0xFF }.' +
            f'{ (ipaddr>>8)&0xFF }.{ ipaddr & 0xFF }')

class Ipv4Packet(NestedPacket):
    """IPv4 Header"""
    IPV_FLD_VAL = 4

    def __init__(self):
        super().__init__()
        self.ip_version = self.IPV_FLD_VAL
        self.header_length = 0
        self.tos = 0
        self.total_length = 0
        self.id = 0
        self.df = 0
        self.mf = 0
        self.fragment_offset = 0
        self.ttl = 0
        self.protocol = 0
        self.checksum = 0
        self.ip_sa = 0
        self.ip_da = 0
        self.options = []

        self.add_header_field('ip_version',      start_bit=0, last_bit=3)
        self.add_header_field('header_length',   start_bit=4, last_bit=7)
        self.add_header_field('tos',             start_bit=8, last_bit=15)
        self.add_header_field('total_length',    start_bit=16, last_bit=31)
        self.add_header_field('id',              start_bit=32, last_bit=47)
        # reserved bit
        self.add_header_field('df',              start_bit=49, last_bit=49)
        self.add_header_field('mf',              start_bit=50, last_bit=50)
        self.add_header_field('fragment_offset', start_bit=51, last_bit=63)
        self.add_header_field('ttl',             start_bit=64, last_bit=71)
        self.add_header_field('protocol',        start_bit=72, last_bit=79)
        self.add_header_field('checksum',        start_bit=80, last_bit=95)
        self.add_header_field('ip_sa',           start_bit=96, last_bit=127)
        self.add_header_field('ip_da',           start_bit=128, last_bit=159)
        self.add_header_field('options',         constant_width=False)

        self.set_trans_type_name("IPv4-Packet")

    def create_nested_packet(self):
        match (self.protocol):
            case 0x06: return TcpPacket()
            case 0x11: return UdpDatagram()
            case   _ : return super().create_nested_packet()

    def do_randomize(self):
        self.header_length   = random.randint(5,15)  # 32-bit words
        self.tos             = random.randint(0,0xFF)
        self.id              = random.randint(0,0xFFFF)
        self.df              = random.randint(0,1)
        self.mf              = random.randint(0,1)
        self.fragment_offset = random.randint(0,0x1FFF)
        self.ttl             = random.randint(0,0xFF)
        self.ip_sa           = random.randint(0,0xFFFF_FFFF)
        self.ip_da           = random.randint(0,0xFFFF_FFFF)
        self.options = [random.randint(0,0xFF) for _
                        in range((self.header_length * 4) - 20)]
        self.protocol        = random.choice([0x06,
                                              0x11,
                                              random.randint(0,0xFF)])


    def options_byte_length(self):
        return (self.header_length * 4) - 20

    def pack_header(self):
        header_bytes = NestedPacket.pack_header(self)
        return header_bytes + self.options

    def unpack_header(self, list_of_bytes):
        unpack_result, remaining_bytes = NestedPacket.unpack_header(self, list_of_bytes)
        if unpack_result == UnpackResult.FAIL:
            return UnpackResult.FAIL, remaining_bytes
        if self.options_byte_length() > len(remaining_bytes):
            return UnpackResult.FAIL, remaining_bytes
        self.options = []
        for _ in range(self.options_byte_length()):
            self.options.append(remaining_bytes.pop(0))
        return UnpackResult.SUCCESS, remaining_bytes

    def get_field_value_str(self, field_name):
        if field_name == 'ip_sa':
            return ipaddr2str(self.ip_sa)
        elif field_name == 'ip_da':
            return ipaddr2str(self.ip_da)
        elif field_name == 'options':
            return '[' + ' '.join([f'{x:02x}' for x in self.options]) + ']'
        else:
            return super().get_field_value_str(field_name)


class Ipv6Packet(NestedPacket):
    """IPv6 Header"""
    IPV_FLD_VAL = 6

    def __init__(self):
        super().__init__()
        self.ip_version = self.IPV_FLD_VAL
        self.tos = 0
        self.flow_label = 0
        self.payload_length = 0
        self.next_header = 0
        self.ttl = 0
        self.ip_sa = 0
        self.ip_da = 0

        self.add_header_field('ip_version',      start_bit=0,   last_bit=3)
        self.add_header_field('tos',             start_bit=4,   last_bit=11)
        self.add_header_field('flow_label',      start_bit=12,  last_bit=31)
        self.add_header_field('payload_length',  start_bit=32,  last_bit=47)
        self.add_header_field('next_header',     start_bit=48,  last_bit=55)
        self.add_header_field('ttl',             start_bit=56,  last_bit=63)
        self.add_header_field('ip_sa',           start_bit=64,  last_bit=191)
        self.add_header_field('ip_da',           start_bit=192, last_bit=319)

        self.set_trans_type_name("IPv6-Packet")

    def do_randomize(self):
        self.tos             = random.randint(0,0xFF)
        self.flow_label      = random.randint(0,0xFFFFF)
        self.ttl             = random.randint(0,0xFF)
        self.ip_sa           = random.randint(0,0xFFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF)
        self.ip_da           = random.randint(0,0xFFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF_FFFF)
        self.next_header     = random.choice([0x06,
                                              0x11,
                                              random.randint(0,0xFF)])
    def create_nested_packet(self):
        match (self.next_header):
            case 0x06: return TcpPacket()
            case 0x11: return UdpDatagram()
            case   _ : return super().create_nested_packet()



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


            
class TcpPacket(NestedPacket):
    """TCP Header"""

    def __init__(self):
        super().__init__()
        self.src_port = 0
        self.dest_port = 0
        self.seq_no = 0
        self.ack_no = 0
        self.offset = 0
        self.urg = 0
        self.ack = 0
        self.psh = 0
        self.rst = 0
        self.syn = 0
        self.fin = 0
        self.window = 0
        self.checksum = 0
        self.urgent_ptr = 0
        self.options = []

        self.add_header_field('src_port',    start_bit=0,  last_bit=15)
        self.add_header_field('dest_port',   start_bit=16, last_bit=31)
        self.add_header_field('seq_no',      start_bit=32, last_bit=63)
        self.add_header_field('ack_no',      start_bit=64, last_bit=95)
        self.add_header_field('offset',      start_bit=96, last_bit=99)
        # reserved 6 bits
        self.add_header_field('urg',         start_bit=106, last_bit=106)
        self.add_header_field('ack',         start_bit=107, last_bit=107)
        self.add_header_field('psh',         start_bit=108, last_bit=108)
        self.add_header_field('rst',         start_bit=109, last_bit=109)
        self.add_header_field('syn',         start_bit=110, last_bit=110)
        self.add_header_field('fin',         start_bit=111, last_bit=111)
        self.add_header_field('window',      start_bit=112, last_bit=127)
        self.add_header_field('checksum',    start_bit=128, last_bit=143)
        self.add_header_field('urgent_ptr',  start_bit=144, last_bit=159)
        self.add_header_field('options',     constant_width=False)

        self.set_trans_type_name("TCP-Packet")


    def do_randomize(self):
        self.src_port   = random.randint(0,0xFFFF)
        self.dest_port  = random.randint(0,0xFFFF)
        self.seq_no     = random.randint(0,0xFFFF_FFFF)
        self.ack_no     = random.randint(0,0xFFFF_FFFF)
        self.offset     = random.randint(5,15) # size of header in 32-bit words
        self.urg        = random.randint(0,1)
        self.ack        = random.randint(0,1)
        self.psh        = random.randint(0,1)
        self.rst        = random.randint(0,1)
        self.syn        = random.randint(0,1)
        self.fin        = random.randint(0,1)
        self.window     = random.randint(0,0xFFFF)
        self.checksum   = random.randint(0,0xFFFF)
        self.urgent_ptr = random.randint(0,0xFFFF)

        self.options = [random.randint(0,0xFF) for _
                        in range(self.options_byte_length())]

    def do_harmonize(self):
        self.update_checksum()
        
    def options_byte_length(self):
        return (self.offset * 4) - 20

    def pack_header(self):
        header_bytes = NestedPacket.pack_header(self)
        return header_bytes + self.options

    def unpack_header(self, list_of_bytes):
        unpack_result, remaining_bytes = NestedPacket.unpack_header(self, list_of_bytes)
        if unpack_result == UnpackResult.FAIL:
            return UnpackResult.FAIL, remaining_bytes
        if self.options_byte_length() > len(remaining_bytes):
            return UnpackResult.FAIL, remaining_bytes
        self.options = []
        for _ in range(self.options_byte_length()):
            self.options.append(remaining_bytes.pop(0))
        return UnpackResult.SUCCESS, remaining_bytes

    def get_field_value_str(self, field_name):
        if field_name == 'src_port':
            return f'{ self.src_port :d}'
        elif field_name == 'dest_port':
            return f'{ self.dest_port :d}'
        elif field_name == 'options':
            return '[' + ' '.join([f'{x:02x}' for x in self.options]) + ']'
        else:
            return super().get_field_value_str(field_name)

    def calc_checksum(self):
        saved_checksum = self.checksum
        self.checksum = 0
        _bytes = self.pack()
        if isinstance(self.enclosing_packet, Ipv4Packet):
            pseudo_header = build_ivp4_pseudo_header(self.enclosing_packet,
                                                     len(_bytes))
        elif isinstance(self.enclosing_packet, Ipv6Packet):
            pseudo_header = build_ivp6_pseudo_header(self.enclosing_packet,
                                                     len(_bytes))
        else:
            raise Exception('TCP Packet not enclosed in IPv4 or IPv6 packet')
        _bytes = pseudo_header + _bytes
        total = 0
        if len(_bytes) % 2 != 0:
            _bytes.append(0)
        for i in range(0, len(_bytes), 2):
            total += ((_bytes[i] << 8) + _bytes[i+1])
            if total > 0xFFFF:
                total = (total & 0xFFFF) + 1
        total = total & 0xFFFF
        total = total ^ 0xFFFF
        if total == 0:
            total = 0xFFFF
        return total

    def check_checksum(self):
        return (self.checksum == self.calc_checksum())

    def update_checksum(self):
        self.checksum = self.calc_checksum()




def build_ivp4_pseudo_header(pkt, tcp_length):
    '''
        IPv4 TCP pseudo header
      0      7 8     15 16    23 24    31
     +--------+--------+--------+--------+
     |           source address          |
     +--------+--------+--------+--------+
     |         destination address       |
     +--------+--------+--------+--------+
     |  zero  |protocol|    TCP length   |
     +--------+--------+--------+--------+
    '''
    pack_format = ', '.join(['uint:32=src_addr',
                             'uint:32=dest_addr',
                             'pad:8',
                             'uint:8=protocol',
                             'uint:16=length'])
    return [int(x) for x in
            bitstring.pack(pack_format,
                           src_addr=pkt.ip_sa,
                           dest_addr=pkt.ip_da,
                           protocol=pkt.protocol,
                           length=tcp_length).tobytes()]

def build_ivp6_pseudo_header(pkt, tcp_length):
    ''' IPv6 TCP pseudo header
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    +                                                               +
    |                                                               |
    +                         Source Address                        +
    |                                                               |
    +                                                               +
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                                                               |
    +                                                               +
    |                                                               |
    +                      Destination Address                      +
    |                                                               |
    +                                                               +
    |                                                               |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                   Upper-Layer Packet Length                   |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                      zero                     |  Next Header  |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    '''
    pack_format = ', '.join(['uint:128=src_addr',
                             'uint:128=dest_addr',
                             'uint:32=length',
                             'pad:24',
                             'uint:8=protocol'])
    return [int(x) for x in
            bitstring.pack(pack_format,
                           src_addr=pkt.ip_sa,
                           dest_addr=pkt.ip_da,
                           length=tcp_length,
                           protocol=pkt.next_header).tobytes()]
