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
    output = check_output(['ip', 'route', 'get', ip_src]).split()
    if output[1] == 'via':
        device_name = output[4]
    else:
        device_name = output[2]

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
    output = check_output(['ip', 'route', 'get', ip_dst]).split()
    if output[1] == 'via':
        return output[2]
    else:
        return output[0]


def get_current_hop(ip_dst):
    output = check_output(['ip', 'route', 'get', ip_dst]).split()
    if output[0] == 'local':
        return output[5]
    elif output[1] == 'via':
        return output[6]
    else:
        return output[4]


def send_next_hop(ip, data, msg_type):
    src_ip = get_current_hop(ip)
    ip = get_next_hop(ip)
    Logger.logger.info('Passing ' + msg_type + ' message to next hop: ' + ip)
    data.getlayer('IP').setfieldval('dst', ip)
    data.getlayer('IP').setfieldval('src', src_ip)
    del data.chksum
    data = data.__class__(str(data))
    data.show2()
    send(data)


def get_sendtemp_data(data):
    src_ip = None
    dst_ip = None
    sendtemp_layer = get_layer(data, Const.CL_SENDTEMP)
    sendtemp_data = sendtemp_layer.getfieldval('Data')
    if int(sendtemp_data[0]) == 1:
        src_ip = sendtemp_data[1:16].lstrip('0')
    if int(sendtemp_data[16]) == 1:
        dst_ip = sendtemp_data[17:32].lstrip('0')

    return {'src': src_ip, 'dst': dst_ip}


def get_adspec_data(data):
    tos = None
    req_speed = None
    adspec_layer = get_layer(data, Const.CL_ADSPEC)
    adspec_data = adspec_layer.getfieldval('Data')
    if int(adspec_data[0]) == 1:
        tos = adspec_data[1:3].lstrip('0')
    if int(adspec_data[3]) == 1:
        req_speed = adspec_data[4:10].lstrip('0')

    return {'tos': tos, 'speed': req_speed}
