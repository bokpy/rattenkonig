#!/usr/bin/env python3
import os
import time
from evdev import ecodes as ec
import toys as toy
import tricks as trick
import pinky as pink
from icecream import ic

from mouseDebug import capabilities_dump

DEBUG=print
error_ic=ic # like to keep them in error messages
ic.configureOutput(includeContext=True)
function_name_stam='act_'

config_dir=''
def set_config_dir(d):
    global config_dir
    config_dir=toy.make_config_dir(d)

class Litter(trick.CapabilityDict):

    def __init__(S,pups:[pink.Pinky]):
        global config_dir
        if config_dir == '':
            ic('No config directory set')
            exit(234)
        trick.CapabilityDict.__init__(S)
        S.pups=pups
        names=[pup.by_id_name for pup in pups]
        name=toy.longestSubstring(names)
        S.name = toy.sanitize_filename(name)
        S.file_path = config_dir + S.name +'.py'
        ic(S.file_path)

    def __str__(S):
        return S.name

    def litter_events(S):
        return [pup.event for pup in S.pups]
 
    def learn_tricks(S):
        toy.clear_screen()
        capabilities=trick.key_selection(S. litter_events())
        S.update(capabilities)
        S.show(capabilities=True,short=True)
        warn='Write the '
        if os.path.isfile(S.file_path):
            warn='OVERWRITE EXISTING '
        print(f'{warn}Configuration Template?')
        print(f'"{S.file_path}" Yes or No',end='')
        answer=toy.get_a_user_char('YN')
        if answer=='N':
            print('Got a No.')
        elif answer=='Y':
            S.write_configuration_template()

    def show(S,capabilities=False,short=True,tabs=''):
        #ic(short,S.pups)
        print(f'{tabs}Litter("{S.name}")')
        if not short:
            for pup in S.pups:
                print(f'{tabs}    {pup}')
        if capabilities:
            trick.CapabilityDict.show(S,name= S.name,limit=24)

    def event_plus_name(S):
        return f'{S.event:>2} "{S.name}"'

    def write_configuration_template(S):
        try:
            f=open(S.file_path,'w')
        except Exception as e:
            ic(e)
            raise e
        S.write_heading(f)
        S.write_sibling(f)
        S.write_functions(f)
        S.write_event_lookup(f)
        f.close()

    def write_heading(S,f):
        f.write(f'# "{S.file_path}"\n')
        f.write(f'# {time.ctime()}\n')
        # S.naw_to_file(f)
        f.write('\n')
        f.write(f'import evdev\n')
        f.write(f'from evdev import ecodes as ec\n')
        f.write('\n')
        f.write(f'piper=None\n')
        #f.write(f'display=None\n')

    def write_sibling(S,f):
        kin = [ pup.by_id_name for pup in S.pups ]
        f.write(f'tag = {hex(S.pups[0].tag)}\n')
        f.write(f'sibs = [ "{'", "'.join(kin)}"]\n')

    def function_name(S,event_str,event_no):
        global function_name_stam
        if event_str=='Q':
            return function_name_stam + str(event_no)
        return function_name_stam + event_str.lower()

    def write_function(S,f,ev_key,event_name,event_no):
        f.write(f'\ndef {S.function_name(event_name,event_no)}(event): # code {event_no}\n')
        f.write('    global piper\n')
        if ev_key== ec.EV_KEY or ev_key==ec.EV_REL:
            f.write('    # if not piper.match_active_window():\n')
            f.write('    #     piper.squeak_event(event)\n')
            f.write('    # return\n')
            f.write('    piper.squeak_event(event)\n')
            return
        f.write(f'    pass\n')
        f.write(f'    #piper.squeak_event(event)\n')

    def write_functions(S,f):
        f.write('\n')
        for ev_key,ev_events in S.items():
            for event_number,event_name in ev_events.items():
                S.write_function(f,ev_key,event_name,event_number)

    def write_event_lookup(S,f):
        def write_events(event_dict):
             f.write(f'{{\n')
             comma=' '
             for event_number,event_name in event_dict.items():
                 #ic(event_number,event_name)
                 f.write(f'    {comma}{event_number:3d}:{S.function_name(event_name,event_number)}\n')
                 comma=','
             f.write(f'    }}\n')
        f.write(f'\nevent_lookup = {{\n')
        comma=' '
        for ev_type in S:
            f.write(f'{comma}{ev_type}:')
            write_events(S[ev_type])
            comma=','
        f.write(f'}}\n')

# def  catch_mice()->[Litter]:
#     '''
#     Look for mouse devices in /dev/class/input/mouse*
#     :return: a list of class Litter instances
#     :rtype: [Litter]
#     '''
#     it=toy.IterSysMouse()
#     return [Litter(sys_mouse) for sys_mouse in it]
#
# def find_same_name_pub(pups)->bool:
#     pups_iter= iter(pups)
#     previous=next(pups_iter)
#     for cur in pups_iter:
#         if cur == previous:
#             return True
#       previous=cur
#     return False

class Tribes(list):
    """
    A collection of class Liter
    """
    def __init__(S):
        super().__init__(S)
        kin=pink.family_reunion()
        for litter,sibs in kin.items():
            S.append(Litter(sibs))

    def make_templates(S):
        while True:
            count=-1
            toy.clear_screen()
            print(f'Make a configuration for one or more of these device(s)')
            for litter in S:
                count+=1
                print(f'    <{count}> "{litter.name}" events( ',end='')
                events_strings=[str(event) for event in litter.litter_events()]
                print(f'{', '.join(events_strings)} )')
            #print(f'Input choice number 0..{count} -1 to leave',end='')
            num=toy.get_one_digit_int(max=count)
            if num<0:
                print('Bye')
                return
            S[num].learn_tricks()

def listMice(capabilties=False,short=True,tabs='')->None:
    '''
    show a listing of connected mouse devices
    :param capabilities: print the capabilities for each mouse
    :type capabilities: bool
    :param short: print name and event_no
    :return: None
    :rtype:   None
    '''
    set_config_dir('.')
    tribes=Tribes()
    for tribe in tribes:
        if short:
            print(tribe)
        else:
            tribe.show(short=short,capabilities=capabilties,tabs=tabs)
        # if capabilties:
        #     toy.simple_capablities_show(tribe)

def clean_test_dir():
    test_dir = './test_config/'
    if os.path.isdir(test_dir):
        from shutil import rmtree
        rmtree(test_dir)
    set_config_dir(test_dir)

# def test_make_litters():
#     litters = make_litters()
#     for litter in litters:
#         print(f'{litter}')

def test_class_Tribes():
    set_config_dir('./test_litter_config')
    tribes=Tribes()
    #listMice(capabilties=True,short=False)
    tribes.make_templates()

def main(argv: list[str] | None = None) -> int:
    # test_make_litters()
    test_class_Tribes()

if __name__ == "__main__":
    main()
