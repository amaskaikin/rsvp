# Packet sniffer in python for Linux
# Sniffs only incoming TCP packet

import socket
import sys
from struct import *
from TCP import *


def create_socket():
    try:
        return socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except socket.error, msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()


def sniff(s):
    tcp = TCP()
    return tcp.unpack(s.recvfrom(65565))

