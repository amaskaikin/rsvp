

class TrafficDiff:
    def __init__(self, iface=None, class_id=None, key=None, reserved_bw=0, diff=0):
        self.iface = iface
        self.class_id = class_id
        self.key = key
        self.reserved_bw = reserved_bw
        self.diff = diff
