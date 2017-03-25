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
    ip = data.getlayer(0).getfieldval('dst')
    is_sender = ip == get_current_hop(ip)
    if is_sender:
        Logger.logger.info('Resv message reached the sender.')
        Logger.logger.info('Full Reservation completed successfully')
        return
    req = ReservationRequest.Instance()
    if not any((req.src_ip, req.dst_ip, req.tos, req.speed)):
        Logger.logger.info('Error! Path is broken')
        return
    Logger.logger.info('[Resv] Reservation request: src ip: ' + str(req.src_ip) + ', dst ip: ' + str(req.dst_ip) +
                       ', tos: ' + str(req.tos) + ', rate: ' + str(req.speed))
    # req = get_reservation_info(data, 'Resv')
    is_reserved = reserve(req)
    # is_sender = req.src_ip == get_current_hop(req.src_ip)
    Logger.logger.info('[Resv] : req_src ip: ' + str(req.src_ip) + ', src ip: ' + str(get_current_hop(req.src_ip)))
    if is_reserved:
        Logger.logger.info('Reservation success')
        send_next_hop(req.src_ip, data, 'Resv')
    else:
        Logger.logger.info('Reservation failed')


