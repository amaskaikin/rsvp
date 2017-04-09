from RSVPBuilder import *
from src.utils.Const import Const


def generate_msg(**kwargs):
    if 'header' not in kwargs:
        print "Header not exists"
    path_msg = get_header(**kwargs.pop('header'))
    for key, value in kwargs.iteritems():
        if key == 'session':
            length = len(str(value.get('Data')))
            obj = dict(Class=Const.CL_SESSION, Length=length + 4)
            path_msg = path_msg/get_object(**obj)/get_data(**value)
        if key == 'hop':
            obj = dict(Class=Const.CL_HOP, Length=16)
            path_msg = path_msg/get_object(**obj)/get_hop(**value)
        if key == 'time':
            obj = dict(Class=Const.CL_TIME)
            path_msg = path_msg/get_object(**obj)/get_time(**value)
        if key == 'sender_tspec':
            length = len(str(value.get('Tokens')))
            obj = dict(Class=Const.CL_SENDER, Length=length + 12)
            path_msg = path_msg/get_object(**obj)/get_sender_tspec(**value)
        if key == 'adspec':
            length = len(str(value.get('Data')))
            obj = dict(Class=Const.CL_ADSPEC, Length=length + 4)
            path_msg = path_msg/get_object(**obj)/get_data(**value)
        if key == 'sender_template':
            length = len(str(value.get('Data')))
            obj = dict(Class=Const.CL_SENDTEMP, Length=length + 4)
            path_msg = path_msg/get_object(**obj)/get_data(**value)
        if key == 'style':
            length = len(str(value.get('Data')))
            obj = dict(Class=Const.CL_STYLE, Length=length + 4)
            path_msg = path_msg/get_object(**obj)/get_data(**value)
        if key == 'msg_id':
            length = len(str(value.get('Data')))
            obj = dict(Class=Const.CL_MSG_ID, Length=length + 4)
            path_msg = path_msg/get_object(**obj)/get_data(**value)
        if key == 'flowspec':
            length = len(str(value.get('Data')))
            obj = dict(Class=Const.CL_FLOWSPEC, Length=length + 4)
            path_msg = path_msg/get_object(**obj)/get_data(**value)
        if key == 'error_spec':
            length = len(str(value.get('Data')))
            obj = dict(Class=Const.CL_ERRSPEC, Length=length + 4)
            path_msg = path_msg/get_object(**obj) / get_data(**value)
    return path_msg
