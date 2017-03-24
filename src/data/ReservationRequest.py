class ReservationRequest:
    def __init__(self, src_ip, dst_ip, tos, speed):
        self._src_ip = src_ip
        self._dst_ip = dst_ip
        self._tos = tos
        self._speed = speed

    @property
    def dst_ip(self):
        return self._dst_ip

    @dst_ip.setter
    def dst_ip(self, val):
        self._dst_ip = val

    @property
    def src_ip(self):
        return self._src_ip

    @src_ip.setter
    def src_ip(self, val):
        self._src_ip = val

    @property
    def tos(self):
        return self._tos

    @tos.setter
    def tos(self, val):
        self._tos = val

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, val):
        self._speed = val
