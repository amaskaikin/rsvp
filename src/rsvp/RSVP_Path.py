from scapy.contrib.rsvp import *

SOURCE_ADDRESS = '00192.168.0.109'
DEST_ADDRESS = '00192.168.0.100'
TOS = '08'
RATE = '000100'


class PathRSVP:
    def __init__(self):
        pass

    HEADER = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x01)}
    # SESSION = {'Data': '192.168.0.100'}
    # HOP = {'neighbor': '192.168.0.109', 'inface': 3}
    TIME = {'refresh': 4}
    SENDER_TEMPLATE = {'Data': '1'+SOURCE_ADDRESS+'1'+DEST_ADDRESS}
    ADSPEC = {'Data': '1'+TOS+'1'+RATE}


class PathTearRSVP:
    def __init__(self):
        pass

    HEADER = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x05)}
    SESSION = {'Data': '192.168.0.100'}
    HOP = {'neighbor': '192.168.0.109', 'inface': 3}
    TIME = {'refresh': 4}
    SENDER_TEMPLATE = {'Data': '1'+SOURCE_ADDRESS+'1'+DEST_ADDRESS}
    ADSPEC = {'Data': '1'+TOS+'1'+RATE}
