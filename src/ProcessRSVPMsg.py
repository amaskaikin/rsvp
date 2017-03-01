from RSVPBuilder import *


def generate_path_msg(**kwargs):
    if 'header' not in kwargs:
        print "Header not exists"
    path_msg = get_header(**kwargs.pop('header'))
    for key, value in kwargs.iteritems():
        if key == 'session':
            length = len(str(value.get('Data')))
            obj = dict(Class=0x01, Length=length + 4)
            path_msg = path_msg/get_object(**obj)/get_data(**value)
        if key == 'hop':
            obj = dict(Class=0x03, Length=16)
            path_msg = path_msg/get_object(**obj)/get_hop(**value)
        if key == 'time':
            obj = dict(Class=0x05)
            path_msg = path_msg/get_object(**obj)/get_time(**value)
        if key == 'sender_tspec':
            length = len(str(value.get('Tokens')))
            obj = dict(Class=0x0c, Length=length + 12)
            path_msg = path_msg/get_object(**obj)/get_sender_tspec(**value)
    return path_msg
