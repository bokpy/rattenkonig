#!/usr/bin/env python3
import asyncio, evdev
#import asyncio
import os
import signal
import sys
#import psutil
#from logging import exception

import time
from evdev import InputDevice, categorize, ecodes as ec, list_devices
import toys as toy
from tricks import service_call
import troupe as act
import mouseOptions
import notify2
from Xlib import X, display
from Xlib.ext import randr
import atexit
args = mouseOptions.parser.parse_args()
import json

from icecream import ic
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

def send_notification():
	# Initialize the notification system
	notify2.init("Pied Piper")
	# Create a notification object
	# Format: notify2.Notification("Title", "Message", "Icon Path")
	n = notify2.Notification("Pied Piper"," is playing","/home/bob/python/rattenkonig/Pied Piper 3.png")
	#n.set_timeout(notify2.EXPIRES_NEVER) #   Set the display duration in milliseconds, or one of the special values EXPIRES_DEFAULT or EXPIRES_NEVER. # Show the notification
	n.set_timeout ( 1000 * 25)
	n.show()
	atexit.register(send_notification)

def kill_device_blocking_pids():
	dev_path_by_id  = '/dev/input/by-id/'
	pids = set()
	for file in  os.listdir(dev_path_by_id):
		lsof = service_call('lsof',dev_path_by_id + file,print_error=False)
		if lsof:
			pid_line=lsof[1].split()
			pids.add(int(pid_line[1]))
	for pid in pids:
		print(f'Remove blocking Rattenkonig {pid=}')
		os.kill(pid, signal.SIGTERM)
		time.sleep(.4)

# def get_active_window_info():
# 	d = display.Display()
# 	root = d.screen().root
# 	# Get the atom for the active window
# 	window_id_atom = d.get_atom('_NET_ACTIVE_WINDOW')
# 	window_id_prop = root.get_full_property(window_id_atom, X.AnyPropertyType)
# 	if not window_id_prop:
# 		return ('Bad','Bad','Bad')
# 	window_id = window_id_prop.value[0]
# 	window_obj = d.create_resource_object('window', window_id)
# 	# Get Window Title
# 	# We check both _NET_WM_NAME (UTF-8) and WM_NAME (STRING)
# 	title = "Unknown"
# 	for atom_name in ['_NET_WM_NAME', 'WM_NAME']:
# 		atom = d.get_atom(atom_name)
# 		prop = window_obj.get_full_property(atom, 0)
# 		if prop:
# 			title = prop.value
# 			if isinstance(title, bytes):
# 				title = title.decode('utf-8', 'ignore')
# 			break
# 	# Get Window Class
# 	# WM_CLASS usually returns a list/tuple: (instance, class)
# 	cls_prop = window_obj.get_full_property(d.get_atom('WM_CLASS'), X.AnyPropertyType)
# 	#cls_prop:
# 	# <GetProperty serial = 23
# 	# , data = {'sequence_number': 23
# 	# , 'property_type': 31
# 	# , 'bytes_after': 0
# 	# , 'value': (8, b'jetbrains-pycharm\x00jetbrains-pycharm\x00')}
# 	# , error = None>
# 	wininf = (title ,'','')
# 	if not cls_prop:
# 		return wininf
# 	cc = cls_prop.value.decode('utf-8', 'ignore')
# 	#print(f'{cc=}')
# 	cc = cc.split('\x00')
# 	return ( title,cc[0],cc[1])

def check_alarm( event):
	global stopper_count, stopper_limit
	if event.code != stopper_key:
		stopper_count = stopper_limit
		return
	if event.code == stopper_key and event.value == 1:
		stopper_count -= 1
		#print(f'{stopper_count=}')
		if stopper_count < 0:
			#ic('stopped by repeated Middle Button presses.')
			raise CloseCircus

def ungrab_devices():
	global troupe_devices
	print('\nMouse sabbatical')
	for dev in troupe_devices:
		print (f'Free "{dev.name}"')
		dev.ungrab()
		dev.close()

fired = '"Pied Piper" you are fired'
async def read_device(dev):
	global fd_to_troupe,troupe_devices,fired
	try:
		async for event in dev.async_read_loop():
			if event.type == ec.EV_KEY:
				check_alarm(event)
			fd_to_troupe[dev.fd].magic_tricks[event.type][event.code](event)
	except KeyError as e:
		ic(e)
		print(f'Mouse: {fd_to_troupe[dev.fd].name=} {dev.fd=}')
		print(f'No entry for event{event} = {toy.str_event(event)}')
		raise
	except asyncio.exceptions.CancelledError as e:
		ic(e)
		pass
	except CloseCircus:
		ic('CloseCircus')
		print("Time to leave.")
		raise
	except Exception as e:
		ic(e)
		troupe=fd_to_troupe[dev.fd]
		print(f'troupe"{troupe.name}" {toy.str_event(event)} ')
		raise

	print(f'{fired}', end='', flush=True)
	fired = ' go' # repeated for each device

async def main_runner():
	global fd_to_troupe,troupe_devices
	send_notification()
	#ic(troupe_devices)
	tasks = [asyncio.create_task(read_device(d)) for d in troupe_devices]
	try:
		await asyncio.gather(*tasks)
	except Exception as e:
		ic(e)
		raise
	except CloseCircus:
		print("Circus Got Closed.") #return from async def main_runner()")
		return

def kill_switch():
	pid =os.getpid()
	print(f'Rattenkonig {pid} now on the trone',end='')
	home_dir = os.path.expanduser('~')
	paths =  os.environ.get("PATH")
	use_path = None
	for path in paths.split(":"):
		if home_dir in path and os.path.isdir(path):
			use_path = path
			break
	if not use_path:
		print ('.')
		return
	kill_file = use_path + '/tomcat'
	print(f' can bee killed by "tomcat".')
	script = f'''
	#!/bin/bash
	if kill  { pid } 2> /dev/null; then
		echo "Pied Piper Process {pid} killed successfully."
		exit
		fi
	echo "No Pied Piper process {pid} to kill"
	
	'''
	
	with open(kill_file, 'w') as f:
		f.write(script )
	os.chmod(kill_file, 0o755)
	print(f'{kill_file=}')
	atexit.register(os.unlink, kill_file)
	
def main():
	global  troupe_devices,fd_to_troupe
	kill_device_blocking_pids() # kill old process
	# that is blocking input devices
	circus=act.MouseCircus()
	troupe_devices=[]
	fd_to_troupe={}
	for ensemble in circus:
		if not ensemble.is_preforming():
			continue
		for mouse in ensemble.actors():
			event_path=toy.event_path(mouse.event)
			device=evdev.InputDevice(	event_path)
			try:
				device.grab()
			except OSError as e:
				ic(e)
				raise
			troupe_devices.append(device)
			fd_to_troupe[device.fd]=ensemble
	atexit.register(ungrab_devices)
	print('\nstop is repeat "middle button"')
	try:
		asyncio.run(main_runner())
	except Exception as e:
		print('asyncio.run(main_runner()) done')
		ic(e)

if __name__ == "__main__":
	# inf = get_active_window_info()
	# ic(inf)
	# exit(0)
	print(f'{sys.argv}')
	if args.list:
		import litter
		litter.listMice(short=not args.verbose)
		exit(0)

	if args.windows:
		from tracer import show_pointed_windows
		show_pointed_windows()
		exit(0)

	if args.keys:
		from pinky import keystoke_tester
		keystoke_tester()
		exit(0)

	act.set_config_dir(args.configdir)
	if args.template:
		import litter
		litter.set_config_dir(args.configdir)
		tribes=litter.Tribes()
		tribes.make_templates()
		exit(0)
		
	kill_switch()
	main()
