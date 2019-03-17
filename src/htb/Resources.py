# System resources class

from subprocess import call

from src.utils.Const import *
from src.utils.Singleton import *
from src.utils.Logger import *


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
              'parent', '1:', 'classid', '1:1', 'htb', 'rate', str(self.bandwidth)])

    def get_available_class_id(self):
        for key, value in self.available_classes_ids.items():
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
        return None

    def class_reserved(self, key):
        for htb_class in self.classes:
            if htb_class.key == key:
                return htb_class.reserved
        return None

    @staticmethod
    def generate_unique_key(ip_src, ip_dst, rate, tos):
        return '_'.join([ip_src, ip_dst, str(rate), str(tos)])

    def reservation_is_available(self, ip_src, ip_dst, rate, tos):
        key = self.generate_unique_key(ip_src, ip_dst, rate, tos)
        
        # stub for testing PathErr
        # return False, key

        # errors
        if not self.bandwidth_is_available(rate):
            return False, Const.ERRORS[1]
        if self.class_reserved(key) is not None:
            return False, Const.ERRORS[2]
        class_id = self.get_available_class_id()
        if not class_id:
            return False, Const.ERRORS[3]

        # create class
        key = self.generate_unique_key(ip_src, ip_dst, rate, tos)
        new_class = Class(key, class_id, ip_src, ip_dst, rate, tos)
        self.classes.append(new_class)
        return True, key

    def get_htb_class(self, key):
        htb_class = self.class_exists(key)

        # errors
        if htb_class is None:
            return False, Const.ERRORS[4]
        if htb_class.reserved:
            return False, Const.ERRORS[5]

        return True, [htb_class.ip_src, htb_class.ip_dst, htb_class.rate, htb_class.tos]

    def call_htb(self, key):
        htb_class = self.class_exists(key)

        # stub for testing ResvErr
        # return False, Const.ERRORS[4]
        
        # errors
        if htb_class is None:
            return False, Const.ERRORS[4]
        if htb_class.reserved:
            return False, Const.ERRORS[5]

        # make class reserved
        htb_class.reserved = True
        
        Logger.logger.info(str(htb_class.class_id) + ' ' + str(htb_class.tos))
        flowid = '1:' + str(htb_class.class_id)
        # call htb cmd
        call(['sudo', 'tc', 'class', 'add', 'dev', self.name,
              'parent', '1:1', 'classid', htb_class.class_id, 'htb', 'rate', str(htb_class.rate)])
        call(['sudo', 'tc', 'filter', 'add', 'dev', self.name,
              'parent', '1:', 'protocol', 'ip', 'prio', '1', 'u32',
              'match', 'ip', 'tos', hex(int(htb_class.tos)), '0xff', 'flowid', flowid])
        # call(['sudo', 'tc', 'qdisc', 'add', 'dev', self.name,
        #       'parent', class_id, 'handle', '20:', 'pfifo', 'limit', '5'])

        return True, [htb_class.ip_src, htb_class.ip_dst, htb_class.rate, htb_class.tos]

    def remove(self, key):
        htb_class = self.class_exists(key)

        # errors
        if htb_class is None:
            return False, Const.ERRORS[4]
        if not htb_class.reserved:
            return False, Const.ERRORS[6]

        # make class unreserved
        htb_class.reserved = False

        # call htb cmd
        call(['sudo', 'tc', 'class', 'del', 'dev', self.name,
              'parent', '1:1', 'classid', htb_class.class_id])

        return True, ''


class Class:
    def __init__(self, key, class_id, ip_src, ip_dst, rate, tos):
        self.key = key
        self.class_id = class_id
        self.ip_src = ip_src
        self.ip_dst = ip_dst
        self.rate = rate
        self.tos = tos
        self.reserved = False
