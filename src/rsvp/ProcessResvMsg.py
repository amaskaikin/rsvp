from scapy.contrib.rsvp import *
from src.rsvp.GenerateRSVPMsg import generate_msg
from src.htb.Reserve import *
from src.utils.Utils import *
from src.rsvp.ProcessErrMsg import *

HEADER_RESV = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x02)}
HEADER_RTEAR = {'TTL': 65, 'Class': rsvpmsgtypes.get(0x06)}
TIME = {'refresh': 4}
STYLE = {'Data': 'WF'}


def generate_resv(data, req_id):
    flowspec = {'Data': get_layer(data, Const.CL_ADSPEC).getfieldval('Data')}
    msg_id = {'Data': req_id}
    rsvp_pkt = dict(header=HEADER_RESV, time=TIME,
                    style=STYLE, flowspec=flowspec, msg_id=msg_id)
    pkt = IP(dst=data.getlayer('IP').getfieldval('dst'))/generate_msg(**rsvp_pkt)
    del pkt.chksum
    pkt = pkt.__class__(str(pkt))
    pkt.show2()
    Logger.logger.info('Sending Resv Message. . .')
    send(pkt)


def generate_resv_tear(data, req_id):
    flowspec = {'Data': get_layer(data, Const.CL_ADSPEC).getfieldval('Data')}
    rsvp_pkt = dict(header=HEADER_RTEAR, time=TIME,
                    style=STYLE, flowspec=flowspec, msg_id=req_id)
    pkt = IP(dst=data.getlayer('IP').getfieldval('dst'))/generate_msg(**rsvp_pkt)
    pkt.show2()
    Logger.logger.info('Sending ResvTear Message. . .')
    send(pkt)


def process_resv(data):
    Logger.logger.info('Processing Resv Message. . .')
    # TODO: move logic to htb, get request parameters from there by id
    key = get_layer(data, Const.CL_MSG_ID).getfieldval('Data')
    req = ReservationRequest.Instance()
    # req = get request parameters from htb by id
    # req.src_ip, req.dst_ip, req.tos, req.speed = ...
    is_class, ret = get_class(key)
    if is_class:     
        req.src_ip = ret[0]
        req.dst_ip = ret[1]
        req.tos = ret[2]
        req.speed = ret[3]
        Logger.logger.info('[Resv] Reservation request: src ip: ' + str(req.src_ip) + ', dst ip: ' + str(req.dst_ip) +
                           ', tos: ' + str(req.tos) + ', rate: ' + str(req.speed))
        ip = data.getlayer(0).getfieldval('dst')
        is_sender = ip == req.src_ip
        if is_sender:
            Logger.logger.info('Resv message reached the sender.')
            Logger.logger.info('Full Reservation completed successfully')
            return
        if not any((req.src_ip, req.dst_ip, req.tos, req.speed)):
            Logger.logger.info('Error! Path is broken')
            error_msg = str(get_current_hop(req.src_ip)) + ': Error! Path is broken'
            send_error(req.src_ip, data, error_msg, 'resv')
            return
    else:
        Logger.logger.info('Htb class not found')
        error_msg = str(get_current_hop(req.src_ip)) + ret
        send_error(req.src_ip, data, error_msg, 'resv')
        return
    is_reserved, ret = reserve(req)
    Logger.logger.info('[Resv] : req_src ip: ' + str(req.src_ip) + ', src ip: ' + str(get_current_hop(req.src_ip)))
    if is_reserved:
        Logger.logger.info('Reservation success')
        send_next_hop(req.src_ip, data, 'Resv')
    else:
        Logger.logger.info('Reservation failed')
        error_msg = str(get_current_hop(req.src_ip)) + ret
        send_error(req.src_ip, data, error_msg, 'resv')


def process_resv_tear(data):
    Logger.logger.info('Processing ResvTear Message. . .')
    ip = data.getlayer(0).getfieldval('dst')
    is_sender = ip == get_current_hop(ip)
    if is_sender:
        Logger.logger.info('ResvTear message reached the sender.')
        Logger.logger.info('Full Reservation destroying completed successfully')
        return
    id = get_layer(data, Const.CL_MSG_ID).getfieldval('Data')
    # req = get request parameters from htb by id
    # req.src_ip, req.dst_ip, req.tos, req.speed = ...
    req = ReservationRequest.Instance()
    if not any((req.src_ip, req.dst_ip, req.tos, req.speed)):
        Logger.logger.info('Error! Path is broken')
        return
    Logger.logger.info('[ResvTear] Destroying request: src ip: ' + str(req.src_ip) + ', dst ip: ' + str(req.dst_ip) +
                       ', tos: ' + str(req.tos) + ', rate: ' + str(req.speed))
    # TODO: call destroy method
    is_destroyed = reserve(req)
    Logger.logger.info('[ResvTear] : req_src ip: ' + str(req.src_ip) + ', src ip: ' + str(get_current_hop(req.src_ip)))
    if is_destroyed:
        Logger.logger.info('Destroying completed successfully')
        send_next_hop(req.src_ip, data, 'ResvTear')
    else:
        Logger.logger.info('Destroying failed')
