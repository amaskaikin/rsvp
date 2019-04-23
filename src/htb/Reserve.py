# Reserve resources
from src.utils.Const import Const
from src.db.DbService import DbService, DbInstance
from src.utils.Utils import *

db_service = DbInstance.Instance().db_service


def check_reserve(request):
    device = get_device_instance(request.dst_ip)
    is_available, key = device.reservation_is_available(request.src_ip, request.dst_ip, request.speed, request.tos)
    if is_available:
        db_service.insert_request_data(key, request)
    return is_available, key


def reserve(key):
    dst_ip = db_service.get_request_data(key)[DbService.DB_DST_IP]
    if not is_path_enabled(key):
        return False, Const.ERRORS[7]
    device = get_device_instance(dst_ip)
    result, ret, class_id = device.call_htb(key)
    db_service.update_reserved_iface(key, device.name, class_id)
    return result, ret


def mark_destroy_path(request):
    device = get_device_instance(request.dst_ip)
    is_valid_path, key = device.is_valid_path(request.src_ip, request.dst_ip, request.speed, request.tos)
    if is_valid_path:
        db_service.update_path_state(key, False)
    return is_valid_path, key


def remove_reserve(key):
    request_data = db_service.get_request_data(key)
    dst_ip = request_data[DbService.DB_DST_IP]
    if is_path_enabled(key):
        return False, Const.ERRORS[7]
    device = get_device_instance(dst_ip)
    db_service.remove_reserved_info(key)

    return device.remove(key)


def get_class(key, is_destroy=False):
    dst_ip = db_service.get_request_data(key)[DbService.DB_DST_IP]
    device = get_device_instance(dst_ip)
    if is_destroy:
        return device.get_htb_class_for_destroy(key)
    return device.get_htb_class(key)


def is_path_enabled(key):
    path_enabled = db_service.get_request_data(key)[DbService.DB_PATH_ENABLED]
    return path_enabled
