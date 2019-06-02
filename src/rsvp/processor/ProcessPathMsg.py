
from src.htb.Reserve import *
from src.rsvp.processor.ProcessErrMsg import *
from src.utils.RSVPDataHelper import get_spec_data, process_static_route


def process_path(data):
    Logger.logger.info('Processing Path Message. . .')
    res_req = get_reservation_info(data)

    current_ip = get_current_hop(res_req.dst_ip)
    next_hop_ip = get_next_hop(res_req.dst_ip)
    data, is_valid_route, static_route = process_static_route(data, current_ip)
    next_ip, is_static = get_direction_ip(static_route, next_hop_ip)

    is_available, key = check_reserve(res_req)
    is_last_hop = next_ip == res_req.dst_ip
    if is_static:
        db_service.set_previous_hop(key, data.getlayer('IP').getfieldval('src'))
    callback = Callback(res_req, data, key, is_available, not is_last_hop, 'Path', next_ip, is_static=is_static)
    Logger.logger.info('[Path]: Required bandwidth is available: ' + str(is_available))
    Logger.logger.info('[Path]: is last hop: ' + str(is_last_hop))
    if not is_available:
        error_o = Error(str(get_current_hop(res_req.dst_ip)) + str(key), 'path')
        callback.error = error_o
    if not is_valid_route:
        error_o = Error('[Path]: Static route is invalid' + str(key), 'path')
        callback.error = error_o

    return callback


def process_path_tear(data):
    Logger.logger.info('Processing PathTear Message. . .')
    res_req = get_reservation_info(data)
    is_marked_for_destroy, key = mark_destroy_path(res_req)

    current_ip = get_current_hop(res_req.dst_ip)
    next_hop_ip = get_next_hop(res_req.dst_ip)
    data, is_valid_route, static_route = process_static_route(data, current_ip)
    next_ip, is_static = get_direction_ip(static_route, next_hop_ip)

    is_last_hop = next_ip == res_req.dst_ip
    Logger.logger.info('[PathTear] next_hop_ip: ' + next_hop_ip)
    Logger.logger.info('[PathTear]: is last hop: ' + str(is_last_hop))

    callback = Callback(res_req, data, key, is_marked_for_destroy, not is_last_hop, 'Path',
                        res_req.dst_ip, is_static=is_static)
    Logger.logger.info('[PathTear]: is destroyed' + str(is_marked_for_destroy))

    if not is_marked_for_destroy:
        error_o = Error(str(get_current_hop(res_req.dst_ip)) + str(key) + " PathTear error", 'path')
        callback.error = error_o

    return callback


def get_reservation_info(data):
    req = ReservationRequest.Instance()
    src_ip = get_sendtemp_data(data).get('src')
    dst_ip = get_sendtemp_data(data).get('dst')
    tos = get_spec_data(data).get('tos')
    req_speed = get_spec_data(data).get('speed')

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
