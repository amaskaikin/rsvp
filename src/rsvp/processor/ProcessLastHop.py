from src.htb.Reserve import reserve
from src.rsvp.generator.GenerateRSVP import generate_resv_tear
from src.rsvp.model.CallbackCommands import CallbackCommands
from src.rsvp.model.Error import Error
from src.utils.Logger import Logger
from src.utils.Utils import get_current_hop
from src.utils.Utils import get_next_hop


def process_path_last_hop(req, data, key):
    Logger.logger.info('Processing Last Path Hop. . .')
    Logger.logger.info('Parameters - src_ip: ' + req.src_ip +
                           ', dst ip: ' + req.dst_ip +
                           ', tos: ' + str(req.tos) + ', rate: ' + str(req.speed))
    is_reserved, ret = reserve(key)
    if is_reserved:
        Logger.logger.info('Reservation success')
        ip = get_next_hop(req.src_ip)
        src_ip = get_current_hop(req.src_ip)
        data.getlayer('IP').setfieldval('dst', ip)
        data.getlayer('IP').setfieldval('src', src_ip)
        return None, CallbackCommands.GENERATE_RESV
    else:
        Logger.logger.info('Reservation failed for request: src ip: ' + req.src_ip +
                           ', dst ip: ' + req.dst_ip +
                           ', tos: ' + str(req.tos) + ', rate: ' + str(req.speed))
        error_msg = str(get_current_hop(req.src_ip)) + ret
        error_o = Error(error_msg, 'resv')
        return error_o, CallbackCommands.SEND_ERROR


def process_resv_last_hop(req, data, key):
    Logger.logger.info('is reserved ' + str(reserve(key)[0]))
    Logger.logger.info('Resv message reached the sender.')
    Logger.logger.info('Full Reservation completed successfully')
    return None, CallbackCommands.NONE


def process_patherr_last_hop(req, data, key):
    Logger.logger.info('PathErr message reached the sender')
    return None, CallbackCommands.NONE


def process_resverr_last_hop(req, data, key):
    Logger.logger.info('ResvErr message reached the sender')
    return None, CallbackCommands.NONE


def process_pathtear_last_hop(req, data, key):
    Logger.logger.info('Processing Last PathTear Hop. . .')
    # TODO: call destroy method
    is_destroyed, ret = reserve(req)
    req_id = key
    if is_destroyed:
        Logger.logger.info('Destroyed successfully')
        ip = get_next_hop(req.src_ip)
        src_ip = get_current_hop(req.src_ip)
        data.getlayer('IP').setfieldval('dst', ip)
        data.getlayer('IP').setfieldval('src', src_ip)
        generate_resv_tear(data, req_id)
    else:
        Logger.logger.info('Destroying failed for request: src ip: ' + req.src_ip +
                           ', dst ip: ' + req.dst_ip +
                           ', tos: ' + str(req.tos) + ', rate: ' + str(req.speed))