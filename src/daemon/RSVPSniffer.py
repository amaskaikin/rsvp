# Packet Modifier

import socket
from scapy.all import *
from scapy.contrib.rsvp import *

from src.utils.Const import *


def modify_packet(pkt):
    data = IP(pkt)
    data.getlayer('RSVP').setfieldval('TTL', 10)
    data.getlayer('HOP').setfieldval('inface', 2)
    data.getlayer('IP').setfieldval('dst', Const.TARGET_ADDRESS)
    data.show2()
    layer = get_layer(data, Const.CL_SENDER)
    print layer.getfieldval('Tokens')[1:3]
    send(data)


def catch_packet():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RSVP)
    print "Socket created"
    try:
        while 1:
            print "Waiting..."
            pkt = sock.recv(2048)
            print "Received..."
            modify_packet(pkt)

    except KeyboardInterrupt:
        print "The loop was interrupted. Sniffer exiting"


def get_layer(data, pclass):
    cnt = 0
    while True:
        layer = data.getlayer(cnt)
        if layer is not None:
            if layer.name == 'RSVP_Object':
                if layer.getfieldval('Class') == pclass:
                    return data.getlayer(++cnt)
        else:
            break
        cnt += 1

