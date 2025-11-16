#!/usr/bin/env python3
import os
import glob
import evdev
import re
from evdev import ecodes as ec
from click import getchar
from icecream import ic
from mouseTables import bus_type,event_types_by_name

DEBUG=print
_int=1
_str=0

def extract_first_int(s):
    return int(re.search(r'\d+', s).group())

def extract_at_end_int(s):
    return int(re.search(r'\d+$', s).group())

def input_a_number(message='Enter a Number'):
    while True:
        in_num=input(message + ' #: ' )
        try:
            num=int(in_num)
            return num
        except ValueError:
            print(f'"{in_num}" is not a number.')

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

try:
    f = open("/dev/tty")
    # f=sys.stdin.fileno()
    # print (f'sys.stdin.fileno() {f}')
except Exception as e:
    #print (f'{e}')
    get_a_user_char=input_input

def event_print(event):
    _timestamp = event.timestamp()
    _type           = event.type
    _sec            = event.sec
    _usec          = event.usec
    _value         = event.value
    _code         = event.code
    print(f'"code{_code}" "{_sec}sec" "stamp:{_timestamp}" "type:{_type}" "{_usec}usec" "value:{_value}"')

class IterById:
    def __iter__(S):
        S.cur=-1
        S.by_id_devices=glob.glob('/dev/input/by-id/*')
        S.count=len(S.by_id_devices)
        return S

    def __next__(S):
        S.cur+=1
        if S.cur < S.count:
            return S.by_id_devices[S.cur]
        raise StopIteration

def get_sys_mouse_numbers():
    return [extract_at_end_int(sys_path) for sys_path in glob.glob('/sys/class/input/mouse*')]


class IterSysMouse:
    '''

    '''
    def __iter__(S):
        S.cur=-1
        S.sys_mice=[extract_at_end_int(sys_path) for sys_path in glob.glob('/sys/class/input/mouse*')]
        S.count=len(S.sys_mice)
        return S

    def __next__(S):
        S.cur+=1
        if S.cur < S.count:
            return S.sys_mice[S.cur]
        raise StopIteration

#def get_sibs_by_id()

def sys_mouse_event(path):
    return os.path.basename(glob.glob(path+'/device/event*')[0])

def mouse_events():
    globbers=glob.glob('/sys/class/input/mouse*/device/event*')
    return [dev.split('/')[-1:][0] for dev in globbers]

def catch_a_moving_mouse()->tuple[str,int]:
    '''
    let the user move a mouse and return name and the event number.
    :return: tuple[ device name, number of event ]
    :rtype: tuple[str,int]
    '''
    print (f'Move the mouse you want to work on')
    ms=mouse_events()
    devices=[evdev.InputDevice(event_path(i)) for i in ms ]
    for dev in devices:
        dev.grab()

    got_one=None
    while not got_one:
        for dev in devices:
            got_something=dev.read_one()
            if got_something and got_something.type==ec.EV_REL:
                got_one=dev
                break
    #print(f'Caught Mouse {got_one}. ')
    for dev in devices:
        dev.ungrab()
    return got_one.name,extract_at_end_int(got_one.path)

class MouseIdentity:
    def __init__(S,sys_no:int):
        if not isinstance(sys_no,int):
            print ('MouseIdentity expects an int value for "sys_no"')
            print ('of a path /dev/class/input/mouse"sys_no"')
            raise ValueError

        S.sys_no   = sys_no
        S.path        =p='/sys/class/input/mouse' + str(sys_no )
        pdid=p + '/device/id/'
        S.product  =read_top_line(pdid,'product')
        S.vendor   =read_top_line(pdid,'vendor')
        S.version  =read_top_line(pdid,'version')
        S.bustype =read_top_line(pdid,'bustype')
        S.event     =extract_at_end_int(sys_mouse_event(p))
        pd=p + '/device/'
        S.name     =read_top_line(pd,'name')
        S.vendor_str,S.product_str=usb_product_lookup(S.vendor,S.product)
        S.bustype_str=bus_type[int(S.bustype)]

    def __str__(S):
        return f'{S.path} {S.event} bustype[{S.bustype}] product[{S.product}] vendor[{S.vendor}] version[{S.version}]'

    def name_and_number(S):
        return S.name,S.event

    def verbose_str(S):
        vendor,product=usb_product_lookup(S.vendor,S.product)
        return f'{S.path} {S.event} product[{S.product}"{product}"] vendor[{S.vendor}"{vendor}"] version[{S.version}]'

    def naw_to_file(S,f):
        f.write(f'# mouse: "{S.name}"\n')
        f.write(f'# product: 0x{S.product} "{S.product_str}"\n')
        f.write(f'# vendor:  0x{S.vendor} "{S.vendor_str,}"\n')
        f.write(f'# version: 0x{S.version}\n')
        f.write(f'# bustype: {S.bustype} " {S.bustype_str}"\n')

    def show(S):
        print(f'name: "{S.name}"')
        print(f'\tevent:   {S.event}')
        print(f'\tsys:     {S.path}')
        print(f'\tproduct: {S.product} "{S.product_str}"')
        print(f'\tvendor:  {S.vendor} "{S.vendor_str}"')
        print(f'\tversion: {S.version}')
        print(f'\tbustype: {S.bustype} "{S.bustype_str}"')

def numeric_str(p:int|str)->str:
    """
    Return for every int or string ending with a 1 or 2 digits
     a number string
    :param p: int or string ending with a 1 or 2 digits
    :type p: int|str
    :return: string of one of two digits
    :rtype: str
    """
    if isinstance(p,int):
        return str(p)
    try:
        n=int(p[-2:])
        return numeric_str(n)
    except ValueError:
        pass
    try:
        n=int(p[-1:])
        return numeric_str(n)
    except ValueError as e:
        ic()
        print(f'Can not construct a numeric string from "{p}".')
        raise ValueError

def event_path(p:int|str)->str:
    """
    Return for every int or string ending with a 1 or 2 digit number
    a corresponding path /dev/input/eventN
    :param p: int or string ending with one or two numeric characters
    :type :
    :return: path like /dev/input/eventN
    :rtype: str
    """
    num=numeric_str(p)
    return '/dev/input/event'+num

def sys_path(p:int|str)->str:
    """
    Return for every int or string ending with a 1 or 2 digit number
    a corresponding path /dev/class/input/mouseN
    :param p: int or string ending with one or two numeric characters
    :type: int|str
    :return: path like /sys/class/input/mouseN
    :rtype: str
    """
    num=numeric_str(p)
    return '/sys/class/input/mouse'+num

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
        print("Error reading %s: %s", sf, e)
        exit(1)

def event_by_id(path)->int:
    ps=path.split('/')
    p=ps[-1:][0]
    lnk=os.readlink('/dev/input/by-id/'+p)
    # if 'mouse' in lnk:
    #     return None
    ret=extract_at_end_int(lnk)
    return ret

def get_capabilities(caps:dict,event:int)->dict:
    if not isinstance(event,int):
        print(f'get_capabilities(event) "event" should be an integer.')
        print(f'from a path /dev/input/event(int event)' )
    dev = evdev.InputDevice('/dev/input/event' + str(event))
    capabilities = dev.capabilities(verbose=True,absinfo=False)

    def event_item(event):
        return int(event[_int]),string_event_names(event[_str])

    def type_events(events):
        ret={}
        for event in events:
            key,value = event_item(event)
            ret[key]=value
        return  ret

    for key, events in capabilities.items():
        caps[int(key[_int])] = type_events(events)
    return caps

def find_kin(name_stam:str)-> list[tuple[str,int]]:
    '''
    Looks in '/dev/input/by-id/ for devices
     with "name_stam" spaces replaced by underscores in it.
    :param name_stam: name of a mouse like "USB Gaming Mouse"
    :type name_stam: str
    :return: list [(by-id name,event no)]
    :rtype: list[tuple[str,int]]
    '''
    if not isinstance(name_stam,str):
        ic()
        raise ValueError

    mouse_stam=name_stam.replace(' ','_')
    kin=[]
    for sib in glob.glob('/dev/input/by-id/*'+mouse_stam+'*'):
        lnk = os.readlink(sib )
        kin.append((sib[17:],extract_at_end_int(lnk)))
    return kin

class EventsById(dict):
    '''
    a dictionary of
     {event numbers:names found in '/dev/input/by-id/device_name,... }
    '''
    def __init__(S):
        super().__init__(S)
        #S.reversed={}
        for by_id in glob.glob('/dev/input/by-id/*'):
            event = event_by_id(by_id)
            # remove '/dev/input/by-id/
            S[event]=by_id[17:]
            #S.reversed[by_id]=event

    def kin_events(S,name_stam):
        events=[event for event,name in S.items() if name.startswith(name_stam)]
        return events

    def sibs(S,brother:int,brother_name:str)->dict:
        # if not isinstance(brother,int):
        #    raise ValueError
        if not isinstance(brother_name,str):
            ic()
            raise ValueError

        brother_name=brother_name.replace(' ','_')

        #print(f'{brother} -> "{brother_name}"')
        family=[]
        for event,name in S.items():
            #print(f' {event == brother} {event} == {brother}')
            # I'm not my one brother
            if event == brother:
                continue
            # If we have simular name we must be family
            #print(f'"{brother_name}" in "{name}" {brother_name in name}')
            if brother_name in name:
                family.append((name,event))
        return family

    def show(S,tabs=''):
        print(f'{tabs}EventsById = {{')
        for key,value in S.items():
            print (f'{tabs}{key:>2}:"{value}"')
        print(f'{tabs}}}')
        return S

# ChatGPT
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

def event_type_name_and_number(event_type):
    if isinstance(event_type,tuple):
        return string_event_names(event_type[0]),event_type[1]
    if isinstance(event_type,int):
        return ec.EV[event_type],event_type
    if isinstance(event_type,str):
        return event_type,event_types_by_name[event_type]
    ic()
    raise ValueError

def event_name_and_number(event_item):
    if isinstance(event_item,tuple) or isinstance(event_item,list):
        return event_item[0],event_item[1]
    if isinstance(event_item,int):
        return ec.KEY[event_item],event_item
    if isinstance(event_item,str):
        return event_item,ec.ecodes[event_item]
    ic()
    ic(event_item)
    raise ValueError

def BTN_or_KEY_str(code):
    try:
        return string_event_names( ec.KEY[code] )
    except KeyError:
        pass
    try:
        return string_event_names( ec.BTN[code])
    except KeyError:
        return 'NO_CODE'

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

def simple_capablities_show(c,name='capabilities',tabs=''):
    tops=16
    print(f'{tabs}{name} = {{')
    for k,i in c.items():
        print(f'{tabs}\t{k:2d}: {{ ',end='')
        tail=''
        l = len(i)
        if l> tops:
            tail = f',... {l} in total.'
        comma=''
        count = 6
        for k2,i2 in i.items():
            #print(f'{comma}{k2}:"{i2}"',end='')
            print(f'{comma}"{i2}"', end='')
            count-=1
            if count <= 0:
                break
            comma=','
        print(f'{tail}}}')
    print(f'{tabs}}}')


def make_config_dir(d):
    if os.path.isdir(d):
        return d
    try:
        os.makedirs(d)
    except Exception as e:
        ic(e)
        exit(1)
    try:
        with open(d + '__init__.py', 'w') as f:
            return d
    except Exception as e:
        ic(e)
        exit(1)
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

def main(argv: list[str] | None = None) -> int:
    kin=find_kin("USB Gaming Mouse")
    print(kin)
    exit(0)
    input_a_number()
    catch_a_moving_mouse()
    exit(0)
    dev=evdev.InputDevice('/dev/input/event4')
    capablities_show(dev.capabilities(verbose=True))
    #list_devices_with_name()
    id=MouseIdentity(1)
    print(id)
    id.show()
    byid=EventsById()
    byid.show()
    exit(0)
    sysMice=IterSysMouse()
    for path in sysMice:
        #print(f'{path=} {sys_mouse_event(path)}')
        info=SysMouseInfo(path)
        info.show()
        print()

    by_ids=IterById()
    for device in by_ids:
        print(device)
        print(event_by_id(device))
    event_by_id('usb-1ea7_2.4G_Mouse-if01-event-mouse')


if __name__ == "__main__":
    main()