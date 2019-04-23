import time
import re
from subprocess import check_output

from src.rsvp.generator.GenerateRSVP import generate_path, PathRSVP
from src.htb.Reserve import check_reserve
from src.utils.Logger import *
from src.utils.Utils import get_next_hop
from src.utils.RSVPDataHelper import get_route_data
from src.rsvp.generator.GenerateRSVP import generate_path_tear

from src.db.DbService import DbService

TC_COMMAND = ["tc", "-s", "-d", "class", "show", "dev"]
HTB_PATTERN = r'htb 1:'
HTB_SENT_PATTERN = r'.*rate\s(\d+)'
DIFF_KEY = "diff"
ADJUST_COEFFICIENT = 0.2


def generate_path_ab(init_request, data):
    dst_ip = get_next_hop(init_request.dst_ip)
    static_route_obj = get_route_data(data)
    path_pkt = PathRSVP(init_request.src_ip, init_request.dst_ip, init_request.tos,
                        init_request.speed, route=static_route_obj)
    is_available, key = check_reserve(init_request)
    if is_available:
        generate_path(path_pkt, dst_ip)
    else:
        Logger.logger.info("ABService.generate_path_ab: Required bw is unavailable for" + key)


class ABService:
    def __init__(self, ab_instance, db_instance):
        self.ab_instance = ab_instance
        self.db_instance = db_instance
        self.initial_measurements = {}
        self.measurements = {}
        self.reserved_data = {}

    def process_autobandwidth(self):
        start = time.time()
        time.clock()
        elapsed = 0
        self.reserved_data = self.db_instance.get_all_reserved_interfaces()
        while elapsed < self.ab_instance.adjust_interval:
            elapsed = round(time.time() - start)
            # print "loop cycle time: %f, seconds count: %02d" % (time.clock(), elapsed)
            self.calculate_diff()
            time.sleep(self.ab_instance.statistics_interval)
            print("elapsed: " + str(elapsed))
        self.update_tunnels()
        # wait for tunnel rebuilding
        time.sleep(self.ab_instance.adjust_interval)
        self.process_autobandwidth()

    def update_tunnels(self):
        for data in self.reserved_data:
            avg_diff = self.calculate_average_diff(data[DIFF_KEY])
            # print("avg_diff: " + str(avg_diff))
            key = data[DbService.DB_KEY]
            Logger.logger.info("ABService: avg_diff = " + str(avg_diff))
            if avg_diff > self.ab_instance.adjust_threshold:
                # decrease bw
                Logger.logger.info("ABService: decrease bw for " + key + " by " +
                                   str(self.ab_instance.adjust_threshold))
                self.db_instance.update_path_state(key, False)
                path_req = self.db_instance.get_request_data(key)
                new_bw = int(path_req[DbService.DB_SPEED]) - self.ab_instance.adjust_threshold
                # path_req[DbService.DB_SPEED] -= self.ab_instance.adjust_threshold
                generate_path_tear(path_tear=path_req, is_autobandwidth=True, new_bw=new_bw)

            elif avg_diff < self.ab_instance.adjust_threshold * ADJUST_COEFFICIENT:
                # increase bw
                Logger.logger.info("ABService: increase bw for " + key + " by " +
                                   str(self.ab_instance.adjust_threshold))

    def calculate_diff(self):
        for data in self.reserved_data:
            actual_rate = self.get_actual_rate(data[DbService.DB_RESERVED_INTERFACE], data[DbService.DB_RESERVED_CLASS])
            diff = int(data[DbService.DB_SPEED]) - int(actual_rate)
            if DIFF_KEY not in data:
                data[DIFF_KEY] = [diff]
            else:
                data[DIFF_KEY].append(diff)

    def get_actual_rate(self, iface, class_id):
        command = TC_COMMAND[:]
        command.append(iface)
        output = check_output(command)
        for chunk in output.split("\n\n"):
            htb_pattern = HTB_PATTERN + class_id
            if re.search(htb_pattern, chunk):
                rate_line = chunk.splitlines()[2]
                return int(re.search(HTB_SENT_PATTERN, rate_line).group(1))

        return -1

    def calculate_average_diff(self, list_diff):
        return sum(list_diff) / float(len(list_diff))
