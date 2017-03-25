from scapy.all import *
from src.htb.Reserve import *
from src.rsvp.ProcessResvMsg import *


def process_path(data):
    Logger.logger.info('Processing Path Message. . .')
    res_req = get_reservation_info(data)
    is_available = check_reserve(res_req)
    is_last_hop = res_req.dst_ip == get_current_hop(res_req.dst_ip)
    # TODO: send error message
    if is_available:
        Logger.logger.info('Required bandwidth is available')

        if not is_last_hop:
            send_next_hop(res_req.dst_ip, data, 'Path')
        else:
            Logger.logger.info('Path message reached the last hop')
            process_last_hop(res_req, data)


def process_last_hop(req, data):
    Logger.logger.info('Processing Last Path Hop. . .')
    is_reserved = reserve(req)
    if is_reserved:
        Logger.logger.info('Reservation success')
        ip = get_next_hop(req.src_ip)
        data.getlayer('IP').setfieldval('dst', ip)
        get_layer(data, Const.CL_SESSION).setfieldval('Data', ip)
        get_layer(data, Const.CL_HOP).setfieldval('neighbor', get_current_hop(ip))
        generate_resv(data)


def get_reservation_info(data):
    src_ip = None
    dst_ip = None
    tos = None
    req_speed = None
    req = ReservationRequest.Instance()
    sendtemp_layer = get_layer(data, Const.CL_SENDTEMP)
    sendtemp_data = sendtemp_layer.getfieldval('Data')
    if int(sendtemp_data[0]) == 1:
        src_ip = sendtemp_data[1:16].lstrip('0')
    if int(sendtemp_data[16]) == 1:
        dst_ip = sendtemp_data[17:32].lstrip('0')

    adspec_layer = get_layer(data, Const.CL_ADSPEC)
    adspec_data = adspec_layer.getfieldval('Data')
    if int(adspec_data[0]) == 1:
        tos = adspec_data[1:3].lstrip('0')
    if int(adspec_data[3]) == 1:
        req_speed = adspec_data[4:10].lstrip('0')

    Logger.logger.info('[Path] Reservation request: src ip: ' + src_ip + ', dst ip: ' + dst_ip +
                       ', tos: ' + tos + ', rate: ' + req_speed)

    if not any((src_ip, dst_ip, tos, req_speed)):
        Logger.logger.info('[Path] Illegal values:src ip: ' + src_ip + ', dst ip: ' + dst_ip +
                           ', tos: ' + tos + ', rate: ' + req_speed)

    # res_req = ReservationRequest(src_ip, dst_ip, tos, int(req_speed))
    req.src_ip = src_ip
    req.dst_ip = dst_ip
    req.tos = tos
    req.speed = int(req_speed)
    return req
