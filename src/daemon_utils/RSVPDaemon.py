# Implementation of daemon's job
from .RSVPSniffer import *
from src.data.ReservationRequest import ReservationRequest
from src.htb.Reserve import *
from src.rsvp.model.RSVP_Path import *


class MyDaemon:
    def __init__(self):
        self.socket = None
        self.logger = None
        self.stdin = sys.stdin
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.pidfile = os.path.abspath('res/my_daemon.pid')
        self.pidfile_timeout = 5

    def run(self):
        self.logger = Logger.logger
        self.logger.info("Daemon started")
        # Testing stub for keeping requested qos on the sender
        req = ReservationRequest.Instance()
        req.src_ip = SOURCE_ADDRESS.lstrip('0')
        req.dst_ip = DEST_ADDRESS.lstrip('0')
        req.tos = int(TOS)
        req.speed = int(RATE)
        DbService().flush()
        # b, r = check_reserve(req)
        catch_packet()
