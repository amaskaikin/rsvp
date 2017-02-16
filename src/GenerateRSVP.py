# Generate RSVP data

from scapy.contrib.rsvp import *
from scapy.layers.inet import IP
from scapy.all import *
from Const import *


def generate_data(dst):
    # Create test RSVP packet
    data = IP(dst=dst)/RSVP(TTL=65, Class=0x01)/RSVP_Object(Class=0x03)/RSVP_HOP(neighbor='192.168.0.107')
    data.show2()
    while True:
        send(data)
        time.sleep(1)


if __name__ == '__main__':
    try:
        generate_data(Const.TARGET_ADDRESS)
    except KeyboardInterrupt:
        pass
