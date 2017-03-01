# Implementation of daemon's job

import time
import os
from RSVPSniffer import *


class MyDaemon:
    def __init__(self, logger, device):
        self.logger = logger
        self.device = device
        self.socket = None
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = os.path.abspath('../res/my_daemon.pid')
        self.pidfile_timeout = 5

    def run(self):
        self.logger.info("Daemon started")
        catch_packet()
        # Sniff
        # self.socket = create_socket(self.device)
        # while True:
            # self.write_to_log_every_second()
            # self.write_to_log_protocol()

    def write_to_log_protocol(self):
        self.logger.info(sniff(self.socket))

    def write_to_log_every_second(self):
        # self.logger.debug("Debug message")
        # self.logger.warn("Warning message")
        # self.logger.error("Error message")
        self.logger.info('Daemon is running...')
        time.sleep(1)
