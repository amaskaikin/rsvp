class Const:
    def __init__(self):
        pass

    TARGET_ADDRESS = '1.1.1.2'

    CL_SESSION = 0x01
    CL_HOP = 0x03
    CL_TIME = 0x05
    CL_ERRSPEC = 0x06
    CL_SENDER = 0x0C
    CL_ADSPEC = 0x0D
    CL_SENDTEMP = 0x0B
    CL_ROUTE = 0x1F
    CL_STYLE = 0x08
    CL_FLOWSPEC = 0x09
    CL_MSG_ID = 0x17

    BANDWIDTH = 10000000

    ERRORS = {
        1: 'Bandwidth is not available',
        2: 'Device already has reservation for this htb class',
        3: 'There is no available htb classes',
        4: 'Htb class does not exist',
        5: 'Htb class is already reserved',
        6: 'Htb class is not reserved'
    }
