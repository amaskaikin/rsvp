# Generate RSVP data

from scapy.contrib.rsvp import *
from scapy.layers.inet import IP
from scapy.all import *
from Const import *


def generate_data(dst):
    # Create test RSVP packet
    data = IP(dst=dst)/RSVP(TTL=65)
    while True:
        output = sr(data)
        print(output)
        time.sleep(1)


if __name__ == '__main__':
    try:
        generate_data(Const.TARGET_RSVP_ADDRESS)
    except KeyboardInterrupt:
        pass
