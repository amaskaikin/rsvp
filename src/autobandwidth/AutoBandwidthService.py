import time
import math
import psutil as psutil

from src.db.DbService import DbService, DbInstance

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
        self.measure_initial_values()
        print("start bytes")
        print(self.initial_measurements)
        while elapsed < self.ab_instance.adjust_interval:
            elapsed = time.time() - start
            # print "loop cycle time: %f, seconds count: %02d" % (time.clock(), elapsed)
            if int(elapsed) == self.ab_instance.statistics_interval:
                self.measure_network()
            time.sleep(1)
        traffic_diff = self.get_traffic_diff()
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
        reserved_ifaces = db_service.get_all_reserved_interfaces()
        for iface in reserved_ifaces:
            iface_name = iface[DbService.DB_RESERVED_INTERFACE]
            received = psutil.net_io_counters(pernic=True)[iface_name].bytes_recv
            if iface_name in self.measurements:
                self.measurements[iface_name].append(received)
            else:
                self.measurements[iface_name] = [received]
        print("end: " + str(self.measurements))

    def measure_initial_values(self):
        net = psutil.net_io_counters(pernic=True)
        for key, value in net.items():
            self.initial_measurements[key] = value.bytes_recv

    def calculate_new_rate(self, traffic_diff):
        new_bw = {}
        for iface, diff in traffic_diff:
            if math.fabs(diff) > self.ab_instance.adjust_threshold:
                req = db_service.get_reserved_interface_request(iface)
                req.speed = req.speed + diff



