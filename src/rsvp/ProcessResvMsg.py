from scapy.contrib.rsvp import *
from src.rsvp.GenerateRSVPMsg import generate_msg
from src.htb.Reserve import *
from src.utils.Utils import *

HEADER = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x02)}
TIME = {'refresh': 4}
STYLE = {'Data': 'WF'}


def generate_resv(data):
    session = {'Data': get_layer(data, Const.CL_SESSION).getfieldval('Data')}
    hop = {'neighbor': get_layer(data, Const.CL_HOP).getfieldval('neighbor'),
           'inface': get_layer(data, Const.CL_HOP).getfieldval('inface')}
    rsvp_pkt = dict(header=HEADER, session=session, hop=hop, time=TIME,
                    style=STYLE, flowspec={'Data': get_layer(data, Const.CL_ADSPEC).getfieldval('Data')})
    pkt = IP(dst=data.getlayer('IP').getfieldval('dst'))/generate_msg(**rsvp_pkt)
    pkt.show2()
    send(pkt)


def process_resv(data):
    Logger.logger.info('Processing Resv Message. . .')
    req = ReservationRequest.Instance()
    Logger.logger.info('[Resv] Reservation request: src ip: ' + req.src_ip + ', dst ip: ' + req.dst_ip +
                       ', tos: ' + req.tos + ', rate: ' + req.speed)
    # req = get_reservation_info(data, 'Resv')
    is_reserved = reserve(req)
    is_sender = req.src_ip == get_current_hop(req.src_ip)
    if is_reserved:
        Logger.logger.info('Reservation success')
        if not is_sender:
            send_next_hop(req.src_ip, data, 'Resv')
        else:
            Logger.logger.info('Full Reservation completed successfully')
    else:
        Logger.logger.info('Reservation failed')


