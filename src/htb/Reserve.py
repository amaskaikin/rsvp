# Reserve resources

from src.utils.Utils import *


def check_reserve(request):
    device = get_device(request.src_ip)
    return device.reservation_is_available(request.src_ip, request.dst_ip, request.speed, request.tos)


def reserve(key):
    src_ip = parse_unique_key(key)
    device = get_device(src_ip)
    return device.call_htb(key)


# def remove_reserve(request):
#    device = get_device(request.src_ip)
