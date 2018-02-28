
from src.htb.Reserve import *
from src.rsvp.processor.ProcessErrMsg import *
from src.rsvp.processor.ProcessLastHop import process_pathtear_last_hop


def process_path(data):
    Logger.logger.info('Processing Path Message. . .')
    res_req = get_reservation_info(data)
    is_available, key = check_reserve(res_req)
    is_last_hop = res_req.dst_ip == get_current_hop(res_req.dst_ip)
    callback = Callback(res_req, data, key, is_available, not is_last_hop, 'Path', res_req.dst_ip)
    Logger.logger.info('Required bandwidth is available: ' + str(is_available))
    Logger.logger.info('Path: is last hop: ' + str(is_last_hop))
    if not is_available:
        error_o = Error(str(get_current_hop(res_req.dst_ip)) + str(key), 'path')
        callback.error = error_o

    return callback


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
            process_pathtear_last_hop(req, data, None)
    else:
        Logger.logger.info('Error during destroying process: path is broken')


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


