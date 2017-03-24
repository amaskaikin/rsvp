# Packet Modifier

import socket
from scapy.all import *
from scapy.contrib.rsvp import *
from src.utils.Utils import *
from src.rsvp.ProcessPathMsg import *

from src.utils.Const import *


# method for testing
def modify_packet(pkt):
    data = IP(pkt)
    data.getlayer('RSVP').setfieldval('TTL', 10)
    data.getlayer('HOP').setfieldval('inface', 2)
    data.getlayer('IP').setfieldval('dst', Const.TARGET_ADDRESS)
    data.show2()
    layer = get_layer(data, Const.CL_SENDER)
    print layer.getfieldval('Tokens')[1:3]
    send(data)


def process_packet(pkt):
    data = IP(pkt)
    rsvp_class = data.getlayer('RSVP').getfieldval('Class')
    print rsvp_class
    if rsvp_class == 0x01:
        process_path(data)


def catch_packet():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RSVP)
    print "Socket created"
    try:
        while 1:
            print "Waiting..."
            pkt = sock.recv(2048)
            print "Received..."
#            modify_packet(pkt)
            process_packet(pkt)

    except KeyboardInterrupt:
        print "The loop was interrupted. Sniffer exiting"

