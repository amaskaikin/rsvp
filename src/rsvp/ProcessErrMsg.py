from src.utils.Utils import *
from scapy.contrib.rsvp import *
from src.rsvp.GenerateRSVPMsg import generate_msg


HEADER_PATH_ERR = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x03)}
HEADER_RESV_ERR = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x04)}
TIME = {'refresh': 4}
STYLE = {'Data': 'WF'}


def generate_path_err(data, err_msg):
    session = {'Data': get_layer(data, Const.CL_SESSION).getfieldval('Data')}
    hop = {'neighbor': get_layer(data, Const.CL_HOP).getfieldval('neighbor'),
           'inface': get_layer(data, Const.CL_HOP).getfieldval('inface')}
    err_spec = {'Data': err_msg}
    sender_temp = {'Data': get_layer(data, Const.CL_SENDTEMP).getfieldval('Data')}
    rsvp_pkt = dict(header=HEADER_PATH_ERR, session=session, hop=hop, time=TIME,
                    error_spec=err_spec, sender_template=sender_temp)
    pkt = IP(dst=data.getlayer('IP').getfieldval('dst'))/generate_msg(**rsvp_pkt)
    del pkt.chksum
    pkt = pkt.__class__(str(pkt))
    pkt.show2()
    Logger.logger.info('Sending PathErr Message. . .')
    send(pkt)


def generate_resv_err(data, err_msg):
    session = {'Data': get_layer(data, Const.CL_SESSION).getfieldval('Data')}
    hop = {'neighbor': get_layer(data, Const.CL_HOP).getfieldval('neighbor'),
           'inface': get_layer(data, Const.CL_HOP).getfieldval('inface')}
    err_spec = {'Data': err_msg}
    flowspec = {'Data': get_layer(data, Const.CL_ADSPEC).getfieldval('Data')}
    rsvp_pkt = dict(header=HEADER_RESV_ERR, session=session, hop=hop, time=TIME,
                    error_spec=err_spec, style=STYLE, flowspec=flowspec)
    pkt = IP(dst=data.getlayer('IP').getfieldval('dst'))/generate_msg(**rsvp_pkt)
    del pkt.chksum
    pkt = pkt.__class__(str(pkt))
    pkt.show2()
    Logger.logger.info('Sending ResvErr Message. . .')
    send(pkt)


def process_path_err(data):
    Logger.logger.info('Processing PathErr Message. . .')
    dst_ip = get_sendtemp_data(data).get('src')
    is_last_hop = dst_ip == get_current_hop(dst_ip)
    if not is_last_hop:
        send_next_hop(dst_ip, data, 'PathErr')
    else:
        Logger.logger.info('PathErr message reached the sender')


def process_resv_err(data):
    Logger.logger.info('Processing PathErr Message. . .')
    dst_ip = data.getlayer(0).getfieldval('dst')
    is_sender = dst_ip == get_current_hop(dst_ip)
    if is_sender:
        Logger.logger.info('PathErr message reached the sender')
        return
    req = ReservationRequest.Instance()
    err_spec = get_layer(data, Const.CL_ERRSPEC).getfieldval('Data')
    Logger.logger.info('[ResvErr] Reservation Error: ' + str(err_spec))
    send_next_hop(req.src_ip, data, 'ResvErr')


def send_error(ip, data, msg_type, msg):
    src_ip = get_current_hop(ip)
    ip = get_next_hop(ip)
    Logger.logger.info('Sending error' + msg_type + ' message to next hop: ' + ip)
    data.getlayer('IP').setfieldval('dst', ip)
    data.getlayer('IP').setfieldval('src', src_ip)
    get_layer(data, Const.CL_SESSION).setfieldval('Data', ip)
    data.getlayer('HOP').setfieldval('neighbor', src_ip)
    del data.chksum
    data = data.__class__(str(data))
    data.show2()
    if msg_type == 'path':
        generate_path_err(data, msg)
    else:
        generate_resv_err(data, msg)
