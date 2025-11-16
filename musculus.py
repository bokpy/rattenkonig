#!/usr/bin/env python3

import os
import sys
import atexit
import importlib
import evdev
from evdev import ecodes as ec
#import json
#from collections import defaultdict
from icecream import ic
from king import MouseKing
from mouseTables import event_types_by_number
import toys as toy
from toys import EventsById

ic.configureOutput(includeContext=True)
DEBUG=print
timeout=12

config_dir=None
def set_config_dir(d):
    global config_dir
    config_dir=toy.make_config_dir(d)
    # enable import of the configuration libs
    sys.path.append(config_dir)

class Musculus(toy.MouseIdentity):

    def __init__(S,sys_no):
        """
        sys_mouse_path = '/sys/class/input/mouseN'
       """
        #print(f'Musculus at {sys_no}')
        toy.MouseIdentity.__init__(S,sys_no)
        S.my_events=[]
        if S.event < 0:
            return
        S.import_lookup()

    def __str__(S):

        sys_mouse=super(Musculus, S).__str__()
        return f'Musculus({sys_mouse})'

        # async def on_click(S,input_device):
        #     event = await input_device.async_read()
        #     print(input_device.path, evdev.categorize(event), sep=': ')
        #
        # def coroutines(S):
        #     return [S.on_click(input_device) for input_device in S.devices]

    def event_action(S,event):
        action=S.go_between[event.type][event.code]
        #ic(action)
        action(event)

    def events(S):
        return S.my_events

    def look_for_kin(S)->None:
        '''
        look for events of devices with shared first part of the name
        and if they are capable of EV_REL or EV_KEY events
        store the event number in the list S.my_events with
        events to listen to.
        :return: side effect fill S.my_events
        :rtype: None
        '''
        kin = toy.find_kin(S.name)

        for sib_name,sib_event in kin:
            #ic(sib_name,sib_event)
            dev = evdev.InputDevice(toy.event_path(sib_event))
            capa = dev.capabilities(verbose=False,absinfo=False)
            #ic(capa)
            if ( ec.EV_REL in capa) or ( ec.EV_KEY in capa):
                S.my_events.append(sib_event)
        #ic(S.my_events)

    def import_lookup(S):
        #ic(config_dir)
        module_name = toy.sanitize_filename(S.name)
        try:
            config = importlib.import_module(module_name)
        except Exception as e:
            #ic(e)
            print(f'"{S.name}" not used, has no config in "{config_dir}"')
            S.event = -1
            return
        print(f'Config: "{config_dir}/{module_name}" found.')
        if config.sibs:
            S.look_for_kin()
        else:
            S.my_events=[S.event]
        S.go_between=config.event_lookup
        config.king=MouseKing.the_king

def get_population()->[Musculus]:
    '''
    look for connected mice /sys/class/input/mouseN
    look for input devices with 
    :return: list of class Musculus mice
    :rtype: [Musculus]
    '''
    # first crown a king
    global king
    king=MouseKing()
    it = toy.IterSysMouse()
    return [Musculus(no) for no in toy.get_sys_mouse_numbers()]

def main(argv: list[str] | None = None) -> int:
    set_config_dir('./config_test/')
    city=get_population()
    print(city)

if __name__ == "__main__":
    main()