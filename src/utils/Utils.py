from subprocess import check_output
from src.htb.Resources import Resources
from .Logger import *
from scapy.all import *
import re


def format_address(ip):
    return ip.zfill(15)


def format_route(route):
    formatted_route = []
    if not route:
        return None
    for ip in route:
        formatted_route.append(format_address(ip))

    return formatted_route


def get_device_instance(next_hop):
    # get singleton instance
    resources = Resources.Instance()

    # get device's name
    output = check_output(['ip', 'route', 'get', next_hop]).split()

    if output[0] == 'local':
        device_name = output[3]
    elif output[1] == 'via':
        device_name = output[4]
    else:
        device_name = output[2]

    # workaround
    if device_name == 'lo':
        device_name = 'enp0s3'

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


def send_next_hop(ip, data, msg_type, is_static):
    src_ip = get_current_hop(ip)
    Logger.logger.info('src' + src_ip)
    if not is_static:
        ip = get_next_hop(ip)
    Logger.logger.info('dst' + ip)
    Logger.logger.info('Passing ' + msg_type + ' message to next hop: ' + ip)
    data.getlayer('IP').setfieldval('dst', ip)
    data.getlayer('IP').setfieldval('src', src_ip)
    del data.chksum
    data = data.__class__(str(data))
    data.show2()
    send(data)


def parse_unique_key(key):
    return re.findall(r'[0-9]+(?:\.[0-9]+){3}', key)[0]
