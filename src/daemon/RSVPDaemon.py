# Implementation of daemon's job


from RSVPSniffer import *
from src.utils.Logger import Logger


class MyDaemon:
    def __init__(self):
        self.socket = None
        self.logger = None
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path = os.path.abspath('res/my_daemon.pid')
        self.pidfile_timeout = 5

    def run(self):
        self.logger = Logger.logger
        self.logger.info("Daemon started")
        catch_packet()
