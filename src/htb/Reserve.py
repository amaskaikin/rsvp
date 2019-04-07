# Reserve resources
from src.utils.Const import Const
from DbService import DbService
from src.utils.Utils import *

db_service = DbService()


def check_reserve(request):
    device = get_device_instance(request.src_ip)
    is_available, key = device.reservation_is_available(request.src_ip, request.dst_ip, request.speed, request.tos)
    if is_available:
        db_service.insert_request_data(key, request)
    return is_available, key


def reserve(key):
    src_ip = db_service.get_request_data(key)[DbService.DB_SRC_IP]
    if not is_path_enabled(key):
        return False, Const.ERRORS[7]
    device = get_device_instance(src_ip)
    return device.call_htb(key)


def mark_destroy_path(request):
    device = get_device_instance(request.src_ip)
    is_valid_path, key = device.is_valid_path(request.src_ip, request.dst_ip, request.speed, request.tos)
    if is_valid_path:
        db_service.update_path_state(key, False)
    return is_valid_path, key


def remove_reserve(key):
    request_data = db_service.get_request_data(key)
    src_ip = request_data[DbService.DB_SRC_IP]
    if is_path_enabled(key):
        return False, Const.ERRORS[7]
    device = get_device_instance(src_ip)
    return device.remove(key)


def get_class(key):
    src_ip = db_service.get_request_data(key)[DbService.DB_SRC_IP]
    device = get_device_instance(src_ip)
    return device.get_htb_class(key)


def is_path_enabled(key):
    path_enabled = db_service.get_request_data(key)[DbService.DB_PATH_ENABLED]
    return path_enabled
