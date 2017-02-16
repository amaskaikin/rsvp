# Usage: python ./RunDaemon.py start|stop|restart device

import logging
import os
import sys
import signal

from daemon import runner
from MyDaemon import MyDaemon
from Const import *

extra = {'device_name': ''}


def run_daemon(args):
    if len(args) == 3:
        # set logger
        extra['device_name'] = args[2]
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('../res/my_daemon.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(device_name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger = logging.LoggerAdapter(logger, extra)

        daemon_runner = runner.DaemonRunner(MyDaemon(logger, args[2]))
        daemon_runner.daemon_context.signal_map = {
            signal.SIGTERM: stop_daemon
        }
        daemon_runner.daemon_context.files_preserve = [handler.stream]
        daemon_runner.do_action()
    else:
        print "usage: %s start|restart device" % args[0]
        sys.exit(2)


def stop_daemon(signum, frame):
    os.system('iptables -D ' + Const.IPTABLES_MODE + ' -d ' + Const.TARGET_ADDRESS +
              ' -j NFQUEUE --queue-num ' + str(Const.QUEUE_NUM))


if __name__ == '__main__':
    run_daemon(sys.argv)

