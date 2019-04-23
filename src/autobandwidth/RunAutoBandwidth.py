import threading

import AutoBandwidthModel
from src.db.DbService import DbInstance
from .AutoBandwidthModel import AutoBandwidth
from .AutoBandwidthService import *

MEASURED_TRAFFIC = 0


class ABRunner:

    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        ab_instance = AutoBandwidth(AutoBandwidthModel.STATISTICS_INTERVAL, AutoBandwidthModel.ADJUST_INTERVAL,
                                    AutoBandwidthModel.ADJUST_THRESHOLD)
        db_instance = DbInstance.Instance().db_service
        ab_service = ABService(ab_instance, db_instance)
        ab_service.process_autobandwidth()


