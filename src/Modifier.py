# Modifier of packets

from netfilterqueue import NetfilterQueue
from scapy.layers.inet import IP
import os


def print_and_accept(pkt):
    data = IP(pkt.get_payload())
    # Set ttl
    data.ttl = 10
    pkt.set_payload(str(data))
    pkt.accept()


def run_queue():
    os.system('iptables -I INPUT -d 192.168.44.53 -j NFQUEUE --queue-num 1')
    q = NetfilterQueue()
    q.bind(1, print_and_accept)
    try:
        q.run()
    except KeyboardInterrupt:
        q.unbind()
        os.system('iptables -F')
