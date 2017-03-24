# System resources class

from subprocess import call
from src.utils.Const import *


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


class Device:
    def __init__(self, name):
        self.name = name
        self.bandwidth = Const.BANDWIDTH
        self.temp_classes = []
        self.available_classes_ids = {'10': 'free', '20': 'free', '30': 'free',
                                      '40': 'free', '50': 'free', '60': 'free',
                                      '70': 'free', '80': 'free', '90': 'free'}
        call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.name,
              'root', 'handle', '1:', 'htb', 'default', 12])
        call(['sudo', 'tc', 'class', 'add', 'dev', self.name,
              'parent', '1:', 'classid', '1:1', 'htb', 'rate', str(self.bandwidth) + 'kbps'])

    def get_available_class_id(self):
        class_id = '0'
        for key, value in self.available_classes_ids:
            if value == 'free':
                self.available_classes_ids[key] = 'busy'
                class_id = key
                break
        return class_id

    def bandwidth_is_available(self, new_rate):
        new_bandwidth = self.bandwidth - new_rate
        if new_bandwidth > 0:
            self.bandwidth = new_bandwidth
            return True
        else:
            return False

    def reservation_is_available(self, request):
        class_id = self.get_available_class_id()
        if self.bandwidth_is_available(request.rate) and class_id != '0':
            new_class = Class(class_id, request.ip_src, request.ip_dst, request.rate, request.tos)
            self.temp_classes.append(new_class)
            return True
        else:
            return False

    def call_htb(self, request):
        # check and remove temp class
        htb_class = 0
        for htb_class in self.temp_classes:
            if (htb_class.ip_src == request.ip_src
               and htb_class.ip_dst == request.ip_dst
               and htb_class.rate == request.rate
               and htb_class.tos == request.tos):
                self.temp_classes.remove(htb_class)
                break
            else:
                return False

        # call htb cmd
        call(['sudo', 'tc', 'class', 'add', 'dev', self.name,
              'parent', '1:1', 'classid', htb_class.class_id, 'htb', 'rate', str(htb_class.rate)])
        call(['sudo', 'tc', 'filter', 'add', 'dev', self.name,
              'parent', '1:', 'protocol', 'ip', 'prio', '1', 'u32',
              'match', 'ip', 'tos', htb_class.tos, 'flowid', htb_class.class_id])
        # call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.name,
        #       'parent', class_id, 'handle', '20:', 'pfifo', 'limit', '5'])
        return True


class Class:
    def __init__(self, class_id, ip_src, ip_dst, rate, tos):
        self.class_id = class_id
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.rate = rate
        self.tos = tos
