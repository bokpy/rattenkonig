#!/usr/bin/python3
from evdev import UInput, ecodes as ec, AbsInfo
import atexit
import time
from Xlib import display
import ladders as ladder
from ladders import ascii_to_evdev as asc2ev
import toys as toy
from icecream import ic
ic.configureOutput(includeContext=True)
KEYDELAY=.01
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

def get_focused_window():
    """
    Gets the currently focused window using Xlib.
    Returns the window ID as an integer, or None if no window has focus.
    """
    try:
        d = display.Display()
        window = d.get_input_focus().focus
        if window != 0:
            return window
        else:
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        if 'd' in locals():
            d.close()

def get_window_info(window):
    if window==0:
        return [0,None,None,None]
    return [window,window.get_wm_name()] + list(window.get_wm_class())

caps={ec.EV_KEY:ladder.ev_key_codes,ec.EV_REL:ladder.ev_rel_codes}
class PiedPiper(UInput):
    """class writing the mouse and keyboard events"""
    piper=None

    def __init__(S):
        if PiedPiper.piper:
            print(f'There should only bee one Pied Piper.')
            exit(666)
        try:
            super().__init__(caps,name="Pied Piper of Hamelin")
            atexit.register(S.abdicate_crown)
        except PermissionError as e:
            print(help_text)
            exit (e.errno)
        PiedPiper.piper=S
        S.pressed_keys=None

    def abdicate_crown(S):
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
        #print(f'King squeak got {event}')
        S.write_event(event)
        S.syn()
        return S

    def squeak_code(S,ev_type,ev_code,ev_value):
        S.write(ev_type,ev_code,ev_value)
        S.syn()

    def default(S,event):
        print(toy.str_event(event))

    def juggle_keys(S,keys):
        # Press all keys
        for key_code in keys:
            S.write(ec.EV_KEY, key_code, 1)  # Key down
            S.write(ec.EV_SYN, ec.SYN_REPORT, 0)
            time.sleep(KEYDELAY)
        # Release all keys
        for key_code in keys:
            S.write(ec.EV_KEY, key_code, 0)  # Key up
            S.write(ec.EV_SYN, ec.SYN_REPORT, 0)
            time.sleep(KEYDELAY)
        return  S

    def type_key(S,key):
        S.write(ec.EV_KEY,key,1)
        S.write(ec.EV_SYN, ec.SYN_REPORT, 0)
        time.sleep(KEYDELAY)
        S.write(ec.EV_KEY,key,0)
        S.write(ec.EV_SYN, ec.SYN_REPORT, 0)
        time.sleep(KEYDELAY)

    def press_and_hold(S,keys):
        if not is_iterable(keys):
            keys=[keys]
        for key in keys:
            S.write(ec.EV_KEY,key,1)
            S.write(ec.EV_SYN, ec.SYN_REPORT, 0)
            #time.sleep(KEYDELAY)
        #S.syn()
        return S

    def release(S,keys):
        if not is_iterable(keys):
            keys=[keys]
        for key in keys:
            S.write(ec.EV_KEY,key,0)
            S.write(ec.EV_SYN, ec.SYN_REPORT, 0)
        #time.sleep(KEYDELAY)
        #S.syn()
        return S

    def message(S,s):
        for c in s:
            code,shift = asc2ev[ord(c)]
            if shift:
                S.juggle_keys([SHIFT,code])
                continue
            S.type_key(code)
        return S

    def nap(S,snooze=KEYDELAY):
        time.sleep(snooze)
        return S

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
    #second_king=PiedPiper()

def test_message():
    king=PiedPiper()
    time.sleep(3)
    print('Message Start:')
    king.message('Hello World!')
    print('Message End:')

def main():
    #test_piper()
    test_message()

if __name__=='__main__':
    main()
