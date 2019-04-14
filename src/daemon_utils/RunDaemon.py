# Usage: python ./RunDaemon.py start|stop|restart device

import os
import signal
import sys

import daemon
from daemon import pidfile

from .RSVPDaemon import MyDaemon
from src.utils.Logger import Logger

extra = {'device_name': ''}
daemon_instance = MyDaemon()


def setup_daemon_context():
    context = daemon.DaemonContext(
        # pidfile=pidfile.TimeoutPIDLockFile(daemon_instance.pidfile),
        stdin=daemon_instance.stdin,
        stdout=daemon_instance.stdout,
        stderr=daemon_instance.stderr,
        files_preserve=[Logger.handler.stream]
    )

    return context


def run_daemon(args):
    if len(args) < 2:
        raise Exception("usage: {} start|stop [autobandwidth]".format(args[0]))

    if args[1] == 'start':
        context = setup_daemon_context()
        with context:
            daemon_instance.run(check_autobandwidth(args))
    elif args[1] == 'stop':
        stop_daemon()
    else:
        raise Exception("usage: {} start|stop".format(args[0]))


def stop_daemon():
    try:
        pf = open(daemon_instance.pidfile, 'r')
    except IOError:
        raise Exception("pidfile {} does not exist. Daemon not running?".format(daemon_instance.pidfile))
    pid = int(pf.read().strip())
    pf.close()

    try:
        os.kill(pid, signal.SIGTERM)
        print("The process {} was successfully stopped".format(pid))
    except OSError as err:
        err = str(err)
        if err.find("No such process") > 0:
            if os.path.exists(daemon_instance.pidfile):
                os.remove(daemon_instance.pidfile)
        else:
            print(str(err))
            sys.exit(1)


def check_autobandwidth(args):
    if len(args) == 3:
        return True
    else:
        return False


if __name__ == '__main__':
    run_daemon(sys.argv)

