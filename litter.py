#!/usr/bin/env python3
import os
import time
from evdev import ecodes as ec
import toys as toy
import tricks as trick
import pinky as pink
from icecream import ic

DEBUG=print
error_ic=ic # like to keep them in error messages
ic.configureOutput(includeContext=True)

function_name_stam='act_'

config_dir=''
def set_config_dir(d):
    global config_dir
    config_dir=toy.make_config_dir(d)

class Litter(trick.MouseCapabilities):

    def __init__(S,pups:[pink.Pinky]):
        #ic(pups)
        trick.MouseCapabilities.__init__(S)
        S.pups=pups
        S.name = toy.sanitize_filename(pups[0].name)
        #S.learn_tricks()

    def __str__(S):
        return S.name
 
    def learn_tricks(S):
        toy.clear_screen()
        print (f'\n"{S.name}" members:')
        count=-1
        for pup in S.pups: # type(pup) = toy.Pinky
            #print (f'\t{count} <-- ',end='')
            count+=1
            pup.get_capabilities()
            if ec.EV_REL in pup.capabilities:
                S.add(ec.EV_REL,pup.capabilities[ec.EV_REL])
            if ec.EV_LED in  pup.capabilities:
                S.add(ec.EV_LED,pup.capabilities[ec.EV_LED])
            if ec.EV_KEY in pup.capabilities:
                toy.simple_capablities_show(
                    pup.capabilities
                    ,f'{count} <-- {pup.name}'
                    ,tabs='\t'
                    ,event_types=[ec.EV_KEY,ec.EV_REL,ec.EV_LED]
                )
                print('From which device to select keystrokes negative to stop',end='')
                choice=toy.input_a_number(message='',max=count)
                if choice < 0:
                    return
                S.pups[choice].contribute_capabilities()

        # events= [event for _,event in S.kin]
        # keys = trick.button_tester(S.event,events)
        # # ic(keys)
        # # input('waiting learned tricks')
        # S+=keys

    def add_placeholders(S,num):
        for p in range(ord('A'), ord('A') + num):
            ph = 'placeholder_' + chr(p)
            ic(ph)
            S.add_placeholder_EV_KEY(ph)

    def show(S,capabilities=False,short=True,tabs=''):
        #ic(short,S.pups)
        print(f'{tabs}Litter("{S.name}")')
        if short:
            return
        for pup in S.pups:
            print(f'{tabs}\t{pup}')
        if capabilities:
            trick.MouseCapabilities.show(S,'capabilities')

    def event_plus_name(S):
        return f'{S.event:>2} "{S.name}"'

    def write_configuration_template(S):
        file_path = config_dir +  toy.sanitize_filename(S.name) +'.py'
        S.file_path=os.path.abspath(file_path)
        #ic(S.file_path)
        if os.path.isfile(S.file_path):
            print(f'File "{S.file_path}" exists.')
            print('Overwrite? "N" No or "Q" Quit "Y" = Yes')
            choice=toy.get_a_user_char('NQY')
            if choice in 'NQ':
                return
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
        S.naw_to_file(f)
        f.write('\n')
        f.write(f'import evdev\n')
        f.write(f'import king\n')
        f.write(f'import Xlib\n')
        f.write('\n')
        f.write(f'king=None\n')
        f.write(f'display=None\n')

    def write_sibling(S,f):
        f.write(f'sibs = {S.connect_with_kin}\n')

    def function_name(S,event_str,event_no):
        global function_name_stam
        if event_str=='Q':
            return function_name_stam + str(event_no)
        return function_name_stam + event_str.lower()

    def write_function(S,f,event_name,event_no):
        f.write(f'\ndef {S.function_name(event_name,event_no)}(event): # code {event_no}\n')
        f.write('\tglobal king,display\n')
        f.write(f'\tking.default(event)\n')

    def write_functions(S,f):
        f.write('\n')
        for ev_key,ev_events in S.items():
            for event_number,event_name in ev_events.items():
                S.write_function(f,event_name,event_number)

    def write_event_lookup(S,f):
        def write_events(event_dict):
             f.write(f'{{\n')
             comma=' '
             for event_number,event_name in event_dict.items():
                 #ic(event_number,event_name)
                 f.write(f'\t{comma}{event_number:3d}:{S.function_name(event_name,event_number)}\n')
                 comma=','
             f.write(f'\t}}\n')
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
        kin=toy.family_reunion()
        for litter,sibs in kin.items():
            S.append(Litter(sibs))

    def make_templates(S):
        while True:
            count=-1
            toy.clear_screen()
            print(f'Make a configuration for one or more of these device(s)')
            for litter in S:
                count+=1
                print(f'\t<{count}> "{litter.name}"')
            print(f'Input choice number 0..{count} -1 to leave',end='')
            num=toy.input_a_number('',min=-1,max=count)
            if num<0:
                print('Bye')
                return
            S[num].learn_tricks()

# def check_mice_conected_and_on():
#     while True:
#         mice=catch_mice()
#         mice.sort()
#         listMice(mice=mice,short=True)
#         if find_same_name_pub(mice):
#             print('There are mice with the same name that will have to share'
#                   ' the same configuration.')
#         print(f'\nIf a device is not listed you can connect it or turn it on.')
#         print('Than press "R" to repeat.')
#         print('Any other key to continue.')
#
#         action=toy.get_a_user_char()
#         if action.upper() != 'R':
#             return mice
#
# def make_litters():
#     kin=toy.family_reunion()
#     litters=[Litter(sibs) for _,sibs in kin.items()]
#     return litters
#     #pinky_mouse.write_configuration_template()

def make_a_Pup()-> Litter | None:
    '''
    interactive config template file creation
    :return:
    :rtype:
    '''
    mouse_name,mouse_event=toy.catch_a_reacting_mouse()
    pinky_sys_no = trick.SysDevEvent().sys_mouse_of_event(mouse_event)
    pinky=Litter(pinky_sys_no)
    pinky.show(capabilities=True,short=False)

    #sibs=pinky.get_siblings_by_id()
    sib_caps=[]
    for sib_name,sib_event in pinky.kin:
        if sib_event == pinky.event:
            # print(f'This i me "{sib_name}" {sib_event}')
            continue
        print(f'\tsib: "{sib_name} {sib_event:2d}')
        caps=trick.SibCapabilities(sib_event)
        if caps.has_ev_key():
            caps.show(tabs='\t\t')
        else:
            print ("\t\thas no key or button events.\n")
        sib_caps.append((sib_name,sib_event,caps))

    if len(sib_caps) == 0:
        print(f'No sib devices found for "{pinky.name}"')
        return pinky
    print ('Use keys and or buttons of kin device(s)?')
    print ('"Q" or "D" = Quit Done, "N" = Non, "A" = all, "P" = make Placeholders,\n'
           '"S" or "I" = Select key/buttons Interactive.')
    choice = toy.get_a_user_char('qdnapis')
    if choice in "QD":
        return None
    if choice == "N":
        return pinky
    pinky.connect_with_kin=True
    if choice == 'A':
        for sib,event,caps in sib_caps:
            print(f'add: "{sib}"')
            pinky+=caps
        return pinky
    if choice == 'P':
        print ('Enter the number of placeholders')
        print ('0 or less to abort.')
        num=toy.input_a_number()
        if num > 0:
            pinky.add_placeholders(num)
        return pinky
    if choice in  'IS':
        pinky.learn_tricks()
        return pinky
    ic('this should not happen.')

def listMice(capabilties=False,short=True,tabs='')->None:
    '''
    show a listing of connected mouse devices
    :param capabilities: print the capabilities for each mouse
    :type capabilities: bool
    :param short: print name and event_no
    :type short: bool
    :return: None
    :rtype:   None
    '''
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
    tribes=Tribes()
    #listMice(capabilties=True,short=False)
    tribes.make_templates()

def main(argv: list[str] | None = None) -> int:
    # test_make_litters()
    test_class_Tribes()

if __name__ == "__main__":
    main()
