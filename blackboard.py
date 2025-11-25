#!/usr/bin/python3
#
from click import getchar
from evdev import UInput, AbsInfo, ecodes as ec
import re
import json
from icecream import ic
import time
from ladders import  ev_key_no_to_str,key_to_str

ic.configureOutput(includeContext=True)

def remove_c_comments(code):
    # Regular expression to match C-style comments
    pattern = r'/\*.*?\*/'
    # Use re.sub to replace comments with an empty string
    cleaned_code = re.sub(pattern, '', code, flags=re.DOTALL)
    return cleaned_code

cap = {
	ec.EV_KEY: [ec.KEY_A, ec.KEY_B],
ec.EV_ABS: [
		(ec.ABS_X, AbsInfo(value=0, min=0, max=255,
		                  fuzz=0, flat=0, resolution=0)),
		(ec.ABS_Y, AbsInfo(0, 0, 255, 0, 0, 0)),
		(ec.ABS_MT_POSITION_X, (0, 128, 255, 0))]
}

#ui = UInput(cap, name='example-device', version=0x3)
def test_abs():
    ui=UInput(cap)
    #print(ui.capabilities(verbose=True,absinfo=True))
    # move mouse cursor
    ui.write(ec.EV_ABS, ec.ABS_X, 200)
    ui.write(ec.EV_ABS, ec.ABS_Y, 200)
    ui.syn()

def kernel_input_codes():
    d={}
    with open('/usr/include/linux/input-event-codes.h','r') as f:
        read_header=True
        comma_1= ' '
        comma_2=' '
        print(f'kernel_input_codes={{')
        while True:
            line=f.readline()
            if not line:
                break
            if len(line)<3:
                #print('empty')
                continue
            if ' /* ' == line[:4] :
                continue
            if '/*' in line and '*/' in line:
                line = remove_c_comments(line)
            line = line[:-1]
            if ' * ' == line[:3]:
                if read_header:
                    if len(line) > 27:
                        print(f'\t# {line}')
                        continue
                    print(f'{comma_1}\n"{line[3:]}"{{')
                    comma_1='},'
                    comma_2=' '
                    read_header = False
                continue
            if '#define' == line[:7]:
                read_header=True
                items=line[8:].split('\t')
                if len(items) < 2:
                    items=line[8:].split(' ')
                try:
                    number=items.pop()
                    name=items[0]
                except IndexError:
                    print (f'IndexError: list index out of range "{line}"')
                    continue
                try:
                    int(number)
                except ValueError:
                    try:
                        int(number,16)
                    except ValueError:
                        print(f'\t#{number}:"{name}"')
                        continue

                print(f'\t{comma_2}{number}:"{name}"')
                comma_2=','
        print('}}')

digit_to_ev_code={
    1: 2# "KEY_1"
    ,2  : 3# "KEY_2"
    , 3 : 4# "KEY_3"
    ,4  : 5# "KEY_4"
    ,5  : 6# "KEY_5"
    ,6  : 7# "KEY_6"
    ,7  : 8# "KEY_7"
    ,8  : 9# "KEY_8"
    ,9  : 10# "KEY_9"
    ,0  : 11# "KEY_0"
}

def make_ascii_lookup(ascii_to_ev_key,button_to_ev_btn):
     for ev_key_code,key_str in ev_key_no_to_str.items():
        if "KEY_" == key_str[:4]:
            key=key_str[4:]
            ascii_to_ev_key[key]= ev_key_code
            print(f'{key}:{ev_key_code} # {key_str}')
        if "BTN_" == key_str[:4]:
            key=key_str[4:]
            button_to_ev_btn[key]= ev_key_code
            print(f'{key}:{ev_key_code} # {key_str}')

s=[
"#define KEY_NUMERIC_POUND	0x20b"
,"#define KEY_NUMERIC_A		0x20c	/* Phone key A - HUT Telephony 0xb9 */"
,"#define KEY_NUMERIC_B		0x20d"
,"#define KEY_NUMERIC_C		0x20e"
,"#define KEY_NUMERIC_D		0x20f"
,""
,"#define KEY_CAMERA_FOCUS	0x210"
,"#define KEY_WPS_BUTTON		0x211	/* WiFi Protected Setup key */"
,""
,"#define KEY_TOUCHPAD_TOGGLE	0x212	/* Request switch touchpad on or off"
]
#key_code_re=re.compile(r'#define (KEY_\S*)\s*(\S*)')
key_code_re = re.compile(r'#define (KEY_\S*)\s*([0123456789abcdefx]+)')
btn_code_re = re.compile(r'#define (BTN_\S*)\s*([0123456789abcdefx]+)')

def match_key_code(line):
    x = key_code_re.match(line)
    print(x)
    if x :
        print (f'found in "{line}"')
        print(f'groups {x.group(1)} {x.group(2)}')
    else:
        print (f'not in "{line}"')

def kernel_key_codes():
    ev_key_no_to_str    ={}
    def number(no):
        try:
            return int(no)
        except ValueError:
                return int(no,16)

    with open('/usr/include/linux/input-event-codes.h', 'r') as f:
        comma_1 = ' '
        line = ' '
        print('key_to_str = {')
        while line:
            line = f.readline()
            x = key_code_re.match(line)
            if not x:
                continue
            print(f'    {comma_1}{x.group(2)}:"{x.group(1)}"')
            comma_1 = ','
            ev_key_no_to_str[number(x.group(2))]=x.group(1)
        print('}')

    with open('/usr/include/linux/input-event-codes.h', 'r') as f:
        comma_1 = ' '
        line = ' '
        print('btn_to_str = {')
        while line:
            line = f.readline()
            x = btn_code_re.match(line)
            if not x:
                continue
            print(f'    {comma_1}{x.group(2)}:"{x.group(1)}"')
            comma_1 = ','
            ev_key_no_to_str[number(x.group(2))]=x.group(1)
        print('}')
        return ev_key_no_to_str

def test_match_key_code():
    for l in s:
        match_key_code(l)

def make_capability_lookup():
    ui=UInput()
    v_caps=ui.capabilities(verbose=True,absinfo=True)
    ui.close()
    for ev_type,ev_code in v_caps.items():
        print(f'{ev_type[1]}:')
        ic( ev_type,ec.EV_KEY, ev_type == ec.EV_KEY)
        if ev_type[1] == ec.EV_KEY:
            print("omitted keys.")
            continue
        for names,code in ev_code:
            name=names
            if isinstance(names,list):
                name=names[0]
            print(f'{code}:"{name}"')


def chatGpt_ascii_to_evdev():
    from evdev import ecodes

    ascii_to_evdev = {}

    # control
    ascii_to_evdev.update({
        0: (None, False),
        7: (None, False),
        8: (ecodes.KEY_BACKSPACE, False),
        9: (ecodes.KEY_TAB, False),
        10: (ecodes.KEY_ENTER, False),
        13: (ecodes.KEY_ENTER, False),
        27: (ecodes.KEY_ESC, False),
    })

    # spatie
    ascii_to_evdev[32] = (ecodes.KEY_SPACE, False)

    # cijfers + symbolen erboven
    digit_row = {
        48: (ecodes.KEY_0, False),
        49: (ecodes.KEY_1, False),
        50: (ecodes.KEY_2, False),
        51: (ecodes.KEY_3, False),
        52: (ecodes.KEY_4, False),
        53: (ecodes.KEY_5, False),
        54: (ecodes.KEY_6, False),
        55: (ecodes.KEY_7, False),
        56: (ecodes.KEY_8, False),
        57: (ecodes.KEY_9, False),

        33: (ecodes.KEY_1, True),  # !
        64: (ecodes.KEY_2, True),  # @
        35: (ecodes.KEY_3, True),  # #
        36: (ecodes.KEY_4, True),  # $
        37: (ecodes.KEY_5, True),  # %
        94: (ecodes.KEY_6, True),  # ^
        38: (ecodes.KEY_7, True),  # &
        42: (ecodes.KEY_8, True),  # *
        40: (ecodes.KEY_9, True),  # (
        41: (ecodes.KEY_0, True),  # )
    }
    ascii_to_evdev.update(digit_row)

    # letters
    for c in range(ord('a'), ord('z') + 1):
        ascii_to_evdev[c] = (getattr(ecodes, f"KEY_{chr(c).upper()}"), False)
    for c in range(ord('A'), ord('Z') + 1):
        ascii_to_evdev[c] = (getattr(ecodes, f"KEY_{chr(c)}"), True)

    # leestekens
    punct = {
        45: (ecodes.KEY_MINUS, False),  # -
        95: (ecodes.KEY_MINUS, True),  # _
        61: (ecodes.KEY_EQUAL, False),  # =
        43: (ecodes.KEY_EQUAL, True),  # +
        91: (ecodes.KEY_LEFTBRACE, False),  # [
        123: (ecodes.KEY_LEFTBRACE, True),  # {
        93: (ecodes.KEY_RIGHTBRACE, False),  # ]
        125: (ecodes.KEY_RIGHTBRACE, True),  # }
        92: (ecodes.KEY_BACKSLASH, False),  # \
        124: (ecodes.KEY_BACKSLASH, True),  # |
        59: (ecodes.KEY_SEMICOLON, False),  # ;
        58: (ecodes.KEY_SEMICOLON, True),  # :
        39: (ecodes.KEY_APOSTROPHE, False),  # '
        34: (ecodes.KEY_APOSTROPHE, True),  # "
        44: (ecodes.KEY_COMMA, False),  # ,
        60: (ecodes.KEY_COMMA, True),  # <
        46: (ecodes.KEY_DOT, False),  # .
        62: (ecodes.KEY_DOT, True),  # >
        47: (ecodes.KEY_SLASH, False),  # /
        63: (ecodes.KEY_SLASH, True),  # ?
        96: (ecodes.KEY_GRAVE, False),  # `
        126: (ecodes.KEY_GRAVE, True),  # ~
    }
    ascii_to_evdev.update(punct)

    return ascii_to_evdev

def print_ascii_dict(name,d):
    comma=' '
    print(f'{name}={{')
    for k,i in d.items():
        #ic(k,i)
        key,shift=i
        #ic(key,shift)
        #continue
        print(f'    {comma}{k}:({key},{shift}) ',end='')
        comma=','
        if not key or k<33:
            print()
            continue
        print (f' # {chr(k)}')
    print('}')

tumble=[{1:2, 2:4, 4:5, 5:1},{6:2, 2:3, 3:5, 5:6}]
spin    =[{1:3, 3:4, 4:6, 6:1},{5:6, 6:2, 2:3, 3:5}]
tumble_order=0
spin_order    =0
current_face=1

def act_btn_side(event=0): # code 275
    # print('act_btn_side')
    # return
    global sire,display,current_face,tumble,tumble_order
    if not current_face in tumble[tumble_order]:
        print(f'{current_face=} not in { tumble[tumble_order]}')
        tumble_order=(tumble_order+1)%2
    current_face=tumble[tumble_order][current_face]
    print(current_face)

def act_btn_extra(event=0): # code 276
    global sire,display,current_face,spin,spin_order
    if not current_face in spin[spin_order] :
        print(f'{current_face=} not in { spin[spin_order]}')
        spin_order=(spin_order+1)%2
    print(current_face)

def test_roulette():
     from random import randint
     while True:
         x=randint(0,100)%2
         if x:
             act_btn_extra()
         else:
             act_btn_side()

def main():
    test_roulette()

if __name__=='__main__':
    main()
