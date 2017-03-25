from scapy.all import *
from src.data.ReservationRequest import *
from src.utils.Utils import *
from src.utils.Const import *
from src.utils.Logger import Logger
from src.htb.Reserve import *


def process_path(data):
    Logger.logger.info('Processing Path Message. . .')
    res_req = get_reservation_info(data)
    is_available = check_reserve(res_req)
    is_last_hop = res_req.dst_ip == get_current_hop(res_req.dst_ip)
    # TODO: send error message
    if is_available is True:
        Logger.logger.info('Required bandwidth is available')

        if is_last_hop is False:
            send_next_hop(data)
        else:
            # TODO: if true, ask htb for reservation
            pass


def get_reservation_info(data):
    src_ip = None
    dst_ip = None
    tos = None
    req_speed = None
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

    Logger.logger.info('Reservation request: src ip - ' + src_ip + ' dst ip - ' + dst_ip +
                       'tos - ' + tos + ' rate - ' + req_speed)

    if not any((src_ip, dst_ip, tos, req_speed)):
        Logger.logger.info('Illegal values: src ip - ' + src_ip + ' dst ip - ' + dst_ip +
                           'tos - ' + tos + ' rate - ' + req_speed)

    res_req = ReservationRequest(src_ip, dst_ip, tos, int(req_speed))
    return res_req


def send_next_hop(data):
    # TODO: call function which returns next hop address
    ip = Const.TARGET_ADDRESS
    Logger.logger.info('Passing Path message to next hop: ' + ip)
    data.getlayer('IP').setfieldval('dst', ip)
    get_layer(data, Const.CL_SESSION).setfieldval('Data', '192.168.0.106')
    print get_layer(data, Const.CL_SESSION).getfieldval('Data')
    send(data)
