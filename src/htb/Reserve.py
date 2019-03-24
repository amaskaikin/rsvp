# Reserve resources
from DbService import DbService
from src.utils.Utils import *

db_service = DbService()


def check_reserve(request):
    device = get_device_instance(request.src_ip)
    is_available, key = device.reservation_is_available(request.src_ip, request.dst_ip, request.speed, request.tos)
    db_service.insert_request_data(key, request)
    return is_available, key


def reserve(key):
    src_ip = db_service.get_request_data(key)[DbService.DB_SRC_IP]
    device = get_device_instance(src_ip)
    return device.call_htb(key)


def remove_reserve(key):
    src_ip = db_service.get_request_data(key)[DbService.DB_SRC_IP]
    device = get_device_instance(src_ip)
    return device.remove(key)


def get_class(key):
    src_ip = db_service.get_request_data(key)[DbService.DB_SRC_IP]
    device = get_device_instance(src_ip)
    return device.get_htb_class(key)
