
from src.htb.Reserve import *
from src.rsvp.processor.ProcessErrMsg import *
from src.rsvp.processor.ProcessLastHop import process_pathtear_last_hop
from src.utils.RSVPDataHelper import get_adspec_data, get_scope_data, set_scope_data


def process_path(data):
    Logger.logger.info('Processing Path Message. . .')
    res_req = get_reservation_info(data)
    is_available, key = check_reserve(res_req)
    current_ip = get_current_hop(res_req.dst_ip)
    data, is_valid_route, static_route = process_static_route(data, current_ip)
    next_ip, is_static = get_direction_ip(static_route, res_req.dst_ip)

    is_last_hop = next_ip == current_ip
    callback = Callback(res_req, data, key, is_available, not is_last_hop, 'Path', next_ip, is_static=is_static)
    Logger.logger.info('Required bandwidth is available: ' + str(is_available))
    Logger.logger.info('Path: is last hop: ' + str(is_last_hop))
    if not is_available:
        error_o = Error(str(get_current_hop(res_req.dst_ip)) + str(key), 'path')
        callback.error = error_o
    if not is_valid_route:
        error_o = Error('Static route is invalid' + str(key), 'path')
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


def process_static_route(data, current_ip):
    is_valid_route = True
    static_route_obj = get_scope_data(data)
    if static_route_obj is None:
        return data, is_valid_route, None

    static_route = static_route_obj.get('static_route')
    if current_ip in static_route:
        idx = static_route.index(current_ip)
        if idx == 0:
            static_route.remove(current_ip)
            data = set_scope_data(data, static_route)
        else:
            Logger.logger.info('[Process Path Message] Error: static route is invalid')
            is_valid_route = False
    else:
        Logger.logger.info('[Process Path Message] Error: static route is invalid')
        is_valid_route = False

    return data, is_valid_route, static_route


def get_direction_ip(static_route, next_ip):
    if static_route is None:
        return next_ip, False
    else:
        return static_route[0], True
