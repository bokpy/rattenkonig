#!/usr/bin/env python3
import sys
import os
import evdev
import json
from collections import defaultdict
from itertools import product
from pathlib import Path
import glob

from mouseTables import event_types_by_number
from mouseDebug import capabilities_dump

def string_event_names(event):
    """
    :param event: something like ['BTN_LEFT', 'BTN_MOUSE'] or 'BTN_RIGHT'
    :type event:
    :return: string like 'BTN_LEFT_'BTN_MOUSE' or  'BTN_RIGHT'
    :rtype:
    """
    if isinstance(event,str):
        return event
    return "_".join(event)

def merge_capabilities(capA,capB) -> dict:
    merged_dict = {}
    for key in capA.keys() | capB.keys():  # Union of keys from both dictionaries
        merged_dict[key] = list(set(capA.get(key, []) + capB.get(key, [])))
    return merged_dict

class RealMouse:

    def __init__(S,mouse_path):
        """
        mouse_path = 'sys/class/input/mouseN'
        gather some info from the contents of this directory and from  '/dev/input/by-id/'
        """
        S.sys_path = mouse_path
        S.name     = read_sys_mouse_file(mouse_path, 'device/name')
        vendor     = read_sys_mouse_file(mouse_path, 'device/id/vendor')
        product    = read_sys_mouse_file(mouse_path, 'device/id/product')
        S.id       = int(vendor + product,16)
        event      = os.path.basename(glob.glob(mouse_path+'/device/event*')[0])
        S.event    = '/dev/input/' + event
        S.event_kbd  = None
        S.event_if01 = None
        no_space_name=S.name.replace(' ','_')
        S.devices=[evdev.InputDevice(S.event)]
        for file in glob.glob('/dev/input/by-id/*'+no_space_name+'*'):
            print(file)
            lnk   = os.readlink(file)
            event = '/dev/input/'+ lnk[3:]
            #print(f'{file[-4:]=}')
            if file[-4:] == '-kbd':
                S.event_kbd= event
                S.devices.append(evdev.InputDevice(event))
                #print(f'{S.event_kbd=}')
            elif file[-5:] == '-if01':
                S.event_if01=event
                S.devices.append(evdev.InputDevice(event))
                #print(f'{S.event_if01}')
        # S.event_kbd = event_kbd

    def __str__(S):
        ret = f'RealMouse (name="{S.name}" id="{hex(S.id)}" event="{S.event}"'
        if S.event_kbd:
            ret += f' event_kbd="{S.event_kbd}"'
        if S.event_if01:
            ret += f' event_if01="{S.event_if01}"'
        ret += ')'
        return ret

    def lookup_template(S)->dict:
        func_defs=[]
        #capabilities=defaultdict(set)
        event_look_up=defaultdict(dict)
        for device in S.devices:
            capa = device.capabilities( verbose=True,absinfo=False)
            for event_type,events in capa.items():
                event_func_dict={}
                for event in events:
                    func_name='func_' + event_type[0] + '_'  + string_event_names(event[0])
                    event_func_dict[event[1]]=func_name
                event_look_up[event_type[1]]= event_look_up[event_type[1]] | event_func_dict
        print(json.dumps(event_look_up,indent=4))
        return event_look_up

def read_sys_mouse_file(dir: str, file: str) -> str | None:
    """
    read the first line and return this line of the file at 'dir/file'
    if the file does not exit return None
    exit at error
    """
    pad=os.path.join(dir, file)
    try:
        with open(os.path.join(dir, file), 'r') as f:
            text=f.readline()
            return text.strip()
    except FileNotFoundError as e:
        return None
    except Exception as e:
        print("Error reading %s: %s", file, e)
        exit(1)

def trap_mouse_devices() -> dict:
    mouse_population=[]
    mice_devices = glob.glob('/sys/class/input/mouse*')
    for mouse_path in mice_devices:
        a_mouse=RealMouse(mouse_path)
        mouse_population.append(a_mouse)
    return mouse_population


def main(argv: list[str] | None = None) -> int:
    mice=trap_mouse_devices()
    for mouse in mice:
        print(str(mouse))
        mouse.lookup_template()
        #mouse.get_capabilities()


if __name__ == "__main__":
    main()