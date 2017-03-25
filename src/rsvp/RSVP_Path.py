from scapy.contrib.rsvp import *


class PathRSVP:
    def __init__(self):
        pass

    HEADER = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x01)}
    SESSION = {'Data': '192.168.0.107'}
    HOP = {'neighbor': '192.168.0.108', 'inface': 3}
    TIME = {'refresh': 4}
    SENDER_TEMPLATE = {'Data': '100192.168.0.109100192.168.0.106'}
    ADSPEC = {'Data': '1081000100'}
