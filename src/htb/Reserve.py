# Reserve resources

from src.utils.Utils import *


def check_reserve(request):
    device = get_device(request.src_ip)
    return device.reservation_is_available(request.src_ip, request.dst_ip, request.speed, request.tos)


def reserve(request):
    device = get_device(request.src_ip)
    return device.call_htb(request.src_ip, request.dst_ip, request.speed, request.tos)


# def remove_reserve(request):
#    device = get_device(request.src_ip)
