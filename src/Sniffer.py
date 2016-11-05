# Packet sniffer

# import socket
import sys
from Ethernet import *
from IPv4 import *


def create_socket(device):
    try:
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
        s.bind((device, 0))
        return s
    except socket.error, msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + '; Message: ' + msg[1]
        sys.exit()


def sniff(s):
    eth = Ethernet((s.recvfrom(65565))[0])
    if eth.proto == 8:
        ipv4 = IPv4(eth.data)
        if ipv4.proto == 1:
            return 'ICMP'
        elif ipv4.proto == 6:
            return 'TCP'
        elif ipv4.proto == 17:
            return 'UDP'
        else:
            return 'Other IPv4 protocol'
