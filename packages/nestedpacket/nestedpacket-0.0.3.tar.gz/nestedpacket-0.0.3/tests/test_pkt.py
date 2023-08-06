import pytest
from nestedpacket import NestedPacket
from nestedpacket.ethernet import EthPacket, EthMacFrame

@pytest.fixture()
def preamble_byte_list():
    return [0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0xD5,
            0x01, 0x02, 0x03, 0x04, 0x05, 0x06,
            0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C,
            0x0D, 0x0E,
            0x0F, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16,
            0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x18, 0x19,
            0x1A, 0x1B, 0x1C, 0x1D]

@pytest.fixture()
def full_eth_frame(preamble_byte_list):
    eth_pkt = EthPacket()
    eth_pkt.unpack(preamble_byte_list)
    return eth_pkt

@pytest.fixture()
def incrementing_byte_list():
    return list(range(1, 0x1D))

@pytest.fixture()
def mac_eth_frame(incrementing_byte_list):
    eth_pkt = EthMacFrame()
    eth_pkt.unpack(incrementing_byte_list)
    return eth_pkt


def test_preamble():
    """at least the first 3 bytes of the preamble are 0x55"""
    eth_pkt = EthPacket()
    for n, byte in enumerate(eth_pkt.pack()):
        if n < 4:
            assert byte == 0x55

def test_eth_src_addr():
    """the 9th packed byte is the 3rd byte of src_addr"""
    mac_frame = EthMacFrame()
    mac_frame.randomize()
    packed_bytes = mac_frame.pack()
    assert packed_bytes[9] == (mac_frame.src_addr >> 16) & 0xFF

def test_eth_preamble_unpack_src_addr(preamble_byte_list):
    eth_pkt = EthPacket()
    eth_pkt.unpack(preamble_byte_list)
    assert eth_pkt.nested_packet.src_addr == 0x0708_090A_0B0C

def test_eth_preamble_unpack_fcs(preamble_byte_list):
    eth_pkt = EthPacket()
    eth_pkt.unpack(preamble_byte_list)
    assert eth_pkt.nested_packet.fcs == 0x1A1B1C1D

def test_eth_frame_unpack_src_addr(incrementing_byte_list):
    eth_frame = EthMacFrame()
    eth_frame.unpack(incrementing_byte_list)
    assert eth_frame.src_addr == 0x0708_090A_0B0C

def test_2_iterators_independent(incrementing_byte_list):
    eth_frame = EthMacFrame()
    eth_frame.unpack(incrementing_byte_list)
    iter_a = iter(eth_frame)
    iter_b = iter(eth_frame)
    for _ in range(len(eth_frame)):
        assert next(iter_a) == next(iter_b)

def test_check_5th_byte(incrementing_byte_list):
    eth_frame = EthMacFrame()
    eth_frame.unpack(incrementing_byte_list)
    assert eth_frame[4] == 0x5

def test_check_last_byte(full_eth_frame):
    assert full_eth_frame[-1] == 0x1D

def test_check_slice(mac_eth_frame):
    assert mac_eth_frame[5:12:2] == [6,8,10,12]

def test_raise_index_error(mac_eth_frame):
    err_msg_regex = "index out of range"
    with pytest.raises(IndexError, match=err_msg_regex):
        mac_eth_frame[0x1E]

