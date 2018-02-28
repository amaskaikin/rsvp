from src.htb.Reserve import *
from src.rsvp.processor.ProcessErrMsg import *


def process_resv(data):
    Logger.logger.info('Processing Resv Message. . .')
    key = get_layer(data, Const.CL_MSG_ID).getfieldval('Data')
    req = ReservationRequest.Instance()
    is_class, ret = get_class(key)

    Logger.logger.info('is_class ' + str(is_class) + ' ret ' + str(ret))
    ip = data.getlayer(0).getfieldval('dst')
    is_sender = ip == req.src_ip
    callback = Callback(req, data, key)

    if is_class:     
        req.src_ip = ret[0]
        req.dst_ip = ret[1]
        req.tos = ret[2]
        req.speed = ret[3]
        Logger.logger.info('[Resv] Reservation request: src ip: ' + str(req.src_ip) + ', dst ip: ' + str(req.dst_ip) +
                           ', tos: ' + str(req.tos) + ', rate: ' + str(req.speed))
        
        if is_sender:
            callback.result = True
            callback.is_next = False
            return callback
        if not any((req.src_ip, req.dst_ip, req.tos, req.speed)):
            error_msg = str(get_current_hop(req.src_ip)) + ': Error! Path is broken'
            callback.result = False
            callback.is_next = True
            error_o = Error(error_msg, 'resv')
            callback.error = error_o
            return callback
    else:
        error_msg = str(get_current_hop(req.src_ip)) + ret
        callback.result = False
        callback.is_next = not is_sender
        error_o = Error(error_msg, 'resv')
        callback.error = error_o
        return callback

    is_reserved, ret = reserve(key)
    Logger.logger.info('[Resv] : req_src ip: ' + str(req.src_ip) + ', src ip: ' + str(get_current_hop(req.src_ip)))
    callback.result = is_reserved
    callback.is_next = not is_sender
    callback.next_label = 'Resv'
    callback.direction = req.src_ip
    if is_reserved:
        Logger.logger.info('Reservation success')
    else:
        Logger.logger.info('Reservation failed')
        error_msg = str(get_current_hop(req.src_ip)) + ret
        error_o = Error(error_msg, 'resv')
        callback.error = error_o

    return callback


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
