from scapy.contrib.rsvp import *


def get_header(**kwargs):
    return RSVP(
        Version=kwargs.get('Version'),
        Flags=kwargs.get('Flags'),
        Class=kwargs.get('Class'),
        chksum=kwargs.get('chksum'),
        TTL=kwargs.get('TTL'),
        dataofs=kwargs.get('dataofs'),
        Length=kwargs.get('Length')
    )


def get_object(**kwargs):
    return RSVP_Object(
        Class=kwargs.get('Class'),
        Length=kwargs.get('Length')
    )


def get_data(**kwargs):
    return RSVP_Data(
        Data=kwargs.get('Data')
    )


def get_hop(**kwargs):
    return RSVP_HOP(
        neighbor=kwargs.get('neighbor'),
        inface=kwargs.get('inface')
    )


def get_time(**kwargs):
    return RSVP_Time(
        refresh=kwargs.get('refresh')
    )


def get_sender_tspec(**kwargs):
    return RSVP_SenderTSPEC(
        Msg_Format=kwargs.get('Msg_Format'),
        reserve=kwargs.get('reserve'),
        Data_Length=kwargs.get('Data_Length'),
        Srv_hdr=kwargs.get('Srv_hdr'),
        reserve2=kwargs.get('reserve2'),
        Srv_Length=kwargs.get('Srv_Length'),
        Tokens=kwargs.get('Tokens')
    )
