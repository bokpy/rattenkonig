#!/usr/bin/env python3
import time

import evdev
from evdev import InputDevice, categorize, ecodes as ec, list_devices
from ladders import ev_types
from collections import defaultdict
import glob
import re
import asyncio
import atexit

from pygments.lexer import combined

import toys as toy
from icecream import ic

DEBUG=print
error_ic=ic
#ic.configureOutput(prefix, outputFunction, argToStringFunction, includeContext, contextAbsPath)

ic.configureOutput(includeContext=True)
timeout=12

_int=1
_str=0



'''
dev.capabilities(verbose=True)
{
('EV_SYN', 0): [('SYN_REPORT', 0), ('SYN_CONFIG', 1), ('SYN_MT_REPORT', 2), ('?', 4)], 
('EV_KEY', 1): [(['BTN_LEFT', 'BTN_MOUSE'], 272), ('BTN_RIGHT', 273), ('BTN_MIDDLE', 274), ('BTN_SIDE', 275), ('BT
N_EXTRA', 276)],
 ('EV_REL', 2): [('REL_X', 0), ('REL_Y', 1), ('REL_HWHEEL', 6), ('REL_WHEEL', 8), ('R
EL_WHEEL_HI_RES', 11), ('REL_HWHEEL_HI_RES', 12)],
 ('EV_MSC', 4): [('MSC_SCAN', 4)]
 }
 '''

class CapabilityDict(dict):
    #event_type_set = (ec.EV_REL, ec.EV_KEY, ec.EV_LED)
    def __init__(S,event_no=-1):
        super().__init__(S)
        S.placeholder_current_id=1025
        for t in ev_types:
            S[t]={}
        if event_no < 0:
            return
        device = evdev.InputDevice(toy.event_path(event_no))
        caps=device.capabilities(verbose=True,absinfo=False)
        device.close()
        # translate:
        # capabilities(verbose=True) dict to
        # CapabilityDict={EV_TYPE:{EV_CODE:"EV_CODE"}
        # if the "EV_CODE" is a list the first name is used.
        for ev_type,ev_list in caps.items():
            ev_type_no=ev_type[_int]
            # if ev_type_no not in CapabilityDict.event_type_set:
            #     continue
            S[ev_type_no]= {
                ev_code:toy.string_event_names(ec_name) for ec_name,ev_code in ev_list}
        #ic(S)

    def add_placeholder_EV_KEY(S,placeholder):
        if not ec.EV_KEY in S:
            S[ec.EV_KEY]={}
        S[ec.EV_KEY][S.placeholder_current_id]=placeholder
        S.placeholder_current_id+=1
        return S

    def __iadd__(S,O):
        for event_type in ev_types:
            S[event_type].update(O[event_type])
        return S

    # def add_inputdevice_capbilties(S,no):
    #     temp = CapabilityDict(no)
    #     return S.__iadd__(temp)

    def add_all_but_keys(S,O)->dict[int,str]:
        for event_type in ev_types:
            if event_type != ec.EV_KEY:
                S[event_type].update(O[event_type])
        keys={}
        for key_button_code,mnemonic  in O[ec.EV_KEY].items():
            if toy.is_BTN(key_button_code):
                S[ec.EV_KEY].update({key_button_code:mnemonic})
            elif  toy.is_KEY(key_button_code):
                keys[key_button_code]=mnemonic
        return keys

    # def add_event(S,event:evdev.InputEvent):
    #     if event.type not in CapabilityDict.event_type_set:
    #         ic('not a acsepted event',event)
    #         return S
    #     S[event.type].update({event.code:toy.BTN_or_KEY_str(event.code)})

    def write_to_file(S,f,func_name_base='event',lower=True):
        #print(f'Writing "{S.zip.event_path}" to file')
        for event_type,events in S.items():
            for _,event in events.items():
                func_name=func_name_base +'_'+event
                if lower:
                    func_name=func_name.lower()
                f.write(func_name+'\n')

    def show(S,name='',tabs='',limit=26):
        #print(f'"{S.zip.event_path}" CapabilityDict:')
        if name=='':
            print(f'"{name}: "')
        toy.simple_capablities_show(S,name,limit=limit,tabs=tabs+'\t' )
        return S

def key_selection( events:[int] ) -> CapabilityDict:
    '''
    Selection of capabilities to handle by its family Litter
    :return: dict{ecode:ecode_name}
    :rtype: dict[int:str]
    '''
    def make_placeholders(capa_dict):
        print('The Number of Placeholders you want <1 to quit',end='')
        num=toy.get_an_integer()
        if num < 1:
            return
        for i in range(1024 ,1024+num):
            capa_dict[ec.EV_KEY].update({i:"Placeholder_"+str(i)})

    toy.clear_screen()
    no_keys_capabilities=CapabilityDict()
    united_capabilities = CapabilityDict()
    united_keys={}
    pinkies_capabilities = [CapabilityDict(i) for i in events]
    for pinky_capabilities in pinkies_capabilities:
        pinky_keys = no_keys_capabilities.add_all_but_keys(pinky_capabilities)
        united_capabilities+=pinky_capabilities
        united_keys.update(pinky_keys)
    toy.show_event_items(united_keys,80)
    print(f'These are the keys that /dev/input/event {events} can produce.')
    print(f'Use: N non, A all, P Placeholders, I,S Select Interactive, or Q,L,B,D quits', end='')
    choise = toy.get_a_user_char('NAPIQSLBD')
    if choise in 'QLBD':
        return CapabilityDict()
    if choise == 'N':
        return no_keys_capabilities
    if choise == 'A':
        return united_capabilities
    if choise == 'P':
        make_placeholders(no_keys_capabilities)
        return no_keys_capabilities
        # ic(ret)
        # input()
    if choise in 'IS':
        test_CapabilityDict = button_tester(events)
        no_keys_capabilities+=test_CapabilityDict
        return no_keys_capabilities
    return CapabilityDict()

# key press testing
grabed_devices=None
key_events=[]
stopper = 1
previous_key_event = -1

class TestEndExeption(Exception):
    pass

def ungrab_devices():
    global grabed_devices
    if not grabed_devices:
        return
    for device in grabed_devices:
        print(f'Ungrab: "{device.name}"')
        device.ungrab()
        device.close()
    grabed_devices=None

async def read_device(dev):
    global grabed_devices,key_events,stopper,previous_key_event

    async for event in dev.async_read_loop():
        if event.type == ec.EV_KEY and event.value==1:
            if event.code == previous_key_event:
                stopper-=1
                if stopper < 0:
                    #ic(stopper)
                    raise TestEndExeption
                    #return key_events
            else:
                stopper=1
                previous_key_event=event.code
            if toy.is_BTN(event.code):
                print(f'{ec.BTN[event.code]}')
            elif toy.is_KEY(event.code):
                if not event.code in key_events:
                    key_events.append(event.code)
                    print(f'{len(key_events):2d} {ec.KEY[event.code]}')

async def run_tasks():
    global grabed_devices
    tasks = [asyncio.create_task(read_device(d)) for d in grabed_devices]
    await asyncio.gather(*tasks)

def button_tester(events:[int])->CapabilityDict:
    global grabed_devices,key_events,stopper,previous_key_event, key_events
    stopper = 1
    previous_key_event = -1
    key_events = []
    print(f'Press all keys on the device.')
    print(f'press the same key or button 3x when done.')
    #print(f'If there are no keystrokes detected the timeout is {timeout} sec.')
    grabed_devices = [InputDevice(toy.event_path(event)) for event in events]
    for device in grabed_devices:
        device.grab()
    atexit.register(ungrab_devices)
    try:
        asyncio.run(run_tasks())
    except TestEndExeption as e:
        ic(e)
    #    exit(112)
    ungrab_devices()
    atexit.unregister(ungrab_devices)
    ret = CapabilityDict()
    ret[ec.EV_KEY]={code:toy.BTN_or_KEY_str(code) for code in key_events}
    return ret

#testers

def test_CapabilityDict_add_inputdevice_capbilties():
    combined=CapabilityDict()
    nokeys=CapabilityDict()
    # capa17=CapabilityDict(17)
    capas=[CapabilityDict(i) for i in (17, 18, 19, 20)]
    keys={}
    for d in capas:
        combined+=d
        k=nokeys.add_all_but_keys(d)
        keys.update(k)
    combined.show()
    nokeys.show()
    ic(keys)

def test_key_selection():
    united_capabilities= key_selection([17, 18, 19, 20])
    united_capabilities.show()

def test_button_tester():
    result = button_tester([17, 18, 19, 20])
    ic(result)

def main():
    #test_CapabilityDict_add_inputdevice_capbilties()
    test_key_selection()
    #test_button_tester()
    #game_caps=CapabilityDict(zip)


if __name__ == "__main__":
    main()