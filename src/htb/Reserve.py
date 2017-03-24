# Reserve resources

from Resources import Resources
from src.utils.Utils import *

# TODO: create resources in daemon
resources = Resources()
# TODO: get next hop in daemon
# next_hop = check_output(['ip', 'route', 'get', ip_dst]).split()[2]


def check_reserve(request):
    device = get_device(request.src_ip)
    return device.reservation_is_available(request)


def reserve(request):
    device = get_device(request.src_ip)
    return device.call_htb(request)
