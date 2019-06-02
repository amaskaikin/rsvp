from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage
from src.utils.Singleton import *


@Singleton
class DbInstance:
    def __init__(self):
        print("init dbservice")
        self.db_service = DbService()

    @property
    def db_service(self):
        print("get dbservice")
        return self.db_service

    @db_service.setter
    def db_service(self, value):
        self._db_service = value


class DbService:
    DB_KEY = 'key'
    DB_SRC_IP = 'src_ip'
    DB_DST_IP = 'dst_ip'
    DB_SPEED = 'speed'
    DB_TOS = 'tos'
    DB_PATH_ENABLED = 'path_enabled'
    DB_RESERVED_INTERFACE = 'reserved_iface'
    DB_RESERVED_CLASS = 'reserved_class'
    DB_FROM_IP = 'current_ip'

    def __init__(self):
        self.db_instance = TinyDB(storage=MemoryStorage).table()

    def insert_request_data(self, key, request):
        self.db_instance.insert({self.DB_KEY: key, self.DB_SRC_IP: request.src_ip, self.DB_DST_IP: request.dst_ip,
                                 self.DB_SPEED: request.speed, self.DB_TOS: request.tos, self.DB_PATH_ENABLED: True})
        return key

    def get_request_data(self, key):
        return self.db_instance.search(where(self.DB_KEY) == key)[0]

    def update_reserved_iface(self, key, iface, class_id):
        self.db_instance.update({self.DB_RESERVED_INTERFACE: iface, self.DB_RESERVED_CLASS: class_id},
                                where(self.DB_KEY) == key)

    def remove_request_data(self):
        pass  # TODO: implement remove

    def update_path_state(self, key, path_enabled):
        self.db_instance.update({self.DB_PATH_ENABLED: path_enabled}, where(self.DB_KEY) == key)

    def insert_reserved_interface(self, interface, key):
        self.db_instance.insert({self.DB_RESERVED_INTERFACE: interface, self.DB_RESERVED_CLASS: key})

    def remove_reserved_info(self, key):
        self.db_instance.remove(where(self.DB_KEY) == key)

    def get_all_reserved_interfaces(self):
        return self.db_instance.search(where(self.DB_RESERVED_INTERFACE))

    def get_reserved_interface_request(self, interface):
        key = self.db_instance.search(where(self.DB_RESERVED_INTERFACE) == interface)
        return self.get_request_data(key)

    def get_previous_hop(self, key):
        data = self.get_request_data(key)
        if self.DB_FROM_IP in data:
            return data[self.DB_FROM_IP]
        else:
            return None

    def set_previous_hop(self, key, src_ip):
        self.db_instance.update({self.DB_FROM_IP: src_ip}, where(self.DB_KEY) == key)

    def flush(self):
        self.db_instance.purge()
