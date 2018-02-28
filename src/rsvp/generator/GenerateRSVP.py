# Generate RSVP data

from GenerateRSVPMsg import *
from src.htb.Reserve import *
from src.rsvp.model.RSVP_Path import *

HEADER_RESV = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x02)}
HEADER_RTEAR = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x06)}
TIME = {'refresh': 4}
STYLE = {'Data': 'WF'}

HEADER_PATH_ERR = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x03)}
HEADER_RESV_ERR = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x04)}


def generate_path(dst):
    # Create test RSVP packet
    rsvp_pkt = dict(header=PathRSVP.HEADER, time=PathRSVP.TIME,
                    sender_template=PathRSVP.SENDER_TEMPLATE, adspec=PathRSVP.ADSPEC)
    pkt = IP(dst=dst)/generate_msg(**rsvp_pkt)
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


def generate_resv(data, key):
    flowspec = {'Data': get_layer(data, Const.CL_ADSPEC).getfieldval('Data')}
    msg_id = {'Data': key}
    rsvp_pkt = dict(header=HEADER_RESV, time=TIME,
                    style=STYLE, flowspec=flowspec, msg_id=msg_id)
    pkt = IP(dst=data.getlayer('IP').getfieldval('dst'))/generate_msg(**rsvp_pkt)
    del pkt.chksum
    pkt = pkt.__class__(str(pkt))
    pkt.show2()
    Logger.logger.info('Sending Resv Message. . .')
    send(pkt)


def generate_path_err(data, err_msg):
    err_spec = {'Data': err_msg}
    sender_temp = {'Data': get_layer(data, Const.CL_SENDTEMP).getfieldval('Data')}
    rsvp_pkt = dict(header=HEADER_PATH_ERR, time=TIME,
                    error_spec=err_spec, sender_template=sender_temp)
    pkt = IP(dst=data.getlayer('IP').getfieldval('dst'))/generate_msg(**rsvp_pkt)
    del pkt.chksum
    pkt = pkt.__class__(str(pkt))
    pkt.show2()
    Logger.logger.info('Sending PathErr Message. . .')
    send(pkt)


def generate_resv_err(data, err_msg):
    err_spec = {'Data': err_msg}
    flowspec = {'Data': get_layer(data, Const.CL_ADSPEC).getfieldval('Data')}
    rsvp_pkt = dict(header=HEADER_RESV_ERR, time=TIME,
                    error_spec=err_spec, style=STYLE, flowspec=flowspec)
    pkt = IP(dst=data.getlayer('IP').getfieldval('dst'))/generate_msg(**rsvp_pkt)
    del pkt.chksum
    pkt = pkt.__class__(str(pkt))
    pkt.show2()
    Logger.logger.info('Sending ResvErr Message. . .')
    send(pkt)


def generate_resv_tear(data, key):
    flowspec = {'Data': get_layer(data, Const.CL_ADSPEC).getfieldval('Data')}
    rsvp_pkt = dict(header=HEADER_RTEAR, time=TIME,
                    style=STYLE, flowspec=flowspec, msg_id=key)
    pkt = IP(dst=data.getlayer('IP').getfieldval('dst'))/generate_msg(**rsvp_pkt)
    pkt.show2()
    Logger.logger.info('Sending ResvTear Message. . .')
    send(pkt)


if __name__ == '__main__':
    try:
        generate_path(Const.TARGET_ADDRESS)
        # generate_path_tear(Const.TARGET_ADDRESS)
    except KeyboardInterrupt:
        pass
