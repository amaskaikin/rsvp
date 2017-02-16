# Modifier of packets

import os
from scapy.contrib.rsvp import *
from Const import *
import socket


def modify_and_accept(pkt):
    data = IP(pkt.get_payload())

    # data.getlayer(1).fields.get('TTL')
    data.getlayer(1).setfieldval('TTL', 10)
    # Set ttl
    data.ttl = 10
    data.chksum = 0x639d
    data.show()
    pkt.set_payload(str(data))
    pkt.accept()


def run_queue():
    # os.system('iptables -I ' + Const.IPTABLES_MODE + ' -d ' + Const.TARGET_ADDRESS +
    #           ' -j NFQUEUE --queue-num ' + str(Const.QUEUE_NUM))
    # q = NetfilterQueue()
    # q.bind(Const.QUEUE_NUM, modify_and_accept)
    # try:
    #     q.run()
    # except KeyboardInterrupt:
    #     q.unbind()
    #     os.system('iptables -F')
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RSVP)
    print "Socket created"
    try:
        while 1:
            print "Waiting..."
            packet = sock.recv(2048)
            print "Received..."
            print IP(packet).getlayer(1).show2()
    except KeyboardInterrupt:
        print "The loop was interrupted via Ctrl^C. Sniffer exiting"
