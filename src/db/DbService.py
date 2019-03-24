from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage


class DbService:
    DB_KEY = 'key'
    DB_SRC_IP = 'src_ip'
    DB_DST_IP = 'dst_ip'
    DB_SPEED = 'speed'
    DB_TOS = 'tos'

    def __init__(self):
        self.db_instance = TinyDB(storage=MemoryStorage).table()

    def insert_request_data(self, key, request):
        self.db_instance.insert({self.DB_KEY: key, self.DB_SRC_IP: request.src_ip, self.DB_DST_IP: request.dst_ip,
                                 self.DB_SPEED: request.speed, self.DB_TOS: request.tos})
        return key

    def get_request_data(self, key):
        return self.db_instance.search(where(self.DB_KEY) == key)

    def flush(self):
        self.db_instance.purge()
