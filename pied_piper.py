#!/usr/bin/env python3
import asyncio, evdev
import asyncio
from evdev import InputDevice, categorize, ecodes, list_devices
import toys as toy
import musculus as mus
import mouseOptions
import atexit
args = mouseOptions.parser.parse_args()
from icecream import ic
import json

ic.configureOutput(includeContext=True)
DEBUG=print
event_to_mouse={}
mus_devices=[]
event_paths=[]

def ungrab_devices():
    global mus_devices
    for dev in mus_devices:
        print (f'Free: {dev}')
        dev.ungrab()

atexit.register(ungrab_devices)

async def read_device(dev):
    async for event in dev.async_read_loop():
        #print(dev.path)
        event_to_mouse[dev.path[-3:]].event_action(event)
        # if event.type == ecodes.EV_KEY:
        #     key_event = categorize(event)
        #     print(f"[{dev.name}] Key {key_event.keycode}: {key_event.keystate}")
        # elif event.type == ecodes.EV_REL:
        #     print(f"[{dev.name}] Relative movement: {event.code} -> {event.value}")
        # elif event.type == ecodes.EV_ABS:
        #     print(f"[{dev.name}] Absolute movement: {event.code} -> {event.value}")

async def main():
    global event_to_mouse,mus_devices
    musculus_mice = mus.get_population()

    for mouse in musculus_mice:
        for event in mouse.events():
            mus_event_path=toy.event_path(event)
            dev=InputDevice(mus_event_path)
            dev.grab()
            mus_devices.append(dev)
            event_to_mouse[mus_event_path[-3:]]=mouse

    ic(event_to_mouse)

    for d in mus_devices:
        print(f"Found: {d.path} ({d.name})")
    #input('just wait here')
    # adjust filter for only keyboard/mouse
    #devices = [d for d in devices if 'keyboard' in d.name.lower() or 'mouse' in d.name.lower()]
    tasks = [asyncio.create_task(read_device(d)) for d in mus_devices]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    if args.list:
        import pup
        pup.listMice(short=not args.verbose)
        exit(0)

    mus.set_config_dir(args.configdir)
    if args.template:
        import pup
        pup.set_config_dir(args.configdir)
        pup.make_a_litter()
        exit(0)
    asyncio.run(main())

