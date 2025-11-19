#!/usr/bin/env python3
import os
import glob
from collections import defaultdict
import toys as toy

import evdev
import re
from evdev import ecodes as ec
from click import getchar
from icecream import ic
from mouseTables import bus_type,event_types_by_name

ic.configureOutput(includeContext=True)
DEBUG=print
_int=1
_str=0

class Pinky:
    event_to_by_id=defaultdict(str)
    def __init__(S,event_no:int):
        if not isinstance(event_no,int):
            print ('Pinky expects an int value for "event_no"')
            print ('of a path /dev/class/input/mouse"event_no"')
            raise TypeError
        S.event = event_no
        if not Pinky.event_to_by_id:
            S.fill_event_by_id_table()
        S.by_id_name=Pinky.event_to_by_id[event_no]

        #ic(Pinky.event_to_by_id)
        S.sys_path = p = '/sys/class/input/event' + str(event_no)
        S.path = '/dev/input/event' + str(event_no)
        pdid=p + '/device/id/'
        S.product  =toy.read_top_line(pdid,'product')
        S.vendor   =toy.read_top_line(pdid,'vendor')
        S.version  =toy.read_top_line(pdid,'version')
        S.bustype =toy.read_top_line(pdid,'bustype')
        pd=p + '/device/'
        S.name     = toy.read_top_line(pd,'name')
        if not S.by_id_name:
            S.by_id_name=S.name.replace(' ','_')
        S.vendor_str,S.product_str=toy.usb_product_lookup(S.vendor,S.product)
        S.bustype_str=bus_type[int(S.bustype)]
        S.tag=int(S.vendor + S.product + S.version,16)
        S.capabilities={}

    def __str__(S):
        #return f'{S.vendor} {S.product} {S.version} {S.by_id_name} {S.event} '
        return f' {S.event:02d} "{S.by_id_name}"'
        #bustype[{S.bustype}] product[{S.product}] vendor[{S.vendor}] version[{S.version}]'

    def __lt__(S,O)->bool:
        return S.tag < O.tag

    # def name_and_number(S):
    #     return S.name,S.event

    def fill_event_by_id_table(S):
        #ic('fill_event_by_id_table')
        for by_id_path in glob.glob('/dev/input/by-id/*'):
            #print(by_id_path)
            lnk =os.readlink(by_id_path)
            Pinky.event_to_by_id[toy.extract_at_end_int(lnk)]= by_id_path[17:]

    def verbose_str(S):
        return f'{S.path} {S.event} product[{S.product}"{S.product_str}"] vendor[{S.vendor}"{S.vendor_str}"] version[{S.version}]'

    def naw_to_file(S,f):
        f.write(f'# mouse: "{S.name}"\n')
        f.write(f'# product: 0x{S.product} "{S.product_str}"\n')
        f.write(f'# vendor:  0x{S.vendor} "{S.vendor_str,}"\n')
        f.write(f'# version: 0x{S.version}\n')
        f.write(f'# bustype: {S.bustype} " {S.bustype_str}"\n')

    def show(S,tabs=''):
        print(f'{tabs}name: "{S.name}"')
        print(f'{tabs}\tby_id:   "{Pinky.event_to_by_id[S.event]}"')
        print(f'{tabs}\tevent:   {S.event}')
        print(f'{tabs}\tsys:     {S.path}')
        print(f'{tabs}\tproduct: {S.product} "{S.product_str}"')
        print(f'{tabs}\tvendor:  {S.vendor} "{S.vendor_str}"')
        print(f'{tabs}\tversion: {S.version}')
        print(f'{tabs}\tbustype: {S.bustype} "{S.bustype_str}"')


    def get_capabilities(S) -> dict:
        dev = evdev.InputDevice('/dev/input/event' + str(S.event))
        capabilities = dev.capabilities(verbose=True, absinfo=False)
        S.capabilities={}
        def event_item(event):
            return int(event[_int]), toy.string_event_names(event[_str])

        def type_events(events):
            ret = {}
            for event in events:
                key, value = event_item(event)
                ret[key] = value
            return ret

        for key, events in capabilities.items():
            S.capabilities[int(key[_int])] = type_events(events)
        return S.capabilities

    def contribute_keys(S)->dict[int:dict[int:str]]:
        '''
        Selection of capabilities to handle by it's family Litter
        :return: dict{EV_TYPE:{ecode:ecode_name}}
        :rtype: dict[int[int:str]]
        '''
        if not S.capabilities:
            S.get_capabilities()
        toy.clear_screen()
        caps={}
        print (f'"{S.name}" capabilities selection.')
        toy.simple_capablities_show(S.capabilities,tabs='\t'
                                ,event_types= [ec.EV_KEY,ec.EV_REL,ec.EV_LED])
        print (f'N non, A all, P Placeholders,I Interactive',end='')
        choise = toy.get_a_user_char('NAPI')
        if choise == 'N':
            return caps
        if choise == 'A':
            return S.capabilities
        if choise == 'P':
            ic()
            print('Placeholders')
        if choise == 'I':
            ic()
            print('Interactive')

def family_reunion()->dict[int:[]]:
    """
    Makes dictionary that bundles input devices based on a tag
    = vendor + product + version,
    :return: {int:[Pinky's,... ]}
    :rtype: dict[int:[]]
    """
    rodents=[Pinky(ssn) for ssn in toy.get_mice_and_keyboards()]
    rodents.sort()
    # for creature in rodents:
    #     print(f'"{str(creature)}"')

    family_count=1
    families={}
    families[family_count]=[]

    cur=rodents.pop()
    while rodents:
        prev=cur
        families[family_count].append(prev)
        cur = rodents.pop()
        if prev.tag == cur.tag:
            continue
        family_count+=1
        families[family_count]=[]
    families[family_count].append(cur) # don't forget Last-lap Larry
    #ic(families)
    return families


def family_reunion_test():
    tribes = family_reunion()
    for tribe, kin in tribes.items():
        print(f'{tribe:02d}')
        for sib in kin:
            print(f'\t\t{str(sib)}')


def main(argv: list[str] | None = None) -> int:
    # Identity_test()
    family_reunion_test()

if __name__ == "__main__":
    main()