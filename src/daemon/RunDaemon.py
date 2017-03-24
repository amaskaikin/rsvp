# Usage: python ./RunDaemon.py start|stop|restart device

import logging
import os
import sys
import signal

from daemon import runner
from RSVPDaemon import MyDaemon
from src.utils.Logger import Logger

extra = {'device_name': ''}


def run_daemon(args):
    if len(args) == 2:
        daemon_runner = runner.DaemonRunner(MyDaemon())
        daemon_runner.daemon_context.signal_map = {
            signal.SIGTERM: stop_daemon
        }
        daemon_runner.daemon_context.files_preserve = [Logger.handler.stream]
        daemon_runner.do_action()
    else:
        print "usage: %s start|restart" % args[0]
        sys.exit(2)


def stop_daemon(signum, frame):
    # os.kill(os.getpid(), signal.SIGTERM)
    # TODO: handle stopping daemon
    pass


if __name__ == '__main__':
    run_daemon(sys.argv)

