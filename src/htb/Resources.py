# System resources class

from subprocess import call


class Resources:
    def __init__(self):
        self.devices = []

    def device_exists(self, name):
        for device in self.devices:
            if device.name == name:
                return True

    def add_device(self, name):
        new_device = Device(name)
        self.devices.append(new_device)

    def get_device(self, name):
        return next(device for device in self.devices if device.name == name)


class Class:
    def __init__(self, class_id, rate, tos):
        self.class_id = class_id
        self.rate = rate
        self.tos = tos


class Device:
    def __init__(self, name):
        self.name = name
        self.bandwidth = '100kbps'
        self.classes = []
        call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.name,
              'root', 'handle', '1:', 'htb', 'default', 12])
        call(['sudo', 'tc', 'class', 'add', 'dev', self.name,
              'parent', '1:', 'classid', '1:1', 'htb', 'rate', self.bandwidth])

    def class_exists(self, new_class_id):
        for htb_class in self.classes:
            if htb_class.class_id == new_class_id:
                return True

    def bandwidth_is_available(self, new_rate):
        new_rate = int(''.join(char for char in new_rate if char.isdigit()))
        old_bandwidth = int(''.join(char for char in self.bandwidth if char.isdigit()))
        new_bandwidth = old_bandwidth - new_rate
        if new_bandwidth > 0:
            self.bandwidth = str(new_bandwidth) + 'kbps' 
            return True
        else:
            return False

    def add_class(self, class_id, rate, tos):
        if self.bandwidth_is_available(rate) and not self.class_exists(class_id):
            call(['sudo', 'tc', 'class', 'add', 'dev', self.name,
                  'parent', '1:1', 'classid', class_id, 'htb', 'rate', rate])
            call(['sudo', 'tc', 'filter', 'add', 'dev', self.name,
                  'parent', '1:', 'protocol', 'ip', 'prio', '1', 'u32',
                  'match', 'ip', 'tos', tos, 'flowid', class_id])
            # call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.name,
            #       'parent', class_id, 'handle', '20:', 'pfifo', 'limit', '5'])
            new_class = Class(class_id, rate, tos)
            self.classes.append(new_class)
