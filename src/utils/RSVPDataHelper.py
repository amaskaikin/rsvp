from src.utils.Const import Const
from src.utils.Utils import format_route, Logger


def get_layer(data, pclass):
    cnt = 0
    while True:
        layer = data.getlayer(cnt)
        if layer is not None:
            if layer.name == 'RSVP_Object':
                if layer.getfieldval('Class') == pclass:
                    return data.getlayer(++cnt)
        else:
            break
        cnt += 1


def get_sendtemp_data(data):
    src_ip = None
    dst_ip = None
    ifaces = []
    sendtemp_layer = get_layer(data, Const.CL_SENDTEMP)
    if sendtemp_layer is None:
        return None
    sendtemp_data = sendtemp_layer.getfieldval('Data')
    if int(sendtemp_data[0]) == 1:
        src_ip = sendtemp_data[1:16].lstrip('0')
    if int(sendtemp_data[16]) == 1:
        dst_ip = sendtemp_data[17:32].lstrip('0')

    ifaces_data = sendtemp_data[33:]
    iface = ""
    for i in range(0, len(ifaces_data)):
        if int(ifaces_data[i]) == 1 and iface:
            ifaces.append(iface)
            iface = None
            continue
        iface += ifaces_data[i]

    return {'src': src_ip, 'dst': dst_ip, 'ifaces': ifaces}


def get_spec_data(data, spec=Const.CL_ADSPEC):
    tos = None
    req_speed = None
    ab_rate = None
    adspec_layer = get_layer(data, spec)
    if adspec_layer is None:
        return None
    adspec_data = adspec_layer.getfieldval('Data')
    if int(adspec_data[0]) == 1:
        tos = adspec_data[1:3].lstrip('0')
    if int(adspec_data[3]) == 1:
        req_speed = adspec_data[4:12].lstrip('0')
    if len(adspec_data) > 12 and int(adspec_data[12]) == 1:
        ab_rate = adspec_data[13:21].lstrip('0')

    return {'tos': tos, 'speed': req_speed, 'ab_rate': ab_rate}


def get_route_data(data):
    static_route = []
    scope_layer = get_layer(data, Const.CL_ROUTE)
    if scope_layer is None:
        return None
    scope_data = scope_layer.getfieldval('Data')
    for i in range(0, len(scope_data), 16):
        if int(scope_data[i]) == 1:
            static_route.append(scope_data[i+1:i+16].lstrip('0'))

    return {'static_route': static_route}


def set_route_data(data, static_route):
    rsvp_layer = data.getlayer('RSVP')
    scope_layer = get_layer(data, Const.CL_ROUTE)
    init_length = scope_layer.getfieldval('Length')

    formatted_route = format_route(static_route)
    packed_route = '1' + ('1'.join(formatted_route) if formatted_route else '')
    scope_layer.setfieldval('Data', packed_route)
    route_length = len(str(packed_route)) + 4

    new_length = rsvp_layer.getfieldval('Length') + (route_length - init_length)
    scope_layer.setfieldval('Length', route_length)
    rsvp_layer.setfieldval('Length', new_length)
    data.setfieldval('len', data.getfieldval('len') + (route_length - init_length))

    return data


def process_static_route(data, current_ip):
    is_valid_route = True
    static_route_obj = get_route_data(data)
    if static_route_obj is None:
        return data, is_valid_route, None

    static_route = static_route_obj.get('static_route')
    Logger.logger.info('[Process Static Route] static_route: ' + str(static_route) + ' current_ip: ' + current_ip)
    if current_ip in static_route:
        idx = static_route.index(current_ip)
        if idx == 0:
            static_route.remove(current_ip)
            data = set_route_data(data, static_route)
        else:
            Logger.logger.info('[Process Static Route] Error: static route is invalid')
            is_valid_route = False
    else:
        Logger.logger.info('[Process Static Route] Error: static route is invalid')
        is_valid_route = False

    return data, is_valid_route, static_route
