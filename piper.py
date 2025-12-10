#!/usr/bin/python3
from evdev import UInput, ecodes as ec, AbsInfo
import atexit
import time
from Xlib import display
import ladders as ladder
import  tracer as trace
from ladders import ascii_to_evdev as asc2ev
import toys as toy
from icecream import ic
ic.configureOutput(includeContext=True)
KEYDELAY=.001
L_SHIFT=SHIFT=42
R_SHIFT=54
help_text="""
ChatGPT:

Allow non-root access to /dev/uinput via udev (recommended)

Description
-----------
Create a persistent udev rule that sets the device node for /dev/uinput to a group
you control (for example 'uinput'), then add your user to that group. This
permits opening the uinput device from a regular user process without running
the script as root.

Steps (one-time, run as root):
  1. Create group and add your user:
     sudo groupadd --system uinput    # only if group doesn't exist
     sudo usermod -aG uinput <your-user>

  2. Create udev rule (file: /etc/udev/rules.d/99-uinput.rules):
     KERNEL=="uinput", SUBSYSTEM=="misc", MODE="0660", GROUP="uinput"

  3. Reload udev rules and trigger:
     sudo udevadm control --reload-rules
     sudo udevadm trigger --action=add /dev/uinput

Notes
-----
• This is persistent across reboots and is the safest common approach.
• If /dev/uinput already exists with different attributes on your distro, adapt
  the rule (or use GROUP="input" if preferred).
• After these steps log out and back in (or reboot) so group membership takes effect.

Justness estimate: 92% — typical on most Linux distributions using udev.

"""

def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

#caps={ec.EV_KEY:ladder.ev_key_codes,ec.EV_REL:ladder.ev_rel_codes}

caps = {ec.EV_LED:ladder.ev_led_codes,ec.EV_KEY: ladder.ev_key_codes, ec.EV_REL: ladder.ev_rel_codes}

class PiedPiper(UInput):
    """class writing the mouse and keyboard events"""
    piper=None

    def __init__(S):
        if PiedPiper.piper:
            print(f'There should only bee one Pied Piper.')
            exit(666)
        try:
            super().__init__(caps,name="Pied Piper of Hamelin")
        except PermissionError as e:
            print(help_text)
            exit (e.errno)
        PiedPiper.piper=S
        #S.pressed_keys=None
        trace.open_window()
        atexit.register(S.leave_hamelin)

    def leave_hamelin(S):
        trace.close_window()
        S.close()
        print(f'Pied Piper left Hamelin.')

    def report_move(S,ev_code,ev_value):
        #print('-',end='',flush=True)
        S.write(ec.EV_REL,ev_code,ev_value)
        S.syn()
        S.syn_report()

    def syn_report(S):
        S.write(ec.EV_SYN,ec.SYN_REPORT,0)

    def squeak_event(S,event):
        #print(f'ratter squeak got {event}')
        S.write_event(event)
        S.syn()
        return S

    def squeak_code(S,ev_type,ev_code,ev_value):
        S.write(ev_type,ev_code,ev_value)
        S.syn()

    def default(S,event):
        print(toy.str_event(event))

    def simultaneous_keys(S,*args):
        # Press all keys
        # for key_code in args:
        #     S.write(ec.EV_KEY, key_code, 1)  # Key down
        # S.write(ec.EV_SYN, ec.SYN_REPORT, 0)
        # time.sleep(KEYDELAY)
        # # Release all keys
        # for key_code in args:
        #     S.write(ec.EV_KEY, key_code, 0)  # Key up
        # S.write(ec.EV_SYN, ec.SYN_REPORT, 0)
        # return  S
        S.press_and_hold(*args)
        time.sleep(KEYDELAY)
        S.release(*args)
        return S

    def type_key(S,key:int):
        '''
        simulate a single key or button press
        :param key: evdev.ecode.code of a key of button
        :type key: int
        :return: self
        :rtype: PiedPiper
        '''
        S.write(ec.EV_KEY,key,1)
        S.syn()
        time.sleep(KEYDELAY)
        S.write(ec.EV_KEY,key,0)
        S.syn()

    def press_and_hold(S,*args):
        '''
        press and hold a number of keys and/or buttons simultaneous.
        :param args: evdev.ecode.code of keys and/or buttons
        :type args: int
        :return: self
        :rtype: PiedPiper
        '''
        for key in args:
            S.write(ec.EV_KEY,key,1)
        S.syn()
        return S

    def release(S,*args):
        '''
        release keys/buttons previous pressed and hold
        :param args: keys/buttons to release
        :type args: int
        :return: self
        :rtype: PiedPiper
        '''
        for key in args:
            S.write(ec.EV_KEY,key,0)
        S.syn()
        return S

    def message(S,s):
        '''
        print a string as typed from a keyboard without capslock on.
        :param s: Ascii string to type
        :type s: str
        :return: self
        :rtype: PiedPiper
        '''
        for c in s:
            code,shift = asc2ev[ord(c)]
            if shift:
                S.simultaneous_keys(SHIFT,code)
                continue
            S.type_key(code)
        return S

    def nap(S,snooze=KEYDELAY):
        time.sleep(snooze)
        return S

    def id_active_window(S):
        return trace.active_window_name_and_classes()

    def match_active_window(S,name=None,class_name=None,class_class=None,show=False):
        n,cn,cc=trace.active_window_name_and_classes()
        if (not n) or (n == "Bad Window"):
            return False
        if show:
            print(f'"{n}","{cn}","{cc}"')
        if name and (not name in n ):
            return False
        if class_name and (not class_name in cn ):
            return False
        if class_class and (not class_class in cc):
            return False
        return True

    def id_mouse_window(S):
        return trace.mouse_over_window_name_and_classes()

# accepts only KEY_* events by default
# ui.write(e.EV_KEY, e.KEY_A, 1)  # KEY_A down
# ui.write(e.EV_KEY, e.KEY_A, 0)  # KEY_A up
# ui.syn()
#ui.closedef

def test_piper():
    piper=PiedPiper()
    #print(piper.capabilities())
    for i in range(1,20):
        piper.squeak_code(ec.EV_KEY, ec.KEY_1+i, 1)
        piper.squeak_code(ec.EV_KEY, ec.KEY_1+i, 0)
        time.sleep(.3)

    dirx=10
    diry=16
    for i in range(1,220):
        if i % 30 == 0:
            dirx=-dirx
        if i % 80 == 0:
            diry=-diry
        piper.report_move( ec.REL_X, dirx)
        piper.report_move( ec.REL_Y, diry)
        time.sleep(.3)
    #second_ratter=PiedPiper()

def test_message():
    ratter=PiedPiper()
    time.sleep(3)
    print('Message Start:')
    ratter.message('Hello World!')
    print('Message End:')

def test_trace():
    piper=PiedPiper()
    count = 5
    last=''
    while count>0:
        n,cn,cc=piper.id_active_window()
        if n != last:
            count-=1
            last=n
            print(f'{n},{cn},{cc}')

def test_hold_keys():
    time.sleep(3)
    piper=PiedPiper()
    ic(piper)
    piper.press_and_hold((ec.BTN_LEFT,ec.BTN_RIGHT))
    print(piper.device.active_keys(verbose=True))
    piper.message('<Buttons Pressed Message.>')
    piper.release((ec.BTN_RIGHT,ec.BTN_LEFT))
    print(piper.device.active_keys(verbose=True))
    time.sleep(3)

def main():
    #test_piper()
    #test_message()
    #test_trace()
    test_hold_keys()

if __name__=='__main__':
    main()
