import logging

from daemon import runner
from MyDaemon import MyDaemon


def set_daemon_runner(my_daemon, handler):
    daemon_runner = runner.DaemonRunner(my_daemon)
    # This ensures that the logger file handle does not get closed during daemonization
    daemon_runner.daemon_context.files_preserve = [handler.stream]
    daemon_runner.do_action()


def set_logger(logger):
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('../res/my_daemon.log')
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return handler


if __name__ == '__main__':
    logger = logging.getLogger()
    set_daemon_runner(MyDaemon(logger), set_logger(logger))
