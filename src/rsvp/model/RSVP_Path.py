from scapy.contrib.rsvp import *

from src.utils.Utils import format_address, format_route, format_speed

SOURCE_ADDRESS = '000000001.1.1.1'
DEST_ADDRESS = '000000001.1.2.2'
TOS = '08'
RATE = '6000000'


class PathRSVP:
    def __init__(self, src_ip, dst_ip, tos, rate, route=None, interfaces=None):
        self.src_ip = format_address(src_ip)
        self.dst_ip = format_address(dst_ip)
        self.tos = str(tos).zfill(2)
        self.rate = format_speed(rate)
        self.route = format_route(route)
        self.interfaces = interfaces

        self.header_obj = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x01), 'Version': 1}
        # SESSION = {'Data': '192.168.0.100'}
        # HOP = {'neighbor': '192.168.0.109', 'inface': 3}
        self.time = {'refresh': 4}
        self.sender_template = {'Data': '1'+self.src_ip+'1'+self.dst_ip +
                                        ('1'.join(self.interfaces) if interfaces else '')}
        self.adspec = {'Data': '1'+self.tos+'1'+self.rate}
        if route:
            self.route_obj = {'Data': '1' + '1'.join(self.route)}
        else:
            self.route_obj = None


class PathTearRSVP:
    # TODO: add new object with changed bw and change it in resv tear
    def __init__(self, src_ip, dst_ip, tos, rate, route=None, interfaces=None, new_bw=None):
        self.src_ip = format_address(src_ip)
        self.dst_ip = format_address(dst_ip)
        self.tos = str(tos).zfill(2)
        self.rate = format_speed(rate)
        self.new_rate = new_bw
        self.route = format_route(route)
        self.interfaces = interfaces

        self.header_obj = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x05), 'Version': 1}
        # SESSION = {'Data': '192.168.0.100'}
        # HOP = {'neighbor': '192.168.0.109', 'inface': 3}
        self.time = {'refresh': 4}
        self.sender_template = {'Data': '1' + self.src_ip + '1' + self.dst_ip +
                                        ('1'.join(self.interfaces) if interfaces else '')}
        self.adspec = {'Data': '1' + str(self.tos) + '1' + str(self.rate) +
                               ('1' + str(self.new_rate)) if self.new_rate else ''}
        if route:
            self.route_obj = {'Data': '1' + '1'.join(self.route)}
        else:
            self.route_obj = None

    HEADER = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x05)}
    TIME = {'refresh': 4}
    SENDER_TEMPLATE = {'Data': '1'+SOURCE_ADDRESS+'1'+DEST_ADDRESS}
    ADSPEC = {'Data': '1'+TOS+'1'+RATE}
