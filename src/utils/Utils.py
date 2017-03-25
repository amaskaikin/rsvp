from subprocess import check_output
from src.htb.Resources import Resources
from Const import *
from Logger import *
from src.data.ReservationRequest import *
from scapy.all import *


def get_layer(data, pclass):
    cnt = 0
    while True:
        layer = data.getlayer(cnt)
        if layer is not None:
            if layer.name == 'RSVP_Object':
                if layer.getfieldval('Class') == pclass:
                    return data.getlayer(++cnt)
        else:
            break
        cnt += 1


def get_device(ip_src):
    # get singleton instance
    resources = Resources.Instance()

    # get device's name
    device_name = check_output(['ip', 'route', 'get', ip_src]).split()[2]

    # get/add device
    if resources.device_exists(device_name):
        # get device
        device = resources.get_device(device_name)
    else:
        # add and get device
        resources.add_device(device_name)
        device = resources.get_device(device_name)

    return device


def get_next_hop(ip_dst):
    return check_output(['ip', 'route', 'get', ip_dst]).split()[0]


def get_current_hop(ip_dst):
    output = check_output(['ip', 'route', 'get', ip_dst]).split()
    if output[0] == 'local':
        return output[5]
    else:
        return output[4]


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


def send_next_hop(ip, data, msg_type):
    ip = get_next_hop(ip)
    Logger.logger.info('Passing + ' + msg_type + ' message to next hop: ' + ip)
    data.getlayer('IP').setfieldval('dst', ip)
    get_layer(data, Const.CL_SESSION).setfieldval('Data', ip)
    data.getlayer('HOP').setfieldval('neighbor', get_current_hop(ip))
    send(data)

