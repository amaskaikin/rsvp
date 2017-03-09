class ReservationRequest:
    def __init__(self, dst_ip, qos_val, inface):
        self._dst_ip = dst_ip
        self._qos_val = qos_val
        self._inface = inface

    @property
    def dst_ip(self):
        return self._dst_ip

    @dst_ip.setter
    def dst_ip(self, val):
        self._dst_ip = val

    @property
    def qos_val(self):
        return self._qos_val

    @qos_val.setter
    def qos_val(self, val):
        self._qos_val = val

    @property
    def inface(self):
        return self._inface

    @inface.setter
    def inface(self, val):
        self._inface = val
