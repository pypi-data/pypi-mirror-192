"""nestedpacket package"""

import random
from collections import Counter
import bitstring
from bitstring import Bits, ConstBitStream
from operator import itemgetter
from enum import Enum

class UnpackResult(Enum):
    FAIL = 0
    SUCCESS = 1

def generate_pack_format(start_bit_table, field_width_table):
    formats = []
    fields = [key for key, val in sorted(start_bit_table.items(),
                                         key=itemgetter(1))]
    next_bit = 0
    for field in fields:
        start_bit = start_bit_table[field]
        width = field_width_table[field]
        if start_bit > next_bit:
            formats.append(f'pad:{ start_bit - next_bit }')
        formats.append(f'uint:{ width }={ field }')
        next_bit = start_bit + width
    return ', '.join(formats)


class TbTransaction:
    """A testbench transaction base class"""

    _id_counter = Counter()

    def __init__(self):
        self.transmit_begin_time = 0
        self.transmit_end_time = 0
        TbTransaction._id_counter[self.__class__.__name__] += 1
        self._trans_id_num = TbTransaction._id_counter[self.__class__.__name__]
        self.set_trans_type_name(self.__class__.__name__)

    def set_trans_type_name(self, type_name):
        self._trans_type_name = type_name

    def trans_id(self):
        """provide a unique id string for this transaction"""
        return f'{self._trans_type_name}-{self._trans_id_num:04d}'


class NestedPacket(TbTransaction):
    """A framework for composing layered frames/packets/datagrams"""

    def __init__(self):
        super().__init__()
        self._nested_packet = None
        self._enclosing_packet = None
        self._header_fields = []
        self._header_bit_table = {}
        self._header_start_bits = {}
        self._header_field_widths = {}
        self._header_format = ''
        self._trailer_fields = []
        self._trailer_bit_table = {}
        self._trailer_start_bits = {}
        self._trailer_field_widths = {}
        self._trailer_format = ''

    def add_header_field(self, var, start_bit=-1, last_bit=-1, constant_width=True):
        try:
            getattr(self, var)
        except:
            raise Exception(f"Class member '{ var }' not found.")
        self._header_fields.append(var)
        if constant_width:
            for n in range(start_bit, last_bit+1):
                if n in self._header_bit_table:
                    raise Exception(
                        f"adding header field '{ var }', but it " +
                        f"overlaps with '{ self._header_bit_table[n] }' field ")
                self._header_bit_table[n] = var
            self._header_start_bits[var] = start_bit
            self._header_field_widths[var] = (last_bit - start_bit) + 1
            self._header_format = generate_pack_format(
                self._header_start_bits, self._header_field_widths)

    def add_trailer_field(self, var, start_bit=-1, last_bit=-1, constant_width=True):
        try:
            getattr(self, var)
        except:
            raise Exception(f"Class member '{ var }' not found.")
        self._trailer_fields.append(var)
        if constant_width:
            for n in range(start_bit, last_bit+1):
                if n in self._trailer_bit_table:
                    raise Exception(
                        f"adding trailer field '{ var }', but it " +
                        f"overlaps with '{ self._trailer_bit_table[n] }' field ")
                self._trailer_bit_table[n] = var
            self._trailer_start_bits[var] = start_bit
            self._trailer_field_widths[var] = (last_bit - start_bit) + 1
            self._trailer_format = generate_pack_format(
                self._trailer_start_bits, self._trailer_field_widths)

    def fixed_width_header_fields(self):
        for fld_name in self._header_fields:
            if fld_name in self._header_start_bits:
                yield fld_name

    def fixed_width_trailer_fields(self):
        for fld_name in self._trailer_fields:
            if fld_name in self._trailer_start_bits:
                yield fld_name

    @property
    def nested_packet(self):
        '''attempts to create a nested_packet if one has not
           already been set'''
        if self._nested_packet is None:
            self._nested_packet = self.create_nested_packet()
            if self._nested_packet is not None:
                self._nested_packet._enclosing_packet = self
        return self._nested_packet

    @nested_packet.setter
    def nested_packet(self, obj):
        '''add a nested packet'''
        self._nested_packet = obj
        if self._nested_packet is not None:
            self._nested_packet._enclosing_packet = self

    def get_nested_packet(self, classinfo=None):
        if classinfo is None:
            return self.nested_packet
        elif self.nested_packet is None:
            return None
        elif isinstance(self.nested_packet, classinfo):
            return self.nested_packet
        else:
            return self.nested_packet.get_nested_packet(classinfo)

    @property
    def enclosing_packet(self):
        return self._enclosing_packet

    def create_nested_packet(self):
        return InnerMostPayload()

    def get_header_field_list(self):
        return self._header_fields

    def get_trailer_field_list(self):
        return self._trailer_fields

    def get_field_value(self, field_name):
        try:
            return getattr(self, field_name)
        except AttributeError:
            if self.nested_packet is not None:
                return self.nested_packet.get_field_value(field_name)
            else:
                raise Exception('field not found: '+ field_name)

    def set_field_value(self, field_name, value):
        if hasattr(self, field_name):
            setattr(self, field_name, value)
        elif self.nested_packet is not None:
            self.nested_packet.set_field_value(field_name, value)
        else:
            raise Exception('field not found: '+ field_name)

    def get_field_value_str(self, field_name):
        return f'{int(getattr(self, field_name)):#x}'

    def pack(self):
        if self.nested_packet is not None:
            return (self.pack_header()
                    + self.nested_packet.pack()
                    + self.pack_trailer())
        else:
            return (self.pack_header()
                    + self.pack_trailer())

    def pack_header(self):
        if self._header_format == '':
            return []
        field_table = {field: int(getattr(self, field))
                       for field in self.fixed_width_header_fields()}
        return [int(x) for x in
                bitstring.pack(self._header_format, **field_table).tobytes()]

    def pack_trailer(self):
        if self._trailer_format == '':
            return []
        field_table = {field: int(getattr(self, field))
                       for field in self.fixed_width_trailer_fields()}
        return [int(x) for x in
                bitstring.pack(self._trailer_format, **field_table).tobytes()]

    def pack_payload(self):
        """This method is only called if the nested_packet is None"""
        return []

    def unpack(self, list_of_bytes):
        match self.unpack_header(list_of_bytes):
            case (UnpackResult.FAIL, _) :
                return UnpackResult.FAIL
            case (UnpackResult.SUCCESS, unused_bytes):
                remaining_bytes = unused_bytes

        match self.unpack_trailer(remaining_bytes):
            case (UnpackResult.FAIL, _) :
                return UnpackResult.FAIL
            case (UnpackResult.SUCCESS, unused_bytes):
                remaining_bytes = unused_bytes
        return self.unpack_payload(remaining_bytes)

    def unpack_header(self, list_of_bytes):
        if self._header_format == '':
            return UnpackResult.SUCCESS, list_of_bytes
        unpack_vals = ConstBitStream(
                           bytearray(list_of_bytes)).unpack(
                               self._header_format + ', bits')
        remaining_bs = unpack_vals.pop()
        for field_name, field_val in zip(self._header_fields,
                                         unpack_vals):
            setattr(self, field_name, field_val)
        return UnpackResult.SUCCESS, [int(x) for x in remaining_bs.tobytes()]

    def unpack_trailer(self, list_of_bytes):
        if self._trailer_format == '':
            return UnpackResult.SUCCESS, list_of_bytes
        unpack_vals = ConstBitStream(
                           bytearray(list_of_bytes)).unpack(
                               'bits, ' + self._trailer_format)
        remaining_bs = unpack_vals.pop(0)
        for field_name, field_val in zip(self._trailer_fields,
                                         unpack_vals):
            setattr(self, field_name, field_val)
        return UnpackResult.SUCCESS, [int(x) for x in remaining_bs.tobytes()]

    def unpack_payload(self, list_of_bytes):
        if self.nested_packet is not None:
            return self.nested_packet.unpack(list_of_bytes)
        elif len(list_of_bytes) == 0:
            return UnpackResult.SUCCESS
        else:
            return UnpackResult.FAIL

    def randomize(self):
        self.do_randomize()
        self.nested_packet = self.create_nested_packet()
        if self.nested_packet is not None:
            self.nested_packet.randomize()

    def do_randomize(self):
        pass

    def harmonize(self):
        if self.nested_packet is not None:
            self.nested_packet.harmonize()
        self.do_harmonize()

    def do_harmonize(self):
        pass

    def length_in_bytes(self):
        return len(self.pack())

    def bytes_str(self):
        byte_list = self.pack()
        idx = 0
        my_str = ''
        while idx < len(byte_list):
            my_str += f'{byte_list[idx]:#04x} '
            if idx + 8 < len(byte_list):
                my_str += ' '.join([f'{bite:02x}' for bite in byte_list[idx+1:idx+8]])
            elif idx + 1 < len(byte_list):
                my_str += ' '.join([f'{bite:02x}' for bite in byte_list[idx+1:]])
            my_str += '\n'
            idx += 8
        return my_str

    def __len__(self):
        return self.length_in_bytes()

    def __getitem__(self, key):
        byte_list = self.pack()
        return byte_list[key]

    def __iter__(self):
        for _byte in self.pack():
            yield _byte


class InnerMostPayload(NestedPacket):
    """Payload packet is just a list of bytes and terminates nesting"""
    def __init__(self,
                 min_len=48, max_len=1500,
                 payload=None):
        super().__init__()
        self._max_len = max_len;
        self._min_len = min_len;
        if payload is None:
            self._payload = []
        else:
            self._payload = payload

    def create_nested_packet(self):
        return None

    def do_randomize(self):
        self._payload = [random.randint(0,255)
                         for _ in range(
                                 random.randint(
                                     self._min_len,
                                     self._max_len))]

    def pack_payload(self):
        return [int(x) for x in self._payload]

    def unpack_payload(self, list_of_bytes):
        self._payload = list_of_bytes
        list_of_bytes = []
        return UnpackResult.SUCCESS

    def pack(self):
        return self.pack_payload()
