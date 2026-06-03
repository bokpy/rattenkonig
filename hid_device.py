#!/bin/python3
import os
import sys
import threading
import evdev
from evdev import categorize,ecodes as ec
import re
import json
import time
from Xlib import X, display
import asyncio

from icecream import ic
ic.configureOutput(includeContext=True)

CONFIGDIR=os.path.expanduser("~/.config/rattenkonig/")
DETECTEDHIDS = None

if not os.path.exists(CONFIGDIR):
	os.makedirs(CONFIGDIR)

def get_abs_path(file):
	"""
	return the absolute path of file
	:param file:
	:return: file
	"""
	if os.path.islink(file):
		return os.path.realpath(file)
	return file

def get_active_class_class():
	d = display.Display()
	root = d.screen().root
	window_id_atom = d.get_atom('_NET_ACTIVE_WINDOW')
	window_id_prop = root.get_full_property(window_id_atom, X.AnyPropertyType)
	#ic(window_id_prop)
	if not window_id_prop:
		return (None,None)
	window_id = window_id_prop.value[0]
	window_obj = d.create_resource_object('window', window_id)
	cls_prop = window_obj.get_full_property(d.get_atom('WM_CLASS'), X.AnyPropertyType)
	if not cls_prop:
		return (None,None)
	cc = cls_prop.value.decode('utf-8', 'ignore')
	cc = cc.split('\x00')
	return ( cc[0],cc[1])

def name_event(event):
	#key event at 1779512964.993459, 274 (BTN_MIDDLE), up
	t = str(categorize(event))
	#ic(t)
	if 'key event at ' in t:
		t =  t.split('(')[1].split(')')[0].strip()
		if not ',' in t:
			return  t
		#['BTN_LEFT', 'BTN_MOUSE']
		return t[2:-2].replace("', '","_x_")
		#return t.split('(')[1].split(')')[0].strip()
	#relative axis event at 1779512961.547177, REL_Y
	elif  'relative axis' in t:
		return t.split(',')[1].strip()
	ic(t,event)
	return f'No Name: "{t}"'

class HidSet(set):
	def __init__(S,filepath):
		super().__init__(S)
		S.filepath=filepath
		#print(f'HidSet("{filepath}")')
		
	def show(S):
		for item in S:
			print(f'{item}')
	
	def writeset(S):
		try:
			with open(S.filepath, 'w') as f:
				json.dump(list(S),f)
		except Exception as e:
			print(f'writing "{S.filepath}" failed')
			ic(e)
			exit(1)
	
	def readset(S):
		if not os.path.isfile(S.filepath):
			print(f'No file "{S.filepath}"')
			return
			
		try:
			with open(S.filepath, 'r') as f:
				jsonlist=json.load(f)
		except Exception as e:
			print(f'Reading "{S.filepath}" failed.')
			ic(e)
			exit(1)
		for item in jsonlist:
			#print(f'\t{item=}')
			S.add(tuple(item))
		#S.show()

	def __set__(S):
		return S
	
	def stores_new(S,tup):
		"""
		store a tuple
		:return: True if new else False
		"""
		if tup in S:
			return False
		S.add(tup)
		return True

class HID_Device:
	def __init__(S,event_by_id,event_path=None):
		S.event_by_id = event_by_id
		if not event_path:
			event_path = get_abs_path('/dev/input/by-id/'+event_by_id)
			print(f'Event path: {event_path}')
		S.event_path = event_path
		S.configdir  = CONFIGDIR + event_by_id +'/'
		try:
			os.makedirs(S.configdir,exist_ok=True)
		except os.error as e:
			ic(e)
			exit(e.errno)
		S.eventset   = HidSet(S.configdir+'events.json')
		S.windowset  = HidSet(S.configdir+'windows.json')
		S.read_sets()
		S.inputdevice=None
		
	def __lt__(S,O):
		return S.event_by_id < O.event_by_id
		
	def connect(S):
		ic(S)
		if not S.inputdevice:
			S.inputdevice=evdev.InputDevice(S.event_path)
			S.inputdevice.grab()
			
	def disconnect(S):
		if not S.inputdevice:
			return
		S.inputdevice.ungrab()
		S.inputdevice.close()
		S.inputdevice=None
		
	def write_sets(S):
		S.windowset.writeset()
		S.eventset.writeset()

	def read_sets(S):
		S.windowset.readset()
		S.eventset.readset()
		
	def create_basic_file(S,configfile):
		def write_events(funcbase,f):
			for item in S.eventset:
				code,name = item
				f.write(f'\n{funcbase}{name}(event):')
				f.write(f'\n\treturn event')
				f.write(f'\n')
		try:
			with open(configfile,'w') as f:
				f.write(f'# rattenkonig config of "{S.event_by_id}"')
				f.write(f'\n# created: "{time.asctime()}"\n')
				
				funcbase="def act_"
				write_events(funcbase,f)
				for item in S.windowset:
					prime,secondary = item
					write_events(funcbase+prime+'_',f)
					if prime != secondary:
						write_events(funcbase+prime+'_'+secondary+'_',f)
		except os.error as e:
			ic(e)
			exit(e.errno)
	
	def update_config(S):
		configfile=S.configdir+'key_def.py'
		if not os.path.isfile(configfile):
			S.create_basic_file(configfile)
			return
			

	def end(S):
		S.ungrab()
		S.close()
	
	# async def call_me(S,action):
	# #def call_me(S):
	# 	try:
	# 		#async for event in dev.async_read_loop():
	# 		async for event in S.async_read_loop():
	# 			action(event)
	# 	except Exception as e:
	# 		ic(e)

def get_hid_devices():
	global DETECTEDHIDS
	DETECTEDHIDS=[]
	for by_id_path in os.listdir('/dev/input/by-id'):
		#print(f'{'/dev/input/by-id/'+by_id_path}')
		abs_path = get_abs_path('/dev/input/by-id/'+by_id_path)
		if '/dev/input/event' in abs_path:
			DETECTEDHIDS.append(HID_Device(event_by_id=by_id_path,event_path=abs_path))
	DETECTEDHIDS.sort()
	return DETECTEDHIDS

def main():
	get_hid_devices()
	for device in DETECTEDHIDS:
		print(device)

if __name__ == '__main__':
	main()