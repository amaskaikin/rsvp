# Modifier of packets

import os
from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP
from Const import *


def print_and_accept(pkt):
    data = IP(pkt.get_payload())
    # Set ttl
    data.ttl = 10
    pkt.set_payload(str(data))
    pkt.accept()


def run_queue():
    os.system('iptables -I INPUT -d ' + Const.TARGET_ADDRESS +
              ' -j NFQUEUE --queue-num ' + str(Const.QUEUE_NUM))
    q = NetfilterQueue()
    q.bind(Const.QUEUE_NUM, print_and_accept)
    try:
        q.run()
    except KeyboardInterrupt:
        q.unbind()
        os.system('iptables -F')
