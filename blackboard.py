#!/usr/bin/python3
#
from evdev import UInput, AbsInfo, ecodes as ec
import re
from icecream import ic
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


def main():
    #make_capability_lookup()
    #test_abs()
    kernel_input_codes()

if __name__=='__main__':
    main()
