#!/bin/python3
import os
import sys
import shutil
import importlib.util
import threading
import evdev
from evdev import AbsInfo,categorize,ecodes as ec
import re
import json
import time
from Xlib import X, display
#from Xlib.Xutil import StateMap
import argparse
import piper
import asyncio
import atexit

from event_config import *
from hid_set import HidSet

parser = argparse.ArgumentParser(
prog=os.path.basename(__file__),
description=f'Catches mouse and keyboard input events and then outputs events via an uinput device. '
			f'What output an event sends to the system can be programmed in a configuration file '
			f'per physical mouse device.'
	f'Use hid_device_setup.py to create a frame for a config file.',

epilog='Peep peep'
	)


parser.add_argument('-c','--configdir',
					help='directory where the configuration files are.',
					default='./configs/',
					nargs='?',
					action='store'
)

args = parser.parse_args()

from icecream import ic
ic.configureOutput(includeContext=True)

def JDUMP(jsn):
	print(json.dumps(jsn,indent=4))
	
def eat_all(*args):
	pass

PRINT=print 
PRINT=eat_all

CONFIGDIR         = None # args.configdir
# KEYSFILEPY        = 'key_def.py'
# KEYSFILE             = ' key_def'
# LOOKUP              = 'hid_lookup'
DETECTEDHIDS = None

CLASS_INDEX=0
TITLE_INDEX=1

CODE_INDEX=0
BUTTON_INDEX=1

#SENTINEL           = "~~~~~~ SENTINEL ~~~~~~"
# MARKER             =  "# ~~~ # "
# FNC                      =  'fnc_'
# DEF                      =  'def ' + FNC
# LDEF                    =  len(DEF)
# PARAMS             =  '(P,ev):'
# LPARAMS           =  len(PARAMS)
PIPER = piper.PiedPiper()

def import_from_path(module_name, file_path):
	#ic(module_name, file_path)
	file_path=os.path.abspath(file_path)
	spec = importlib.util.spec_from_file_location(module_name, file_path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[module_name] = module  # Registers it globally
	spec.loader.exec_module(module)
	return module


#re_def_fnc=re.compile(f'{DEF}\w+{PARAMS}$')
re_def_fnc=re.compile(r'def fnc_\w+\(P,ev\):')


def yn(true,yes,no):
	if true:
		return yes
	return no
		
re_one_char=re.compile(r'KEY_([A-Z])$',re.I)
re_title =re.compile(r':(\w+) ')

class HID_Device:
	trigger_events=(
	ec.EV_KEY
	 , ec.EV_ABS
	# , ec.EV_CNT
	# , ec.EV_FF
	# , ec.EV_FF_STATUS
	# , ec.EV_LED
	# , ec.EV_MAX
	# , ec.EV_MSC
	# , ec.EV_PWR
	 , ec.EV_REL
	# , ec.EV_REP
	# , ec.EV_SND
	# , ec.EV_SW
	# , ec.EV_SYN
	# , ec.EV_UINPUT
	# , ec.EV_VERSION
	)
	
	def __init__(S,event_by_id,event_path=None):
		S.event_by_id = event_by_id
		if not event_path:
			event_path = get_abs_path('/dev/input/by-id/'+event_by_id)
			print(f'Event path: {event_path}')
		S.event_path = event_path
		S.event_no= f'{int(re.search('[0-9]+$',S.event_path).group()):02d}'
		S.configdir  = CONFIGDIR + CamelCase(event_by_id) +'/'
		S.config_file_path=S.configdir+KEYSFILEPY
		PRINT(f'{S.config_file_path=}')
	
		try:
			os.makedirs(S.configdir,exist_ok=True)
		except os.error as e:
			ic(e)
			exit(e.errno)
		S.eventset      = HidSet(S.configdir+'events.json')
		S.windowset  = HidSet(S.configdir+'windows.json')
		S.read_sets()
		S.import_config() # sets S.lookup
		S.peek_info() # read S.capabilities, S.name and S.phys
		S.inputdevice=None
		
	def __str__(S):
		bid=S.event_by_id
		if len(bid)>20:
			bid = bid[:8]+'...'+bid[-8:]
		ev=int(S.event_path[16:])
		return f'HID_Device({ev:02d},"{bid}")'
		
	def __lt__(S,O):
		return S.event_by_id < O.event_by_id
	
	def peek_info(S):
		dev= evdev.InputDevice(S.event_path)
		S.capabilities=dev.capabilities()
		# print(f'\n\n{S.event_by_id}')
		# ic(S.capabilities)
		S.name=dev.name
		S.phys=dev.phys
		dev.close()
	
	def is_configured(S):
		return not S.lookup is None
	
	def clear_config(S):
		for file in os.listdir(S.configdir):
			dir_or_file=os.path.join(S.configdir,file)
			print(f'Clearing config: {os.path.join(S.configdir,file)}')
			try:
				os.remove(dir_or_file)
			except IsADirectoryError:
				shutil.rmtree(dir_or_file) # ignore_errors=True
				
		S.eventset.clear()
		S.windowset.clear()
	
	def import_config(S):
		if not os.path.isfile(S.config_file_path):
			#S.lookup=S.func_set=None
			S.lookup=None
			return False
		print(f'Import: "{S.config_file_path}"')
		try:
			key_def  = import_from_path(
				"key_def",S.config_file_path)
			S.lookup = key_def.hid_lookup
		except Exception as e:
			print(f'Import: "{S.config_file_path}" FAILED')
			ic(e)
			return False
		
		return True
	
	def connect(S):
		ic(S)
		if not S.inputdevice:
			try:
				S.inputdevice=evdev.InputDevice(S.event_path)
				S.inputdevice.grab()
			except OSError as e:
				ic(e)
				print('Do')
				print(f'sudo lsof {S.event_path}')
				print(f'sudo kill <PID>')
				exit(1)
		atexit.register(S.disconnect)
			
	def device(S):
		return S.inputdevice
			
	def disconnect(S):
		if not S.inputdevice:
			return
		S.write_sets()
		S.inputdevice.ungrab()
		S.inputdevice.close()
		S.inputdevice=None
		print(f'{S} disconnected')
		
	def write_sets(S):
		S.windowset.writeset()
		S.eventset.writeset()

	def read_sets(S):
		S.windowset.readset()
		S.eventset.readset()
		
	def config_update(S):
		updt =  EventFncConfig(S.config_file_path,S.eventset,S.windowset)
		updt.write_file()

	async def event_listener(S):
		# DOTS=90
		# _dot=DOTS
		async for event in S.inputdevice.async_read_loop():
			if not event.type in  HID_Device.trigger_events:
				#print(f'Reject {event.type}')
				continue
			#PRINT=yn(event.type == ec.EV_REL,print,eat_all)
			#print(f'event_listener {evdev.categorize(event)}')
			# continue
			code , event_name , clss , title=gen_code_key_class_title(event)
			keyCTC,keyCC,keyC=compose_3_sorting_keys(code,clss,title)
		
			action = S.lookup.get(keyCTC)
			if action:
				action(PIPER,event)
				continue
			action = S.lookup.get(keyCC)
			if action:
				action(PIPER,event)
				continue
			action = S.lookup.get(keyC)
			if action:
				action(PIPER,event)
				continue
			#
			# _dot-=1
			# if _dot < 0:
			# 	print(f'<')
			# 	_dot=DOTS
			# 	continue
			# print('.',end='',flush=True)

def get_hid_devices():
	global DETECTEDHIDS
	dev_paths = {path for path in evdev.list_devices()}
	# ic(dev_paths)
	DETECTEDHIDS=[]
	for by_id_path in os.listdir('/dev/input/by-id'):
		#print(f'{'/dev/input/by-id/'+by_id_path}')
		abs_path = get_abs_path('/dev/input/by-id/'+by_id_path)
		# if '/dev/input/event' in abs_path:
		# 	DETECTEDHIDS.append(HID_Device(event_by_id=by_id_path,event_path=abs_path))
		# print(f'"{abs_path}"')
		if abs_path in dev_paths:
			DETECTEDHIDS.append(HID_Device(event_by_id=by_id_path
										   ,event_path=abs_path))
	DETECTEDHIDS.sort()
	return DETECTEDHIDS

async def  hid_read_loop():
	global PIPER
	get_hid_devices()
	tasks=[PIPER.release_keys()]
	# loop = asyncio.new_event_loop()
	# loop.run_forever()
	for hid in DETECTEDHIDS:
		if hid.is_configured():
			hid.connect()
			tasks.append(hid.event_listener())
			print(f'{hid} task added')
	print(tasks)
	await asyncio.gather(*tasks)

def kill_switch():
	pid=os.getpid()
	print(f'Rattenkonig {pid} now on the trone', end='')
	home_dir=os.path.expanduser('~')
	bin_path=os.path.join(home_dir,'bin')
	paths=os.environ.get("PATH").split(':')
	if bin_path not in paths:
		tomcat=os.path.join(paths[0],'tomcat')
	else:
		tomcat=os.path.join(bin_path,'tomcat')
	
	print(f' can bee killed by "tomcat".')
	script=f'''#!/bin/bash
	if kill -SIGINT {pid} 2> /dev/null; then
		echo "Pied Piper Process {pid} killed successfully."
		#read
		exit
		fi
	echo "No Pied Piper process {pid} to kill"
	#read

	'''
	with open(tomcat, 'w') as f:
		f.write(script)
	os.chmod(tomcat, 0o755)
	atexit.register(os.remove,tomcat)
	return tomcat
	
def main():
	get_hid_devices()
	for hid in DETECTEDHIDS:
		hid.update_config()
		
def get_caps():
	get_hid_devices()
	caps={}
	for hid in DETECTEDHIDS:
		#print(f'{hid.capabilities=}')
		for key , item in hid.capabilities.items():
			if key == ec.EV_ABS:
				print(f'"{hid}"')
				print(f'ABS caps: {item}')
			if key not in caps:
				caps[key]=set(item)
			else:
				caps[key].update(item)
		
	for key , item in caps.items():
		#print (f"{key=}: {item=}")
		caps[key]=list(item)
	ic(caps)
	
	
if __name__ == '__main__':
	# test_proto_list()
	# exit(0)
	# # get_caps()
	# # exit(0)
	# # print( get_active_title_class_class())
	# # # get_active_title_class_class()
	# # test_update()
	# # exit(0)
	CONFIGDIR         = args.configdir
	if CONFIGDIR[-1:] != '/':
		CONFIGDIR+= '/'
	tomcat=kill_switch()
	try:
		asyncio.run(hid_read_loop())
	except KeyboardInterrupt:
		print(f'Terminated by KeyboardInterrupt')
	