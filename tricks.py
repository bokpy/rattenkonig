#!/usr/bin/env python3
import time
from evdev import InputDevice, categorize, ecodes as ec, list_devices
from collections import defaultdict
import glob
import re
import toys as toy
from icecream import ic

DEBUG=print
error_ic=ic
#ic.configureOutput(prefix, outputFunction, argToStringFunction, includeContext, contextAbsPath)

ic.configureOutput(prefix='Trick: ', includeContext=True)
timeout=12

_int=1
_str=0

class SysDevEvent:
    sys_to_dev={}
    dev_to_sys= {}
    def __init__(S):
        if SysDevEvent.sys_to_dev:
            return

        for g in glob.glob('/sys/class/input/mouse*'):
            sys=toy.extract_at_end_int(g)
            #print(f'{sys=}')
            dev=glob.glob(g+'/device/event*')[0]
            dev=toy.extract_at_end_int(dev)
            #print(f'{dev=}"')
            SysDevEvent.sys_to_dev[sys]=dev
            SysDevEvent.dev_to_sys[dev]=sys
        #ic(SysDevEvent.sys_to_dev,SysDevEvent.dev_to_sys)

    def event_of_sys_mouse(S,no):
        return SysDevEvent.sys_to_dev[no]

    def sys_mouse_of_event(S,no):
        return SysDevEvent.dev_to_sys[no]


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

class MouseZip:
    def __init__(S,sys_mouse_no:int):
        S.sys_path='/sys/class/input/mouse' + str(sys_mouse_no)
        S.name=toy.read_top_line(S.sys_path+'/device','name')
        ev = glob.glob(S.sys_path + '/device/event*')[0]
        S.event =  int(re.search(r'\d+$', ev).group())
        S.event_path='/dev/input/event' + str(S.event)
        S.by_id_name='Not Jet'
        S.sibs=[]

    def __int__(S):
        return S.event

    def __str__(S):
        return S.event_path

    def set_by_id(S,name):
        S.by_id_name=name
        return S

    def set_sibs(S,sibs):
        if sibs:
            S.sibs=sibs
        return S

    def show(S,tabs=''):
        print(f'{tabs}MouseZip ( event {S.event:02d} "{str(S)}" <- "{S.sys_path}")')
        print(f'{tabs}name: "{S.name}"')
        print(f'{tabs}by id "{S.by_id_name}"')
        for sib in S.sibs:
            print(f'{tabs}\tsib {sib}')
        return S

class MouseSib:
    def __init__(S,by_id_path:str):
        try:
            S.event = toy.event_by_id(by_id_path)
        except Exception as e:
            ic()
            raise e
        S.brother=None
        S.name=by_id_path.split('/').pop()

    def show(S,tabs=''):
        print(f'{tabs}MouseSib( "{S.name}" )')
        print(f'{tabs}event {S.event}')
        print(f'brother {S.brother}')

class MouseCapabilities(dict):
    def __init__(S,mouse_zip:MouseZip|int):
        if isinstance(mouse_zip,MouseZip):
            event=mouse_zip.event
        elif isinstance(mouse_zip,int):
            event = mouse_zip
        else:
            error_ic()
            print (f'MouseCapabilities expects a int or MouseZip was {type(mouse_zip)}.')
            raise ValueError
        # init dictionary
        super().__init__(S)
        S.placeholder_current_id=1025
        toy.get_capabilities(S,event)

    def add_placeholder_EV_KEY(S,placeholder):
        if not ec.EV_KEY in S:
            S[ec.EV_KEY]={}
        S[ec.EV_KEY][S.placeholder_current_id]=placeholder
        S.placeholder_current_id+=1
        return S

    def __iadd__(S,O):
        for event_type in O:
            if event_type in S:
                S[event_type].update(O[event_type])
                continue
            S[event_type]=O[event_type].copy()
        return S

    def write_to_file(S,f,func_name_base='event',lower=True):
        print(f'Writing "{S.zip.event_path}" to file')
        for event_type,events in S.items():
            for _,event in events.items():
                func_name=func_name_base +'_'+event
                if lower:
                    func_name=func_name.lower()
                f.write(func_name+'\n')

    def show(S,name='',tabs=''):
        #print(f'"{S.zip.event_path}" MouseCapabilities:')
        if name=='':
            name=S.name
        toy.simple_capablities_show(S,name,tabs+'\t' )
        return S
        # for key in S:
        #     if S[key]:
        #         print(f'{tabs}{key} #{ec.EV[key]} ')
        #         print (f'{tabs}{S[key]}')

class SibCapabilities(dict):
    def __init__(S, sib_mouse:MouseSib|int):
        if isinstance(sib_mouse,int):
            S.event = sib_mouse
        elif isinstance(sib_mouse,MouseSib):
            S.event=sib_mouse.event
        else:
            print('SibCapabilities expects /dev/input/event"int" or "MouseSib" argument')
            error_ic()
            raise ValueError
        # init dictionary
        super().__init__(S)
        toy.get_capabilities(S, S.event)

    def has_ev_key(S):
        return ec.EV_KEY in S

    def show(S, tabs=''):
        toy.simple_capablities_show(S,S.event,tabs+'\t' )
        return S
        # print(f'"{S.sib.event}" SibCapabilities:')
        # for key in S:
        #     if S[key]:
        #         print(f'{tabs}{key} #{ec.EV[key]} ')
        #         print(f'{tabs}{S[key]}')

def button_tester(ignore:int,events:[int])-> dict[int, dict[int, str]]:
    '''
    Test which events are generated by the mouse buttons
    on a mouse device.
    :param ignore: the mouse event
    :type ignore: int
    :param events: list of event numbers to monitor
    :type events: list[int]
    :return: dict {ec.EV_KEY:{event.code:ecodes.BTN or KEY}
    :rtype: dict[int, dict[int, str]]
    '''
    print(f'Press all keys on the device.')
    print(f'press the same key 3x when done.')
    print(f'If there are no keystrokes detected the timeout is {timeout} sec.')

    last_key = -1
    stop_count = 3
    stop_time = time.time() + timeout
    a_key_was_pressed = False
    print (f'button_tester({ignore=},{events=})')

    def stop_test(test_event)->bool:
        """
        Test if the time is up and nothing happened or if
        the user pressed the same button 3 times
        :param event: evdev InputEvent
        :type event: InputEvent
        :return: True stop False continue
        :rtype: bool
        """
        nonlocal a_key_was_pressed,stop_time,stop_count,last_key

        # there is no live sign from these devices check to timeout
        if not test_event and not a_key_was_pressed:
            if time.time() > stop_time:
                print('Key press test timed out')
                return True
        if not test_event:
            return False
        #if it was a key or button press test for the count out
        if test_event.type == ec.EV_KEY and test_event.value:
            a_key_was_pressed = True
            #DEBUG(f'{stop_count } {last_key=} {test_event.code=}')
            if last_key == test_event.code:
                stop_count -= 1
                return stop_count <= 0
            # an other key was pressed restart the countdown
            last_key = test_event.code
            stop_count = 3
        return False

    ev_key_events = {}
    ev_key_events[ec.EV_KEY]={}
    tested_events=ev_key_events[ec.EV_KEY]

    event_count = 0

    def show_status():
        nonlocal tested_events,event_count
        length=len(tested_events)
        if length == event_count:
            return
        print(f'{length:3d} ',end='')
        for code,code_str in tested_events.items():
            print (f'[{code:03d},{code_str}] ',end='')
        event_count=length
        print()

    def handle_event(event):
        nonlocal tested_events,a_key_was_pressed
        if not event or not event.value:
            return False
        if event.type == ec.EV_KEY:
            a_key_was_pressed = True
            bok=toy.BTN_or_KEY_str(event.code)
            code_str=toy.string_event_names(bok)
            #DEBUG(f'Key Event "{code_str}"')
            if not event.code in tested_events:
                tested_events[event.code]=code_str
                show_status()
            #ic(ec.KEY[event.code])
            return True
        if event.type == ec.EV_REL:
            #DEBUG(f'Rel Event "{ec.REL[event.code]}"')
            #test_events[event.type][event.code]=ec.REL[event.code]
            #ic(ec.REL[event.code])
            return True
        return False
        #print(f'{ec.EV[event.type]}:{event.code} not handled.')

    devices=[InputDevice(toy.event_path(event)) for event in events]
    for dev in devices : dev.grab()

    event_ignore=toy.event_path(ignore)
    while True:
        got_somthing=None
        for dev in devices:
            got_somthing = dev.read_one()
            if got_somthing and (event_ignore != dev.path):
                #print(dev)
                handle_event(got_somthing)
                break
        if stop_test(got_somthing):
            break

    for dev in devices:
        dev.ungrab()
    return ev_key_events

def main():

    zip=MouseZip(0)
    zip.show()
    game_caps=MouseCapabilities(zip)


if __name__ == "__main__":
    main()