from scapy.contrib.rsvp import *
from src.rsvp.GenerateRSVPMsg import generate_msg
from src.htb.Reserve import *
from src.utils.Utils import *

HEADER = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x02)}
TIME = {'refresh': 4}
STYLE = {'Data': 'WF'}
SENDER_TEMPLATE = {'Data': '100192.168.0.106100192.168.0.105'}


def generate_resv(data):
    session = {'Data': get_layer(data, Const.CL_SESSION).getfieldval('Data')}
    hop = {'neighbor': get_layer(data, Const.CL_HOP).getfieldval('neighbor'),
           'inface': get_layer(data, Const.CL_HOP).getfieldval('inface')}
    rsvp_pkt = dict(header=HEADER, session=session, hop=hop, time=TIME,
                    style=STYLE, sender_template=SENDER_TEMPLATE,
                    flowspec={'Data': get_layer(data, Const.CL_ADSPEC).getfieldval('Data')})
    pkt = IP(dst=data.getlayer('IP').getfieldval('dst'))/generate_msg(**rsvp_pkt)
    # pkt = IP(dst=dst) / RSVP(TTL=65, Class=0x01) / RSVP_Object(Class=0x03) / RSVP_HOP(neighbor='192.168.0.107')
    pkt.show2()
    Logger.logger.info('Sending Resv Message. . .')
    send(pkt)


def process_resv(data):
    Logger.logger.info('Processing Resv Message. . .')
    req = get_reservation_info(data, 'Resv')
    is_reserved = reserve(req)
    is_sender = req.src_ip == get_current_hop(req.src_ip)
    Logger.logger.info(req.src_ip + ' ' + get_current_hop(req.src_ip))
    if is_reserved:
        Logger.logger.info('Reservation success')
        if not is_sender:
            send_next_hop(req.src_ip, data, 'Resv')
        else:
            Logger.logger.info('Full Reservation completed successfully')
    else:
        Logger.logger.info('Reservation failed')


