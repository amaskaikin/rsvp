# Packet Modifier

from src.rsvp.ProcessPathMsg import *
from src.rsvp.ProcessErrMsg import *


def process_packet(pkt):
    data = IP(pkt)
    rsvp_class = data.getlayer('RSVP').getfieldval('Class')
    if rsvp_class == 0x01:
        process_path(data)
    if rsvp_class == 0x02:
        process_resv(data)
    if rsvp_class == 0x05:
        process_path_tear(data)
    if rsvp_class == 0x06:
        process_resv_tear(data)
    if rsvp_class == 0x03:
        process_path_err(data)
    if rsvp_class == 0x04:
        process_resv_err(data)


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

