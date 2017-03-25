from scapy.all import *
from src.htb.Reserve import *
from src.rsvp.ProcessResvMsg import *


def process_path(data):
    Logger.logger.info('Processing Path Message. . .')
    res_req = get_reservation_info(data, 'Path')
    is_available = check_reserve(res_req)
    is_last_hop = res_req.dst_ip == get_current_hop(res_req.dst_ip)
    print is_last_hop
    # TODO: send error message
    if is_available:
        Logger.logger.info('Required bandwidth is available')

        if not is_last_hop:
            send_next_hop(res_req.dst_ip, data, 'Path')
        else:
            Logger.logger.info('Path message reached the last hop')
            process_last_hop(res_req, data)


def process_last_hop(req, data):
    Logger.logger.info('Processing Last Path Hop. . .')
    is_reserved = reserve(req)
    if is_reserved:
        Logger.logger.info('Reservation success')
        ip = get_next_hop(req.src_ip)
        data.getlayer('IP').setfieldval('dst', ip)
        get_layer(data, Const.CL_SESSION).setfieldval('Data', ip)
        get_layer(data, Const.CL_HOP)('neighbor', get_current_hop(ip))
        generate_resv(data)
