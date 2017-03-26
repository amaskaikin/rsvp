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
    else:
        return output[4]


def send_next_hop(ip, data, msg_type):
    ip = get_next_hop(ip)
    Logger.logger.info('Passing ' + msg_type + ' message to next hop: ' + ip)
    data.getlayer('IP').setfieldval('dst', ip)
    get_layer(data, Const.CL_SESSION).setfieldval('Data', ip)
    data.getlayer('HOP').setfieldval('neighbor', get_current_hop(ip))
    send(data)

