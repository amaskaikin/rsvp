# Packet Modifier

from scapy.contrib.rsvp import *
from Const import *
from scapy.all import *
import socket


def modify_packet(pkt):
    data = IP(pkt)
    data.getlayer('RSVP').setfieldval('TTL', 10)

    data.getlayer('IP').setfieldval('dst', Const.TARGET_ADDRESS)
    data.show2()
    send(data)


def process_packet():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RSVP)
    print "Socket created"
    try:
        while 1:
            print "Waiting..."
            pkt = sock.recv(2048)
            print "Received..."
            print IP(pkt).show2()
            modify_packet(pkt)

    except KeyboardInterrupt:
        print "The loop was interrupted. Sniffer exiting"
