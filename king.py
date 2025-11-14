#!/usr/bin/python3
"""
Create a virtual Uinput device to send (modified) events form
the real mouse devices
"""
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
import evdev
import glob
import atexit
# import UInput, ecodes as e
import time
from Xlib import display

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

class MouseKing:
    """class writing the mouse and keyboard events"""
    the_king=None
    def __init__(S):
        """a new uinput"""
        if MouseKing.the_king:
            print(f'Only one mouse can bee the King')
            exit(1)
        MouseKing.the_king=S
        S.name = "Ratoncito Perez"
        S.pressed_keys_owner=None
        S.pressed_keys=None

        try:
            S.ui_mouse = evdev.UInput(name=S.name,vendor=0xb0b0,version=0xbbb)
        except PermissionError as e:
            print(help_text)
            exit (e.errno)
        atexit.register(S.close)

    def close(S):
        print(f'closing uinput mouse "{S.name}"')
        S.ui_mouse.close()

    def default(S,event):
        print(f'King Default got {event}')

    def hold_keys(S,house_mouse_id:int,keys:[int])-> None:
        # no hold keys pressed just press
        if not S.pressed_keys_owner:
            S.pressed_keys_owner = house_mouse_id
            S.press_keys(keys)
            return
        # an other mouse pressed the keys before so release them ad press what this mouse requests
        if S.pressed_keys_owner != house_mouse_id:
            S.realese_keys()
            S.hold_keys(house_mouse_id,keys)
            return
        # the pressed keys belong to the still active mouse
        if S.pressed_keys == keys: # no changes return
            return
        S.realese_keys()
        S.hold_keys(house_mouse_id,keys)

    def realese_keys(S):
        for key in S.pressed_keys:
            print(f'realese key[{key}]')
        S.pressed_keys=[]
        S.pressed_keys_owner=None

    def write_event(S,house_mouse_id:int,event:evdev.events.InputEvent)->None:
        print(f'MouseKing.write: {event}')

# accepts only KEY_* events by default
# ui.write(e.EV_KEY, e.KEY_A, 1)  # KEY_A down
# ui.write(e.EV_KEY, e.KEY_A, 0)  # KEY_A up
# ui.syn()
#ui.close

def main():
    spirit=MouseKing()
    #king2=MouseKing()
    time.sleep(10)
    # spirit.close()

if __name__=='__main__':
    main()
