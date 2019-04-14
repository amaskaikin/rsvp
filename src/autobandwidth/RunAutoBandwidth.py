import threading

import AutoBandwidthModel
from .AutoBandwidthModel import AutoBandwidth
from .AutoBandwidthService import *

MEASURED_TRAFFIC = 0


class ABRunner:

    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution
        # TODO: run autobandwidth if previous hop is sender (get info from IP layer)

    def run(self):
        ab_instance = AutoBandwidth(AutoBandwidthModel.STATISTICS_INTERVAL, AutoBandwidthModel.ADJUST_INTERVAL,
                                    AutoBandwidthModel.ADJUST_THRESHOLD)
        ab_service = ABService(ab_instance)
        #while True:
        ab_service.process_autobandwidth()


