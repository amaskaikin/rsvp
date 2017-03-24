# Reserve resources

from Resources import Resources
from utils import Utils

# TODO: create resources in daemon
resources = Resources()
# TODO: get next hop in daemon
# next_hop = check_output(['ip', 'route', 'get', ip_dst]).split()[2]


def check_reserve(ip_src, ip_dst, rate, tos):
    device = Utils.get_device(ip_src)
    return device.reservation_is_available(ip_src, ip_dst, rate, tos)


def reserve(ip_src, ip_dst, rate, tos):
    device = Utils.get_device(ip_src)
    return device.call_htb(ip_src, ip_dst, rate, tos)
