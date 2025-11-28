#!/usr/bin/env python3
import asyncio, evdev
import asyncio
from evdev import InputDevice, categorize, ecodes as ec, list_devices
import toys as toy
import troupe as act
import mouseOptions
import atexit
args = mouseOptions.parser.parse_args()
from icecream import ic
import json

ic.configureOutput(includeContext=True)
DEBUG=print
fd_to_troupe={}
troupe_devices=[]
event_paths=[]

stopper_limit = 5
stopper_count = stopper_limit
stopper_key=ec.BTN_MIDDLE

class CloseCircus(Exception):
    pass

def check_alarm( event):
    global stopper_count, stopper_limit
    if event.code != stopper_key:
        stopper_count = stopper_limit
        return
    if event.code == stopper_key and event.value == 1:
        stopper_count -= 1
        print(f'{stopper_count=}')
        if stopper_count < 0:
            #ic('stopped by repeated Middle Button presses.')
            raise CloseCircus

def ungrab_devices():
    global troupe_devices
    print('Mouse sabbatical')
    for dev in troupe_devices:
        print (f'Free "{dev.name}"')
        dev.ungrab()
        dev.close()

fired = '"pied Piper" you are fired'
async def read_device(dev):
    global fd_to_troupe,troupe_devices,fired
    try:
        async for event in dev.async_read_loop():
            if event.type == ec.EV_KEY:
                check_alarm(event)

            fd_to_troupe[dev.fd].magic_tricks[event.type][event.code](event)

    except asyncio.exceptions.CancelledError as e:
        pass
    except KeyError as e:
        print(f'{dev.fd=} {toy.str_event(event)}')
        raise
    except CloseCircus:
        print("Time to leave.")
        raise
    print(f'{fired}', end='', flush=True)
    fired = ' go'

async def main_runner():
    global fd_to_troupe,troupe_devices
    #ic(troupe_devices)
    tasks = [asyncio.create_task(read_device(d)) for d in troupe_devices]
    try:
        await asyncio.gather(*tasks)
    except CloseCircus:
        print("Circus Got Closed.") #return from async def main_runner()")
        return

def main():
    global  troupe_devices,fd_to_troupe
    circus=act.MouseCircus()
    troupe_devices=[]
    fd_to_troupe={}
    for ensemble in circus:
        if not ensemble.is_preforming():
            continue
        for mouse in ensemble.actors():
            device=evdev.InputDevice(toy.event_path(mouse.event))
            device.grab()
            troupe_devices.append(device)
            fd_to_troupe[device.fd]=ensemble
    atexit.register(ungrab_devices)
    #vfvfvfvfvfprint('\nasyncio.run(main_runner()) start')
    try:
        asyncio.run(main_runner())
    except Exception as e:
        print('asyncio.run(main_runner()) done')
        ic(e)

if __name__ == "__main__":
    if args.list:
        import litter
        litter.listMice(short=not args.verbose)
        exit(0)

    if args.windows:
        from tracer import show_pointed_windows
        show_pointed_windows()
        exit(0)

    act.set_config_dir(args.configdir)
    if args.template:
        import litter
        litter.set_config_dir(args.configdir)
        tribes=litter.Tribes()
        tribes.make_templates()
        exit(0)

    main()


