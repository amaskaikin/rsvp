class PathRSVP:
    def __init__(self):
        pass

    HEADER = {'TTL': 65, 'Class': 0x01}
    SESSION = {'Data': 'test'}
    HOP = {'neighbor': '192.168.0.102', 'inface': 3}
    TIME = {'refresh': 4}
    SENDER_TSPEC = {'Tokens': 'testing tokenssssss'}

