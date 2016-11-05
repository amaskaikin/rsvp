import time
import os
from Sniffer import *


class MyDaemon:
    def __init__(self, logger):
        self.logger = logger
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = os.path.abspath('../res/my_daemon.pid')
        self.pidfile_timeout = 5
        self.socket = None

    def run(self):
        self.logger.info("Daemon started")
        self.socket = create_socket()
        while True:
            self.work_it()

    def work_it(self):
        # self.logger.debug("Debug message")
        # self.logger.warn("Warning message")
        # self.logger.error("Error message")
        # self.logger.info("Daemon is running...")
        # time.sleep(1)
        packet = sniff(self.socket)
        self.logger.info(str(packet.iph[6]))
