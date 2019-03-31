from src.data.ReservationRequest import ReservationRequest
from src.rsvp.generator.GenerateRSVP import generate_path_err, generate_resv_err
from src.rsvp.model.Callback import Callback
from src.rsvp.model.Error import Error
from src.utils.Const import Const
from src.utils.RSVPDataHelper import get_sendtemp_data, get_layer
from src.utils.Utils import *


def process_path_err(data):
    Logger.logger.info('Processing PathErr Message. . .')
    dst_ip = get_sendtemp_data(data).get('src')
    Logger.logger.info('Processing PathErr Message. . . DST_IP ' + str(dst_ip))
    req = ReservationRequest.Instance()

    Logger.logger.info('Processing PathErr Message. . . REQ SRC IP' + str(req.src_ip))
    Logger.logger.info('Processing PathErr Message. . . REQ DST IP' + str(req.dst_ip))

    is_last_hop = dst_ip == get_current_hop(dst_ip)
    Logger.logger.info('Processing PathErr Message. . . IS_LAST_HOP ' + str(is_last_hop))

    err_spec = get_layer(data, Const.CL_ERRSPEC).getfieldval('Data')
    Logger.logger.info('[PathErr] Path Error: ' + str(err_spec))
    error_o = Error(err_spec, 'path')
    callback = Callback(request=req, data=data, result=True, is_next=not is_last_hop, next_label='PathErr',
                        direction=dst_ip, error=error_o)

    return callback


def process_resv_err(data):
    Logger.logger.info('Processing ResvErr Message. . .')
    dst_ip = data.getlayer(0).getfieldval('dst')
    Logger.logger.info('Processing ResvErr Message. . . DST_IP ' + str(dst_ip))
    req = ReservationRequest.Instance()

    Logger.logger.info('Processing ResvErr Message. . . REQ SRC IP' + str(req.src_ip))
    Logger.logger.info('Processing ResvErr Message. . . REQ DST IP' + str(req.dst_ip))

    is_sender = dst_ip == get_current_hop(dst_ip)
    Logger.logger.info('Processing ResvErr Message. . . IS_SENDER ' + str(is_sender))
    err_spec = get_layer(data, Const.CL_ERRSPEC).getfieldval('Data')
    Logger.logger.info('[ResvErr] Reservation Error: ' + str(err_spec))
    error_o = Error(err_spec, 'resv')

    callback = Callback(request=req, data=data, result=True, is_next=is_sender, next_label='ResvErr',
                        direction=dst_ip, error=error_o)

    return callback


def send_error(ip, data, err):
    msg = err.err_msg
    msg_type = err.err_label
    Logger.logger.info('[send_error] ' + ip)
    src_ip = get_current_hop(ip)
    ip = get_next_hop(ip)
    Logger.logger.info('Sending error' + msg_type + ' message to next hop: ' + ip)
    data.getlayer('IP').setfieldval('dst', ip)
    data.getlayer('IP').setfieldval('src', src_ip)
    del data.chksum
    data = data.__class__(str(data))
    if msg_type == 'path':
        generate_path_err(data, msg)
    else:
        generate_resv_err(data, msg)
