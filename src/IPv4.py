# Class for IPv4 packet
# Function 'unpack(packet)' returns parsed IPv4 packet

import struct
import socket


class IPv4:
    def __init__(self, packet):
        self.version, self.ihl, self.ttl, self.proto, self.src, self.dst = unpack(packet)


def unpack(packet):
    iph = struct.unpack('!BBHHHBBH4s4s', packet[:20])
    return iph[0] >> 4, iph[0] & 0xF, iph[5], iph[6], socket.inet_ntoa(iph[8]), socket.inet_ntoa(iph[9])
