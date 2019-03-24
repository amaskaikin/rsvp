from src.utils.Const import Const
from src.utils.Utils import format_route


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


def get_adspec_data(data):
    tos = None
    req_speed = None
    adspec_layer = get_layer(data, Const.CL_ADSPEC)
    if adspec_layer is None:
        return None
    adspec_data = adspec_layer.getfieldval('Data')
    if int(adspec_data[0]) == 1:
        tos = adspec_data[1:3].lstrip('0')
    if int(adspec_data[3]) == 1:
        req_speed = adspec_data[4:12].lstrip('0')

    return {'tos': tos, 'speed': req_speed}


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
    scope_layer = get_layer(data, Const.CL_ROUTE)
    packed_route = {'Data': '1' + '1'.join(format_route(static_route))}
    scope_layer.setfieldval('Data', packed_route)

    return data
