#!/usr/bin/env python3
'''
Read the configuration for the devices from the file in
config_dir and make the functions available via a dict
'''
import os
import sys
import atexit
import importlib
import time

import evdev
from evdev import ecodes as ec,categorize
#import json
#from collections import defaultdict
from icecream import ic
from king import MouseKing
import pinky as pink
from tricks import  CapabilityDict
from ladders import event_types_by_number
import toys as toy

ic.configureOutput(includeContext=True)
DEBUG=print

config_dir=None
def set_config_dir(d):
    global config_dir
    config_dir=toy.make_config_dir(d)
    # enable import of the configuration libs
    sys.path.append(config_dir)

class MouseTroupe:
    def __init__(S,pinkies:[pink.Pinky]):
        global config_dir
        if config_dir == '':
            ic('No config directory set')
            exit(234)
        S.mice=pinkies.copy()
        names = [mouse.by_id_name for mouse in S.mice]
        name = toy.longestSubstring(names)
        S.name = toy.sanitize_filename(name)
        S.file_path = config_dir + S.name + '.py'
        S.magic_tricks=None
        S.read_magic()
        S.events=[]
        if S.magic_tricks:
            S.events = [mouse.event for mouse in S.mice]
        #ic(S.events)

        #ic(S.file_path)
    def is_preforming(S):
        return S.magic_tricks!=None

    def actors(S):
        return S.mice

    def read_magic(S):
        try:
            config = importlib.import_module(S.name)
        except Exception as e:
            # ic(e)
            print(f'"{S.name}"\nhas no config in\n"{config_dir}"\n')
            return
        print(f'Config: "{S.file_path}" found.\n')
        S.magic_tricks = config.event_lookup
        config.sire = MouseKing.the_king


    # def do_magic(S,event):
    #     if not event.type in  CapabilityDict.event_type_set:
    #         print(categorize(event))
    #         return
    #     S.check_alarm(event)
    #     func= S.magic_tricks[event.type][event.code]
    #     #ic(func)
    #     func(event)

    def show(S):
        tricks='has no preformance'
        if S.magic_tricks:
            tricks = "is preforming"
        print(f'MouseTroupe("{S.name}") {tricks}.')
        for mouse in S.mice:
            print(f'\t\t"{mouse.by_id_name}"')

class MouseCircus(list):

    def __init__(S):
        super().__init__(S)
        # first crown a king
        global king
        king=MouseKing()
        troupes=pink.family_reunion()
        #ic(troupes)
        for number,pinkies in troupes.items():
            S.append(MouseTroupe(pinkies))

    def devices(S):
        ret=[]
        for troupe in S:
            ret+=troupe.events
        return ret

    def show(S):
        for troupe in S:
            troupe.show()


def test_MouseCircus():
    circus = MouseCircus()
    circus.show()

def main(argv: list[str] | None = None) -> int:
    set_config_dir('./test_litter_config')
    test_MouseCircus()

if __name__ == "__main__":
    main()