from subprocess import check_output
from src.htb.Resources import Resources
# TODO: import variable resources from daemon


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


def get_device(ip_src):
    # get singleton instance
    resources = Resources.Instance()

    # get device's name
    device_name = check_output(['ip', 'route', 'get', ip_src]).split()[2]

    # get/add device
    if resources.device_exists(device_name):
        # get device
        device = resources.get_device(device_name)
    else:
        # add and get device
        resources.add_device(device_name)
        device = resources.get_device(device_name)

    return device
