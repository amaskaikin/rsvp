from struct import *


class TCP:
    def __init__(self):
        self.iph = None
        self.tcph = None

    def unpack(self, packet):
        packet = packet[0]
        self.iph = unpack('!BBHHHBBH4s4s', packet[0:20])
        iph_length = (self.iph[0] & 0xF) * 4
        tcp_header = packet[iph_length:iph_length + 20]
        self.tcph = unpack('!HHLLBBHHH', tcp_header)
        return self
