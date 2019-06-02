# Generate RSVP data
import argparse
from .GenerateRSVPMsg import *
from src.htb.Reserve import *
from src.rsvp.model.RSVP_Path import *
from src.utils.RSVPDataHelper import get_layer
from src.db.DbService import DbService

HEADER_RESV = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x02)}
HEADER_RTEAR = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x06)}
TIME = {'refresh': 4}
STYLE = {'Data': 'WF'}

HEADER_PATH_ERR = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x03)}
HEADER_RESV_ERR = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x04)}


def generate_path(path_msg, dst):
    # Create test RSVP packet
    rsvp_pkt = dict(header=path_msg.header_obj, time=path_msg.time,
                    sender_template=path_msg.sender_template, adspec=path_msg.adspec)
    if path_msg.route_obj is not None:
        rsvp_pkt['route'] = path_msg.route_obj
    pkt = IP(dst=dst, src=path_msg.src_ip.lstrip('0'))/generate_msg(**rsvp_pkt)
    # pkt = IP(dst=dst) / RSVP(TTL=65, Class=0x01) / RSVP_Object(Class=0x03) / RSVP_HOP(neighbor='192.168.0.107')
    pkt.show()
    Logger.logger.info('Sending Path message to ' + dst.lstrip('0') + ' . . .')
    # while True:
    send(pkt)
    # time.sleep(5)


def generate_path_tear(path_tear, dst=None, is_autobandwidth=False, new_bw=None):
    # Create test RSVP packet
    if is_autobandwidth:
        path_tear = PathTearRSVP(path_tear[DbService.DB_SRC_IP], path_tear[DbService.DB_DST_IP],
                                 path_tear[DbService.DB_TOS], path_tear[DbService.DB_SPEED], new_bw=new_bw)
        dst = get_next_hop(path_tear.dst_ip)
    rsvp_pkt = dict(header=path_tear.header_obj, time=path_tear.time,
                    sender_template=path_tear.sender_template, adspec=path_tear.adspec)
    if path_tear.route_obj is not None:
        rsvp_pkt['route'] = path_tear.route_obj
    pkt = IP(src=path_tear.src_ip.lstrip('0'), dst=dst)/generate_msg(**rsvp_pkt)
    pkt.show()
    Logger.logger.info('Sending PathTear message to ' + dst.lstrip('0') + ' . . .')
    send(pkt)


def generate_resv(data, key):
    flowspec = {'Data': get_layer(data, Const.CL_ADSPEC).getfieldval('Data')}
    msg_id = {'Data': key}
    rsvp_pkt = dict(header=HEADER_RESV, time=TIME,
                    style=STYLE, flowspec=flowspec, msg_id=msg_id)
    dst = data.getlayer('IP').getfieldval('dst')
    pkt = IP(dst=dst)/generate_msg(**rsvp_pkt)
    del pkt.chksum
    pkt = pkt.__class__(str(pkt))
    pkt.show2()
    Logger.logger.info('Sending Resv Message to' + dst.lstrip('0') + ' . . .')
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
    msg_id = {'Data': key}
    rsvp_pkt = dict(header=HEADER_RTEAR, time=TIME,
                    style=STYLE, flowspec=flowspec, msg_id=msg_id)
    dst = data.getlayer('IP').getfieldval('dst')
    pkt = IP(dst=dst)/generate_msg(**rsvp_pkt)
    del pkt.chksum
    pkt = pkt.__class__(str(pkt))
    pkt.show2()
    Logger.logger.info('Sending ResvTear Message to' + dst.lstrip('0') + ' . . .')
    send(pkt)


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('-src', '--source_ip', dest='src_ip', required=True)
        parser.add_argument('-dst', '--dest_ip', dest='dst_ip', required=True)
        parser.add_argument('-tos', '--tos', dest='tos', required=True)
        parser.add_argument('-rate', '--bandwidth_rate', dest='rate', required=True)
        parser.add_argument('-route', nargs='+', dest='route')
        parser.add_argument('-ifaces', nargs='+', dest='ifaces')

        parsed = parser.parse_args()  # parses sys.argv by default
        rsvp = PathRSVP(parsed.src_ip, parsed.dst_ip, parsed.tos, parsed.rate, parsed.route, parsed.ifaces)
        next_ip = get_next_hop(parsed.dst_ip)
        generate_path(rsvp, next_ip)
        # generate_path_tear(Const.TARGET_ADDRESS)
    except KeyboardInterrupt:
        pass
