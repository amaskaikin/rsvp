class PathRSVP:
    def __init__(self):
        pass

    HEADER = {'TTL': 65, 'Class': 0x01}
    SESSION = {'Data': '192.168.0.107'}
    HOP = {'neighbor': '192.168.0.108', 'inface': 3}
    TIME = {'refresh': 4}
    SENDER_TSPEC = {'Tokens': 'testing tokenssssss'}
    ADSPEC = {'Data': '2 1'}
