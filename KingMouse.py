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



class KingMouse:
    """class writing the mouse and keyboard events"""
    one_king=False
    def __init__(S):
        """a new uinput"""
        if KingMouse.one_king:
            print(f'Only one mouse can bee the King')
            exit(1)
        KingMouse.one_king=True
        S.name = "King Mouse"
        S.pressed_keys=None
        S.# capabilities={}

        #check if the uinput device already exists
        # file_name = glob.glob('/dev/input/by-id/*King_Mouse*')
        # print(f'{file_name}')
        # if file_name:
        #     print (f'found "{file_name[0]}"')
        # devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        # for device in devices:
        #     # capabilities=merge_capabilities(capabilities,device.capabilities())
        #     # print(device.path, device.name, device.phys)
        #     # print(capabilities)
        #     if S.name == device.name:
        #         print(f'"{S.name}" existed.')
        #         S.ui_mouse=device
        #         return
        try:
            S.ui_mouse = evdev.UInput(name=S.name,vendor=0xb0b0,version=0xbbb)
        except PermissionError as e:
            print(help_text)
            exit (e.errno)
        atexit.register(S.close)

    def close(S):
        print(f'closing uinput mouse "{S.name}"')
        S.ui_mouse.close()

# accepts only KEY_* events by default
# ui.write(e.EV_KEY, e.KEY_A, 1)  # KEY_A down
# ui.write(e.EV_KEY, e.KEY_A, 0)  # KEY_A up
# ui.syn()
#ui.close

def main():
    spirit=KingMouse()
    #king2=KingMouse()
    time.sleep(10)
    # spirit.close()

if __name__=='__main__':
    main()
