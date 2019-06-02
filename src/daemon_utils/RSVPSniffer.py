# Packet Modifier
from scapy.layers.inet import IP

from src.rsvp.generator.GenerateRSVP import generate_resv, generate_resv_tear
from src.rsvp.model.CallbackCommands import CallbackCommands
from src.rsvp.processor.ProcessLastHop import process_resv_last_hop, process_patherr_last_hop, \
    process_resverr_last_hop, process_path_last_hop, process_pathtear_last_hop, process_resvtear_last_hop
from src.rsvp.processor.ProcessPathMsg import *
from src.rsvp.processor.ProcessResvMsg import process_resv, process_resv_tear
from src.autobandwidth.AutoBandwidthService import generate_path_ab


def catch_packet():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RSVP)
    print("Socket created")
    try:
        while 1:
            print("Waiting...")
            pkt = sock.recv(2048)
            print("Received...")
            process_packet(pkt)

    except KeyboardInterrupt:
        print("The loop was interrupted. Sniffer exiting")


def process_packet(pkt):
    data = IP(pkt)
    rsvp_class = data.getlayer('RSVP').getfieldval('Class')
    if rsvp_class == 0x01:
        callback = process_path(data)
        process_callback(callback, lambda: process_path_last_hop(callback.request, callback.data, callback.key))
    if rsvp_class == 0x02:
        callback = process_resv(data)
        process_callback(callback, lambda: process_resv_last_hop(callback.request, callback.data, callback.key))
    if rsvp_class == 0x05:
        callback = process_path_tear(data)
        process_callback(callback, lambda: process_pathtear_last_hop(callback.request, callback.data, callback.key))
    if rsvp_class == 0x06:
        callback = process_resv_tear(data)
        process_callback(callback, lambda: process_resvtear_last_hop(callback.request, callback.data, callback.key))
    if rsvp_class == 0x03:
        callback = process_path_err(data)
        process_callback(callback, lambda: process_patherr_last_hop(callback.request, callback.data, callback.key))
    if rsvp_class == 0x04:
        callback = process_resv_err(data)
        process_callback(callback, lambda: process_resverr_last_hop(callback.request, callback.data, callback.key))


def process_callback(callback, lasthop_processor):
    Logger.logger.info('Process callback: ' + str(callback.request.src_ip) + ', result: ' + str(callback.result) +
                       ', is_next: ' + str(callback.is_next))
    if callback.result:
        if not callback.is_next:
            error_o, func = lasthop_processor()
            if error_o is not None:
                send_error(callback.request.src_ip, callback.data, error_o)
            else:
                execute_callback_command(callback, func)
        else:
            send_next_hop(callback.direction, callback.data, callback.next_label, callback.is_static)
    else:
        send_error(callback.request.src_ip, callback.data, callback.error)


def execute_callback_command(callback, func):
    if func == CallbackCommands.NONE:
        pass
    if func == CallbackCommands.GENERATE_RESV:
        generate_resv(callback.data, callback.key)
    if func == CallbackCommands.GENERATE_RESV_TEAR:
        generate_resv_tear(callback.data, callback.key)
    if func == CallbackCommands.GENERATE_PATH:
        generate_path_ab(callback.request, callback.data)
