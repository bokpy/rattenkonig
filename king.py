#!/usr/bin/python3
from evdev import UInput, ecodes as ec, AbsInfo
import atexit
import time
from Xlib import display

import ladders as ladder
import toys as toy
from icecream import ic
ic.configureOutput(includeContext=True)

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
class MouseKing(UInput):
    """class writing the mouse and keyboard events"""
    the_king=None

    def __init__(S):
        if MouseKing.the_king:
            print(f'Only one mouse can bee the King')
            exit(666)
        try:
            super().__init__(caps,name="Ratoncito Perez")
            atexit.register(S.abdicate_crown)
        except PermissionError as e:
            print(help_text)
            exit (e.errno)
        MouseKing.the_king=S
        S.pressed_keys=None

    def abdicate_crown(S):
        S.close()
        print(f'Royal highness "{S.name}" abdicated.')

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

    def squeak_code(S,ev_type,ev_code,ev_value):
        S.write(ev_type,ev_code,ev_value)
        S.syn()

    def default(S,event):
        print(toy.str_event(event))
        #S.write_event(event)

    def hold_keys(S,house_mouse_id:int,keys:[int])-> None:
        pass
        # no hold keys pressed just press
        # if not S.pressed_keys_owner:
        #     S.pressed_keys_owner = house_mouse_id
        #     S.press_keys(keys)
        #     return
        # # an other mouse pressed the keys before so release them ad press what this mouse requests
        # if S.pressed_keys_owner != house_mouse_id:
        #     S.realese_keys()
        #     S.hold_keys(house_mouse_id,keys)
        #     return
        # # the pressed keys belong to the still active mouse
        # if S.pressed_keys == keys: # no changes return
        #     return
        # S.realese_keys()
        # S.hold_keys(house_mouse_id,keys)

    def realese_keys(S):
        pass
        # for key in S.pressed_keys:
        #     print(f'realese key[{key}]')
        #
        # S.pressed_keys=[]
        # S.pressed_keys_owner=None


# accepts only KEY_* events by default
# ui.write(e.EV_KEY, e.KEY_A, 1)  # KEY_A down
# ui.write(e.EV_KEY, e.KEY_A, 0)  # KEY_A up
# ui.syn()
#ui.close

def test_the_king():
    king=MouseKing()
    #print(king.capabilities())
    for i in range(1,20):
        king.squeak_code(ec.EV_KEY, ec.KEY_1+i, 1)
        king.squeak_code(ec.EV_KEY, ec.KEY_1+i, 0)
        time.sleep(.3)

    dirx=10
    diry=16
    for i in range(1,220):
        if i % 30 == 0:
            dirx=-dirx
        if i % 80 == 0:
            diry=-diry
        king.report_move( ec.REL_X, dirx)
        king.report_move( ec.REL_Y, diry)
        time.sleep(.3)
    #second_king=MouseKing()

def main():
    test_the_king()

if __name__=='__main__':
    main()
