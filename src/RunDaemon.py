# Usage: python ./RunDaemon.py start|stop|restart device

import logging
import sys
from daemon import runner
from MyDaemon import MyDaemon

extra = {'device_name': ''}

if __name__ == '__main__':
    if len(sys.argv) == 3:
        # set logger
        extra['device_name'] = sys.argv[2]
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('../res/my_daemon.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(device_name)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger = logging.LoggerAdapter(logger, extra)

        # set daemonization
        daemon_runner = runner.DaemonRunner(MyDaemon(logger, sys.argv[2]))
        daemon_runner.daemon_context.files_preserve = [handler.stream]
        daemon_runner.do_action()
    else:
        print "usage: %s start|restart device" % sys.argv[0]
        sys.exit(2)
