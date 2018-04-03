from scapy.contrib.rsvp import *

from src.utils.Utils import format_address, format_route

SOURCE_ADDRESS = '000000001.1.1.1'
DEST_ADDRESS = '000000001.1.2.2'
TOS = '08'
RATE = '6000000'


class PathRSVP:
    def __init__(self, src_ip, dst_ip, tos, rate, route=None, interfaces=None):
        self.src_ip = format_address(src_ip)
        self.dst_ip = format_address(dst_ip)
        self.tos = tos
        self.rate = rate
        self.route = format_route(route)
        self.interfaces = interfaces

        self.header_obj = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x01)}
        # SESSION = {'Data': '192.168.0.100'}
        # HOP = {'neighbor': '192.168.0.109', 'inface': 3}
        self.time = {'refresh': 4}
        self.sender_template = {'Data': '1'+self.src_ip+'1'+self.dst_ip}
        self.adspec = {'Data': '1'+self.tos+'1'+self.rate}
        self.route_obj = {'Data': '1' + '1'.join(self.route)}


class PathTearRSVP:
    def __init__(self):
        pass

    HEADER = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x05)}
    TIME = {'refresh': 4}
    SENDER_TEMPLATE = {'Data': '1'+SOURCE_ADDRESS+'1'+DEST_ADDRESS}
    ADSPEC = {'Data': '1'+TOS+'1'+RATE}
