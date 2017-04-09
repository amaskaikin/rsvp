from scapy.all import *
from src.htb.Reserve import *
from src.rsvp.ProcessResvMsg import *
from src.rsvp.ProcessErrMsg import *


def process_path(data):
    Logger.logger.info('Processing Path Message. . .')
    res_req = get_reservation_info(data)
    is_available = check_reserve(res_req)
    is_last_hop = res_req.dst_ip == get_current_hop(res_req.dst_ip)
    if is_available:
        Logger.logger.info('Required bandwidth is available')
        if not is_last_hop:
            send_next_hop(res_req.dst_ip, data, 'Path')
        else:
            Logger.logger.info('Path message reached the last hop')
            process_path_last_hop(res_req, data)
    else:
        error_msg = str(get_current_hop(res_req.dst_ip)) + ': Required bandwidth is not available'
        send_error(data, res_req.src_ip, error_msg, 'path')


def process_path_tear(data):
    Logger.logger.info('Processing PathTear Message. . .')
    req = ReservationRequest.Instance()
    src_ip = get_sendtemp_data(data).get('src')
    dst_ip = get_sendtemp_data(data).get('dst')
    tos = get_adspec_data(data).get('tos')
    req_speed = get_adspec_data(data).get('speed')
    is_last_hop = req.dst_ip == get_current_hop(req.dst_ip)
    if req.src_ip == src_ip and req.dst_ip == dst_ip and str(req.tos) == str(tos) and str(req.speed) == str(req_speed):
        Logger.logger.info('Destroying Path: src ip: ' + src_ip + ', dst ip: ' + dst_ip +
                           ', tos: ' + str(tos) + ', rate: ' + str(req_speed))
        if not is_last_hop:
            send_next_hop(req.dst_ip, data, 'PathTear')
        else:
            Logger.logger.info('PathTear message reached the last hop')
            process_pathtear_last_hop(req, data)
    else:
        Logger.logger.info('Error during destroying process: path is broken')


def process_path_last_hop(req, data):
    Logger.logger.info('Processing Last Path Hop. . .')
    is_reserved = reserve(req)
    req_id = 1
    if is_reserved:
        Logger.logger.info('Reservation success')
        ip = get_next_hop(req.src_ip)
        src_ip = get_current_hop(req.src_ip)
        data.getlayer('IP').setfieldval('dst', ip)
        data.getlayer('IP').setfieldval('src', src_ip)
        generate_resv(data, req_id)
    else:
        Logger.logger.info('Reservation failed for request: src ip: ' + req.src_ip +
                           ', dst ip: ' + req.dst_ip +
                           ', tos: ' + req.tos + ', rate: ' + req.req_speed)
        error_msg = str(get_current_hop(req.src_ip)) + ': Reservation failed'
        send_error(data, req.src_ip, error_msg, 'path')


def process_pathtear_last_hop(req, data):
    Logger.logger.info('Processing Last PathTear Hop. . .')
    # TODO: call destroy method
    is_destroyed = reserve(req)
    if is_destroyed:
        Logger.logger.info('Destroyed successfully')
        ip = get_next_hop(req.src_ip)
        src_ip = get_current_hop(req.src_ip)
        data.getlayer('IP').setfieldval('dst', ip)
        data.getlayer('IP').setfieldval('src', src_ip)
        generate_resv(data)
    else:
        Logger.logger.info('Destroying failed for request: src ip: ' + req.src_ip +
                           ', dst ip: ' + req.dst_ip +
                           ', tos: ' + str(req.tos) + ', rate: ' + str(req.speed))


def get_reservation_info(data):
    req = ReservationRequest.Instance()
    src_ip = get_sendtemp_data(data).get('src')
    dst_ip = get_sendtemp_data(data).get('dst')
    tos = get_adspec_data(data).get('tos')
    req_speed = get_adspec_data(data).get('speed')

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


