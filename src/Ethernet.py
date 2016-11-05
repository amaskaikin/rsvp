# Class for Ethernet packet
# Function 'unpack(packet)' returns parsed Ethernet packet

import struct
import socket


class Ethernet:
    def __init__(self, packet):
        self.dst, self.src, self.proto, self.data = unpack(packet)


def unpack(packet):
    eth = struct.unpack('!6s6sH', packet[:14])
    return eth_addr(eth[0]), eth_addr(eth[1]), socket.htons(eth[2]), packet[14:]


def eth_addr(a):
    b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]), ord(a[1]), ord(a[2]), ord(a[3]), ord(a[4]), ord(a[5]))
    return b



