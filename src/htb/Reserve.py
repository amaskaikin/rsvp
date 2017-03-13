# Reserve resources

from Resources import Resources


def reserve(device, class_id, rate, tos):
    # create resources (TODO: do it in daemon)
    resources = Resources()

    if Resources.device_exists(device):
        # get device
        device = resources.get_device(device)
    else:
        # add and get device
        resources.add_device(device)
        device = resources.get_device(device)

    device.add_class(class_id, rate, tos)
