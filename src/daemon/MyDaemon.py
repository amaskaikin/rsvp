import time
import os


class MyDaemon:
    def __init__(self, logger):
        self.logger = logger
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = os.path.abspath('../../res/my_daemon.pid')
        self.pidfile_timeout = 5

    def run(self):
        while True:
            self.work_it()

    def work_it(self):
        # self.logger.debug("Debug message")
        # self.logger.warn("Warning message")
        # self.logger.error("Error message")
        self.logger.info("Daemon is running...")
        time.sleep(1)