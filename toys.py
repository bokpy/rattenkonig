#!/usr/bin/env python3
import os
import glob
from collections import defaultdict
from click import getchar
from difflib import SequenceMatcher
import evdev
import re
from evdev import ecodes as ec


from icecream import ic
import ladders as ladder

ic.configureOutput(includeContext=True)
DEBUG=print
_int=1
_str=0

def longestSubstring(strings:[str]):
    #ic(strings)
    if len(strings) == 0:
        return ''
    if len(strings) == 1:
        return strings[0]
        # initialize SequenceMatcher object with
        # input string
    longest=strings.pop()
    while strings:
        next=strings.pop()
        seqMatch = SequenceMatcher(None, longest,next)
        #ic(seqMatch)
        # find match of longest sub-string
        # output will be like Match(a=0, b=0, size=5)
        match = seqMatch.find_longest_match(0, len(longest), 0, len(next))
        if (match.size == 0):
            return ''
        longest=longest[match.a: match.a + match.size]
    return longest

def extract_first_int(s):
    return int(re.search(r'\d+', s).group())

def extract_at_end_int(s):
    return int(re.search(r'\d+$', s).group())

def common_prefix_length(a,b):
    count=0
    for i,j in zip(a,b):
        if i !=j:
            return count
        count +=1
    return count

def get_an_integer(message='Enter a Number', min=-100, max=100):
    while True:
        in_num=input(message + ' #: ' )
        try:
            num=int(in_num)
        except ValueError:
            print(f'"{in_num}" is not a number.')
            continue
        if (num<=max) and  (num >= min):
            return num
        print(f'enter a number from {min} to {max}',end='')

def getchar_input(allow='*'):
    allow=allow.upper()
    while True:
        print('#:',end='',flush=True)
        c=getchar().upper()
        if (allow == '*') or ( c in allow ):
            return c
        print(f'One of "{allow}" ',end='',flush=True)

def input_input(allow='*'):
    allow=allow.upper()
    while True:
        c=input('->:').upper()
        if c and  (allow=='*') or ( c in allow):
            return c
        print(f'One of "{allow}" ',end='',flush=True)

get_a_user_char=getchar_input

def clear_screen_pass():
    pass

def clear_screen_os():
     os.system('clear')

clear_screen=clear_screen_pass

try:
    f = open("/dev/tty")
    clear_screen=clear_screen_os
    # f=sys.stdin.fileno()
    # print (f'sys.stdin.fileno() {f}')
except Exception as e:
    #print (f'{e}')
    get_a_user_char=input_input

def get_one_digit_int(min=0,max=9):
    s=[chr(ord('0')+i) for i in range(min,max+1)]
    digits='QSLB'+''.join(s)
    print (f'Pick between {min} and {max} or Q,S,L,B,D quits',end='')
    choice=get_a_user_char(digits)
    if choice in  'QSLBD':
        return -1
    return int(choice)

def str_event(event):
    # _timestamp = event.timestamp()
    # _type           = event.type
    # _sec            = event.sec
    # _usec          = event.usec
    # _value         = event.value
    # _code         = event.code
    str_type=ladder.ev_type_no_to_str[event.type]
    str_code=ladder.ev_type_code_no_to_str[event.type][event.code]
    return f'{str_type},{str_code},{event.value}'

def get_mice_and_keyboards()->[int]:
    '''
    Look for device that have mouse or keyboard in the name
    :return: list of numbers of /dev/input/event"number"
    :rtype: [int]
    '''
    event_numbers=[]
    for event_path in evdev.list_devices():
        dev=evdev.InputDevice(event_path)
        up_name=dev.name.upper()
        if ('MOUSE' in up_name) or ('KEYBOARD' in up_name):
            number=extract_at_end_int(event_path)
            #name=dev.name
            #ic(dev,name,number)
            event_numbers.append(number)
    return event_numbers

# def catch_a_reacting_mouse()->tuple[str,int]:
#     '''
#     let the user move a mouse and return name and the event number.
#     :return: tuple[ device name, number of event ]
#     :rtype: tuple[str,int]
#     '''
#     print (f'Move a mouse or press a key to select a mouse or keyboard.')
#     ms=get_mice_and_keyboards()
#     devices=[evdev.InputDevice('/dev/input/event'+str(i)) for i in ms ]
#     for dev in devices:
#         dev.grab()
#
#     got_one=None
#     while not got_one:
#         for dev in devices:
#             got_something=dev.read_one()
#             if (got_something and
#                     ( got_something.type==ec.EV_REL or got_something.type==ec.EV_KEY)):
#                 got_one=dev
#                 break
#     #print(f'Caught Mouse {got_one}. ')
#     for dev in devices:
#         dev.ungrab()
#     return got_one.name,extract_at_end_int(got_one.path)

def string_event_names(event):
    """
    :param event: something like ['BTN_LEFT', 'BTN_MOUSE'] or 'BTN_RIGHT'
    :type event:
    :return: string like 'BTN_LEFT' 'BTN_RIGHT' '?' are replace by 'Q' Question
    :rtype:
    """
    ret=event
    if isinstance(event,tuple) or isinstance(event,list):
        ret = event[0]
    return ret.replace('?', 'Q')

def read_top_line(s_dir: str, s_file: str) -> str | None:
    """
    read the first line and return this line of the file at 'dir/file'
    if the file does not exit return None
    exit at error
    """
    #DEBUG(f'{sys_dir=} {sys_file=}')
    #sysf = os.path.join(sys_dir, sys_file)
    if (s_dir[-1:] != '/') and (s_file[:1] != '/'):
        sf='/'.join([s_dir,s_file])
    else:
        sf = s_dir+ s_file
    #DEBUG(f'{sysf=}')
    try:
        with open(sf, 'r') as f:
            text=f.readline()
            return text.strip()
    except FileNotFoundError as e:
        return None
    except Exception as e:
        ic(e,s_dir, s_file)
        raise

def usb_product_lookup(vendor_id, product_id, pad="/usr/share/hwdata/usb.ids"):
    vendor_name, product_name = None, None
    with open(pad, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            if not line.startswith("\t") and line.split()[0] == vendor_id.lower():
                vendor_name = " ".join(line.split()[1:])
            elif vendor_name and line.startswith("\t") and line.split()[0] == product_id.lower():
                product_name = " ".join(line.split()[1:])
                break
    return vendor_name, product_name

def pci_product_lookup(vendor_id, device_id, pad="/usr/share/hwdata/pci.ids"):
    vendor_name, device_name = None, None
    with open(pad, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            if not line.startswith("\t") and line.split()[0] == vendor_id.lower():
                vendor_name = " ".join(line.split()[1:])
            elif vendor_name and line.startswith("\t") and line.split()[0] == device_id.lower():
                device_name = " ".join(line.split()[1:])
                break
    return vendor_name, device_name
# ChatGPT end
#
# def event_type_name_and_number(event_type):
#     if isinstance(event_type,tuple):
#         return string_event_names(event_type[0]),event_type[1]
#     if isinstance(event_type,int):
#         return ec.EV[event_type],event_type
#     if isinstance(event_type,str):
#         return event_type,event_types_by_name[event_type]
#     ic()
#     raise ValueError
#
# def event_name_and_number(event_item):
#     if isinstance(event_item,tuple) or isinstance(event_item,list):
#         return event_item[0],event_item[1]
#     if isinstance(event_item,int):
#         return ec.KEY[event_item],event_item
#     if isinstance(event_item,str):
#         return event_item,ec.ecodes[event_item]
#     ic()
#     ic(event_item)
#     raise ValueError

def event_path(event_number):
    return '/dev/input/event'+str(event_number)

def BTN_or_KEY_str(event_code):
    if event_code in ec.BTN:  # BTN represents button codes
        return string_event_names( ec.BTN[event_code])
    if event_code in ec.KEY:  # KEY represents key codes
        return string_event_names( ec.KEY[event_code] )
    return 'NO_CODE'

def is_BTN(event_code):
    return event_code in ec.BTN

def is_KEY(event_code):
    return event_code in ec.KEY

def only_buttons(capabilities):
    for code in capabilities[ec.EV_KEY]:
        if not is_BTN(code):
            return False
    return True

def has_no_keys(capabilities):
    for code in capabilities[ec.EV_KEY]:
        if is_KEY(code):
            return False
    return True

def capablities_show(c,name='capabilities',tabs=''):
    def an_event(event):
        return f'{event[_int]:03d}:"{string_event_names(event[_str])}"'
    def type_events(events):
        l= len(events)
        tail_str=''
        if l>5:
            tail_str=f'... {l} in total.'
        ts=[an_event(e) for e in events[:5]]
        tsj=','.join(ts)
        print(f'{{{(tsj)} {tail_str} }}')
    print(f'{tabs}{name} = {{')
    for ev_type,events in c.items():
        print(f'{tabs}{ev_type[_str].ljust(8)}: ',end='')
        type_events(events)
    print(f'{tabs}}}')

def simple_capablities_show(c,name='capabilities',tabs='',limit=16,event_types=None):
    print(f'{tabs}{name} = {{')
    for k,i in c.items():
        if event_types and not (k in event_types):
            continue
        print(f'{tabs}\t{k:2d} {ec.EV[k]}: {{ ',end='')
        tail=''
        l = len(i)
        if l> limit:
            tail = f',... {l} in total.'
        comma=''
        count = limit
        for k2,i2 in i.items():
            #print(f'{comma}{k2}:"{i2}"',end='')
            print(f'{comma}"{i2}"', end='')
            count-=1
            if count <= 0:
                break
            comma=','
        print(f'{tail}}}')
    print(f'{tabs}\t}}')

def make_config_dir(d):
    # if d[-1:] != '/':
    #     d=d+'/'
    if os.path.isdir(d):
        return os.path.abspath(d)+'/'
    try:
        os.makedirs(d)
    except Exception as e:
        ic(e)
        exit(1)
    try:
        with open(d + '__init__.py', 'w') as f:
            f.write('Rattenkonig Configuration\n')
    except Exception as e:
        ic(e)
        exit(1)
    return os.path.abspath(d)+'/'


def sanitize_filename(filename):
    # Remove spaces and punctuation using regex
    sanitized = re.sub(r'[^\w]', '_', filename)  # Replace non-word characters with underscores
    return sanitized

def list_devices_with_name():
    for path in glob.glob('/sys/class/input/event*/device/'):
        event_no=int(re.search(r'\d+', path).group())
        name = read_top_line(path, 'name')
        print(f'event{event_no:<2} "{name}"')

    for path in glob.glob('/sys/class/input/input*/'):
        input_no=int(re.search(r'\d+', path).group())
        name = read_top_line(path, 'name')
        print(f'input{input_no:<2} "{name}"')

def show_event_items(event_items:dict[int,str],max_line_length):
    if not event_items:
        return
    len_sorted=sorted(event_items.items(), key=lambda item: len(item[1]),reverse=True)
    word_len = len(len_sorted[0][1])+1
    prev_len=word_len
    printed_len=word_len
    for code,key_name in len_sorted:
        if (printed_len + word_len) > max_line_length:
            new_len = len(key_name)+1
            if new_len < prev_len - 5:
                prev_len = word_len = new_len
            printed_len=word_len
            print()
        else:
            printed_len+=word_len
        print(f'{key_name.ljust(word_len,' ')}',end='')
    print()

#testers
def test_get_one_digit_int():
    choise=1
    while choise >= 0:
        choise = get_one_digit_int(4,8)
        print(f'{choise=}')

def test_longestSubstring():
    test_strings=["usb-1ea7_2.4G_Mouse-event-kbd"
    ,"usb-1ea7_2.4G_Mouse-if01-event-mouse"
    ,"usb-1ea7_2.4G_Mouse-event-if01"
    ,"2.4G_Mouse"
    ,"2.4G_Mouse_System_Control"
    ]
    print (longestSubstring(test_strings))

def main(argv: list[str] | None = None) -> int:
    test_longestSubstring()
    # test_get_one_digit_int()

if __name__ == "__main__":
    main()