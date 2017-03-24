from src.data.ReservationRequest import *
from src.utils.Utils import *
from src.utils.Const import *


def process_path(data):
    res_req = get_reservation_info(data)
    # TODO: call htb method for checking available bandwidth
    is_available = False
    is_last_hop = False
    if is_available is True:
        if is_last_hop is False:
            push_path()



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

    if not any((src_ip, dst_ip, tos, req_speed)):
        print 'Illegal values'

    res_req = ReservationRequest(src_ip, dst_ip, tos, req_speed)
    return res_req

