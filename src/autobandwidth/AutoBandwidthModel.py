STATISTICS_INTERVAL = 2
ADJUST_INTERVAL = 10
ADJUST_THRESHOLD = 300000


class AutoBandwidth:
    def __init__(self, statistics_interval=None, adjust_interval=None, adjust_threshold=None):
        self.statistics_interval = statistics_interval
        self.adjust_interval = adjust_interval
        self.adjust_threshold = adjust_threshold
