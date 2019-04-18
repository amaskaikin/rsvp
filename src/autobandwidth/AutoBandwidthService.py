import time
import re
from subprocess import check_output

from .TrafficDiffModel import TrafficDiff
from src.utils.Logger import *
from src.htb.Reserve import remove_reserve
from src.rsvp.generator.GenerateRSVP import generate_path_tear

from src.db.DbService import DbService, DbInstance

TC_COMMAND = ["tc", "-s", "-d", "class", "show", "dev"]
HTB_PATTERN = r'htb 1:'
HTB_SENT_PATTERN = r'.*rate\s(\d+)'
ADJUST_COEFFICIENT = 0.2

db_service = DbInstance.Instance().db_service


class ABService:
    def __init__(self, ab_instance):
        self.ab_instance = ab_instance
        self.initial_measurements = {}
        self.measurements = {}

    def process_autobandwidth(self):
        start = time.time()
        time.clock()
        elapsed = 0
        while elapsed < self.ab_instance.adjust_interval:
            elapsed = time.time() - start
            # print "loop cycle time: %f, seconds count: %02d" % (time.clock(), elapsed)
            if int(elapsed) == self.ab_instance.statistics_interval:
                self.measure_network()
            time.sleep(1)
        # TODO: if new bw is calculated, force to generate pathTear + new Path messages with new value
        self.process_autobandwidth()

    def get_traffic_diff(self):
        traffic_diff = {}
        for key, values in self.measurements.items():
            start_value = self.initial_measurements[key]
            average_value = sum(values) / len(values)
            traffic_diff[key] = average_value - start_value

        return traffic_diff

    def measure_network(self):
        print("start: " + str(self.measurements))
        diff_model_data = self.get_reserved_interfaces()
        for diff_model in diff_model_data:
            if diff_model.diff > self.ab_instance.adjust_threshold:
                # decrease bw
                Logger.logger.info("ABService: decrease bw for " + diff_model.key + " by " +
                                   str(self.ab_instance.adjust_threshold))
                db_service.update_path_state(diff_model.key, False)
                remove_reserve(diff_model.key)
                path_req = db_service.get_request_data(diff_model.key)
                path_req[DbService.DB_SPEED] -= self.ab_instance.adjust_threshold
                generate_path_tear(path_tear=path_req, is_autobandwidth=True)

            elif diff_model.diff > self.ab_instance.adjust_threshold * ADJUST_COEFFICIENT:
                # increase bw
                Logger.logger.info("ABService: increase bw for " + diff_model.key + " by " +
                                   str(self.ab_instance.adjust_threshold))

    def get_reserved_interfaces(self):
        diff_model_data = []
        reserved_data = db_service.get_all_reserved_interfaces()
        for data in reserved_data:
            diff_model = TrafficDiff(data[DbService.DB_RESERVED_INTERFACE], data[DbService.DB_RESERVED_CLASS],
                                     data[DbService.DB_KEY], data[DbService.DB_SPEED])
            actual_rate = self.get_actual_rate(diff_model.iface, diff_model.class_id)
            diff_model.diff = int(diff_model.reserved_bw) - actual_rate
            # TODO calculate difference from tc command by executing for each iface and parsing per each class
            # compare parsed rate with reserved one
            # if parsed rate up to reserved, try to increase bw by adjust_threshold
            # otherwise decrease by adjust_threshold
            diff_model_data.append(diff_model)

        return diff_model_data

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
