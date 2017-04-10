# Generate RSVP data

from scapy.all import *

from GenerateRSVPMsg import *
from RSVP_Path import *
from src.utils.Logger import Logger
from src.data.ReservationRequest import *
from src.htb.Reserve import *


def generate_path(dst):
    # Create test RSVP packet
    rsvp_pkt = dict(header=PathRSVP.HEADER, time=PathRSVP.TIME,
                    sender_template=PathRSVP.SENDER_TEMPLATE, adspec=PathRSVP.ADSPEC)
    pkt = IP(dst=dst)/generate_msg(**rsvp_pkt)

    # Testing stub for keeping requested qos on the sender
    req = ReservationRequest.Instance()
    req.src_ip = SOURCE_ADDRESS.lstrip('0')
    req.dst_ip = DEST_ADDRESS.lstrip('0')
    req.tos = int(TOS)
    req.speed = int(RATE)
    check_reserve(req)
    # pkt = IP(dst=dst) / RSVP(TTL=65, Class=0x01) / RSVP_Object(Class=0x03) / RSVP_HOP(neighbor='192.168.0.107')
    pkt.show2()
    Logger.logger.info('Sending Path message to ' + DEST_ADDRESS.lstrip('0') + ' . . .')
    # while True:
    send(pkt)
    # time.sleep(5)


def generate_path_tear(dst):
    # Create test RSVP packet
    rsvp_pkt = dict(header=PathTearRSVP.HEADER,
                    time=PathTearRSVP.TIME, sender_template=PathTearRSVP.SENDER_TEMPLATE, adspec=PathTearRSVP.ADSPEC)
    pkt = IP(dst=dst)/generate_msg(**rsvp_pkt)
    pkt.show2()
    Logger.logger.info('Sending PathTear message to ' + DEST_ADDRESS.lstrip('0') + ' . . .')
    send(pkt)


if __name__ == '__main__':
    try:
        generate_path(Const.TARGET_ADDRESS)
        # generate_path_tear(Const.TARGET_ADDRESS)
    except KeyboardInterrupt:
        pass
