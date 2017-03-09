# Packet Modifier

import socket
from scapy.all import *
from scapy.contrib.rsvp import *
from src.data.ReservationRequest import *

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


def get_reservation_info(pkt):
    data = IP(pkt)
    adspec_layer = get_layer(data, Const.CL_ADSPEC)
    adspec_data = adspec_layer.getfieldval('Data')
    qos_class = adspec_data[0]
    if int(qos_class) != 2:
        print 'Wrong service required (not Guarantee Service)'
    qos_value = adspec_data[2]

    session_layer = get_layer(data, Const.CL_SESSION)
    session_data = session_layer.getfieldval('Data')
    dst_ip = session_data[0:15]

    hop_layer = get_layer(data, Const.CL_HOP)
    inface = hop_layer.getfieldval('inface')

    res_req = ReservationRequest(dst_ip, qos_value, inface)
    return res_req


def catch_packet():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RSVP)
    print "Socket created"
    try:
        while 1:
            print "Waiting..."
            pkt = sock.recv(2048)
            print "Received..."
#            modify_packet(pkt)
            get_reservation_info(pkt)

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

