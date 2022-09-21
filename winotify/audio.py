"""Handles audio"""

from typing import NamedTuple

ROOT = "ms-winsoundevent:Notification"


class _Sound(NamedTuple):
    """Contains names used by built-in audio samples"""

    Default:        str = '.'.join((ROOT, 'Default'))
    IM:             str = '.'.join((ROOT, 'IM'))
    Mail:           str = '.'.join((ROOT, 'Mail'))
    Reminder:       str = '.'.join((ROOT, 'Reminder'))
    SMS:            str = '.'.join((ROOT, 'SMS'))
    LoopingAlarm:   str = '.'.join((ROOT, 'Looping', 'Alarm'))
    LoopingAlarm2:  str = '.'.join((ROOT, 'Looping', 'Alarm2'))
    LoopingAlarm3:  str = '.'.join((ROOT, 'Looping', 'Alarm3'))
    LoopingAlarm4:  str = '.'.join((ROOT, 'Looping', 'Alarm4'))
    LoopingAlarm5:  str = '.'.join((ROOT, 'Looping', 'Alarm5'))
    LoopingAlarm6:  str = '.'.join((ROOT, 'Looping', 'Alarm6'))
    LoopingAlarm7:  str = '.'.join((ROOT, 'Looping', 'Alarm7'))
    LoopingAlarm8:  str = '.'.join((ROOT, 'Looping', 'Alarm8'))
    LoopingAlarm9:  str = '.'.join((ROOT, 'Looping', 'Alarm9'))
    LoopingAlarm10: str = '.'.join((ROOT, 'Looping', 'Alarm10'))
    LoopingCall:    str = '.'.join((ROOT, 'Looping', 'Call'))
    LoopingCall2:   str = '.'.join((ROOT, 'Looping', 'Call2'))
    LoopingCall3:   str = '.'.join((ROOT, 'Looping', 'Call3'))
    LoopingCall4:   str = '.'.join((ROOT, 'Looping', 'Call4'))
    LoopingCall5:   str = '.'.join((ROOT, 'Looping', 'Call5'))
    LoopingCall6:   str = '.'.join((ROOT, 'Looping', 'Call6'))
    LoopingCall7:   str = '.'.join((ROOT, 'Looping', 'Call7'))
    LoopingCall8:   str = '.'.join((ROOT, 'Looping', 'Call8'))
    LoopingCall9:   str = '.'.join((ROOT, 'Looping', 'Call9'))
    LoopingCall10:  str = '.'.join((ROOT, 'Looping', 'Call10'))
    Silent:         str = 'silent'


Sound = _Sound()
