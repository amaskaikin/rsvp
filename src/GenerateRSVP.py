# Generate RSVP data

from scapy.contrib.rsvp import *
from scapy.layers.inet import IP
from scapy.all import *
from Const import *
from RSVP_Path import *
from ProcessRSVPMsg import *


def generate_data(dst):
    # Create test RSVP packet
    rsvp_pkt = dict(header=PathRSVP.HEADER, session=PathRSVP.SESSION, hop=PathRSVP.HOP, time=PathRSVP.TIME,
                    sender_tspec=PathRSVP.SENDER_TSPEC)
    pkt = IP(dst=dst)/generate_path_msg(**rsvp_pkt)
    # pkt = IP(dst=dst) / RSVP(TTL=65, Class=0x01) / RSVP_Object(Class=0x03) / RSVP_HOP(neighbor='192.168.0.107')
    pkt.show2()
    while True:
        send(pkt)
        time.sleep(1)


if __name__ == '__main__':
    try:
        generate_data(Const.TARGET_ADDRESS)
    except KeyboardInterrupt:
        pass
