from src.rsvp.model.Callback import build_callback, build_callback_error
from src.htb.Reserve import *
from src.rsvp.processor.ProcessErrMsg import *


def process_resv(data):
    Logger.logger.info('Processing Resv Message. . .')
    key = get_layer(data, Const.CL_MSG_ID).getfieldval('Data')
    is_class, ret = get_class(key)
    Logger.logger.info('is_class ' + str(is_class) + ' ret ' + str(ret))
    req = ReservationRequest.Instance()
    req.src_ip = ret[0]
    req.dst_ip = ret[1]

    next_ip = get_next_hop(req.src_ip)
    previous_static_hop = db_service.get_previous_hop(key)
    if previous_static_hop is not None:
        next_ip = previous_static_hop
    Logger.logger.info('[Process Resv]: next_ip=' + next_ip + ', sender_ip=' + req.src_ip)

    is_sender = next_ip == req.src_ip
    callback = Callback(req, data, key)

    if is_class:
        req.speed = ret[2]
        req.tos = ret[3]
        Logger.logger.info('[Resv] Reservation request: src ip: ' + str(req.src_ip) + ', dst ip: ' + str(req.dst_ip) +
                           ', tos: ' + str(req.tos) + ', rate: ' + str(req.speed))
        if not any((req.src_ip, req.dst_ip, req.tos, req.speed)):
            error_msg = str(get_current_hop(req.src_ip)) + ': Error! Path is broken'
            error_o = Error(error_msg, 'resv')

            build_callback_error(callback, True, error_o)
            return callback
    else:
        error_msg = str(get_current_hop(req.src_ip)) + ret
        error_o = Error(error_msg, 'resv')

        build_callback_error(callback, not is_sender, error_o)
        return callback

    is_reserved, ret = reserve(key)
    Logger.logger.info('[Resv] : req_src ip: ' + str(req.src_ip) + ', src ip: ' + str(get_current_hop(req.src_ip)))
    if is_reserved:
        Logger.logger.info('Reservation success')
        build_callback(callback, is_reserved, not is_sender, 'Resv', req.src_ip)

    else:
        Logger.logger.info('Reservation failed')
        error_msg = str(get_current_hop(req.src_ip)) + ret
        error_o = Error(error_msg, 'resv')
        callback.error = error_o

    return callback


def process_resv_tear(data):
    Logger.logger.info('Processing ResvTear Message. . .')
    key = get_layer(data, Const.CL_MSG_ID).getfieldval('Data')
    is_class, ret = get_class(key, True)
    Logger.logger.info('is_class ' + str(is_class) + ' ret ' + str(ret))

    req = ReservationRequest.Instance()
    req.src_ip = ret[0]
    req.dst_ip = ret[1]
    req.speed = ret[2]
    req.tos = ret[3]

    previous_static_hop = db_service.get_previous_hop(key)
    is_destroyed, ret = remove_reserve(key)

    Logger.logger.info('[ResvTear] Destroying request: src ip: ' + str(req.src_ip) + ', dst ip: ' + str(req.dst_ip) +
                       ', tos: ' + str(req.tos) + ', rate: ' + str(req.speed))

    next_ip = get_next_hop(req.src_ip)
    if previous_static_hop is not None:
        next_ip = previous_static_hop

    is_sender = next_ip == req.src_ip
    callback = Callback(req, data, key)

    if is_destroyed:
        Logger.logger.info('Destroying completed successfully')
        build_callback(callback, is_destroyed, not is_sender, 'ResvTear', req.src_ip)
    else:
        Logger.logger.info('Destroying failed')
        error_msg = str(get_current_hop(req.src_ip)) + ': Error! Destroying failed ' + ret
        error_o = Error(error_msg, 'resv')
        build_callback_error(callback, not is_sender, error_o)

    return callback
