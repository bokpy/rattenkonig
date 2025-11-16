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
        print (f'Free "{dev.name}"')
        dev.ungrab()

atexit.register(ungrab_devices)

def population_buildup():
    global event_to_mouse,mus_devices
    musculus_mice = mus.get_population()
    for mouse in musculus_mice:
        for event in mouse.events():
            mus_event_path=toy.event_path(event)
            dev=InputDevice(mus_event_path)
            dev.grab()
            mus_devices.append(dev)
            print(f'{mouse} {type(mouse)}')
            event_to_mouse[mus_event_path[-3:]]=mouse
    #ic(event_to_mouse)
    # for d in mus_devices:
    #     print(f"Found: {d.path} ({d.name})")

fired = '"pied Piper" you are fired'
async def read_device(dev):
    global event_to_mouse,mus_devices,fired
    try:
        async for event in dev.async_read_loop():
            exited_mouse = event_to_mouse[dev.path[-3:]]
            #print(f'{exited_mouse.name}')
            # ic(func)
            exited_mouse.event_action(event)
    except asyncio.exceptions.CancelledError as e:
        pass
    print(f'{fired}', end='', flush=True)
    fired = ' go'


async def main():
    global event_to_mouse,mus_devices
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

    population_buildup()
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print('.')
        print(f'KeyboardInterrupt')

