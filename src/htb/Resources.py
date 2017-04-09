# System resources class

from subprocess import call
from src.utils.Const import *
from src.utils.Singleton import *
from src.utils.Utils import *


@Singleton
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
        self.classes = []
        self.available_classes_ids = {'10': 'free', '20': 'free', '30': 'free',
                                      '40': 'free', '50': 'free', '60': 'free',
                                      '70': 'free', '80': 'free', '90': 'free'}
        call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.name,
              'root', 'handle', '1:', 'htb', 'default', '12'])
        call(['sudo', 'tc', 'class', 'add', 'dev', self.name,
              'parent', '1:', 'classid', '1:1', 'htb', 'rate', str(self.bandwidth) + 'kbps'])

    def get_available_class_id(self):
        for key, value in self.available_classes_ids.iteritems():
            if value == 'free':
                self.available_classes_ids[key] = 'busy'
                return key
        return False

    def bandwidth_is_available(self, new_rate):
        new_bandwidth = self.bandwidth - new_rate
        if new_bandwidth > 0:
            self.bandwidth = new_bandwidth
            return True
        else:
            return False

    def class_exists(self, key):
        for htb_class in self.classes:
            if htb_class.key == key:
                return htb_class
        return False

    def class_reserved(self, key):
        for htb_class in self.classes:
            if htb_class.key == key:
                return htb_class.reserved
        return False

    def reservation_is_available(self, ip_src, ip_dst, rate, tos):
        key = generate_unique_key(ip_src, ip_dst, rate, tos)
        if not self.bandwidth_is_available(rate) or self.class_reserved(key):
            return False, None
        class_id = self.get_available_class_id()
        if class_id:
            key = generate_unique_key(ip_src, ip_dst, rate, tos)
            new_class = Class(key, class_id, ip_src, ip_dst, rate, tos)
            self.classes.append(new_class)
            return True, key
        else:
            return False, None

    def call_htb(self, key):
        htb_class = self.class_exists(key)
        if not htb_class or htb_class.reserved:
            return False

        # make class reserved
        htb_class.reserved = True

        # call htb cmd
        call(['sudo', 'tc', 'class', 'add', 'dev', self.name,
              'parent', '1:1', 'classid', htb_class.class_id, 'htb', 'rate', str(htb_class.rate)])
        call(['sudo', 'tc', 'filter', 'add', 'dev', self.name,
              'parent', '1:', 'protocol', 'ip', 'prio', '1', 'u32',
              'match', 'ip', 'tos', htb_class.tos, 'flowid', htb_class.class_id])
        # call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.name,
        #       'parent', class_id, 'handle', '20:', 'pfifo', 'limit', '5'])
        return True

    # def remove(self, ip_src, ip_dst, rate, tos):


class Class:
    def __init__(self, key, class_id, ip_src, ip_dst, rate, tos):
        self.key = key
        self.class_id = class_id
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.rate = rate
        self.tos = tos
        self.reserved = False
