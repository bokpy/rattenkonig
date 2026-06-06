#!/bin/python3
import os
import sys
import shutil
#from collections import OrderedDict
#import importlib
import importlib.util
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


CONFIGDIR="configs/"
KEYSFILEPY='key_def.py'
KEYSFILE='key_def'
LOOKUP='hid_lookup'
DETECTEDHIDS = None


if not os.path.exists(CONFIGDIR):
	os.makedirs(CONFIGDIR)
	
HIDLOOKUPMARK='TABLE START'

FILE_MARK=f"""
'''{HIDLOOKUPMARK}
Don't put new code below here.
It wil be lost by a config update.
only edit the hid_lookup dict
set 'func' value to a fnc_name to make it execute
when the conditions of that level are met.
the 'active' value is the function intendeded
for the level but everything is possible
'''
"""

def file_header(name):
	return f'''# rattenkonig key button configuration
# date:  {time.asctime()}
id='{name}'
'''
def import_from_path(module_name, file_path):
	ic(module_name, file_path)
	file_path=os.path.abspath(file_path)
	spec = importlib.util.spec_from_file_location(module_name, file_path)
	module = importlib.util.module_from_spec(spec)
	sys.modules[module_name] = module  # Registers it globally
	spec.loader.exec_module(module)
	return module

def make_config_dir(d,content=None):
	os.makedirs(d, exist_ok=True)
	try:
		with open(d + '__init__.py', 'w') as f:
			if content:
				f.write('\n')
				f.write(content)
				f.write('\n')
	except Exception as e:
		ic(e)
		exit(1)
	return os.path.abspath(d)+'/'

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

def clean_function_name(name):
	name = re.sub(r"[!-/:-@[-`{-~]", '_',name)
	name = re.sub('[^A-Za-z0-9_]', '', name)
	return name

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
	
	def read_sorted_list(S):
		"""
		reads the list from S.filepath
		and returns it as a sorted list
		:return: sorted list | None
		"""
		if not os.path.isfile(S.filepath):
			print(f'read_sorted_list No file "{S.filepath}"')
			return None
			
		try:
			with open(S.filepath, 'r') as f:
				jsonlist=json.load(f)
		except Exception as e:
			print(f'Reading "{S.filepath}" failed.')
			ic(e)
			exit(1)
		jsonlist.sort()
		ic(jsonlist)
		return jsonlist
		
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
		S.configdir  = CONFIGDIR + clean_function_name(event_by_id) +'/'
		S.hash = str(hash(event_by_id))
		S.config_file_path=S.configdir+KEYSFILEPY
	
		try:
			os.makedirs(S.configdir,exist_ok=True)
		except os.error as e:
			ic(e)
			exit(e.errno)
		S.eventset      = HidSet(S.configdir+'events.json')
		S.windowset  = HidSet(S.configdir+'windows.json')
	
		S.read_sets()
		# S.windowset.show()
		# S.eventset.show()
		S.hash = str(hash(event_by_id))
		S.import_config() # sets S.lookup and S.func_list
		S.inputdevice=None
		
	def __str__(S):
		bid=S.event_by_id
		if len(bid)>20:
			bid = bid[:8]+'...'+bid[-8:]
		ev=int(S.event_path[16:])
		return f'HID_Device({ev:02d},"{bid}")'
		
	def __lt__(S,O):
		return S.event_by_id < O.event_by_id
	
	def configured(S):
		return S.lookup != None
	
	def import_config(S):
		if not os.path.isfile(S.config_file_path):
			S.lookup=S.func_list=None
			return
		print(f'Exists: "{S.config_file_path}"')
		libpath=os.path.realpath(S.configdir)
		sys.path.append(libpath)
		key_def  = import_from_path(
			"key_def",S.config_file_path)
		S.lookup = key_def.hid_lookup
		S.func_list= [ x for x in dir(key_def) if x[:4] == 'fnc_' ]
		print(f'{key_def.id} key_def.id ')
		print(f'{S.event_by_id} S.event_by_id ')
		if key_def.id != S.event_by_id:
			ic(key_def.id ,S.event_by_id)
			exit(112)
		ic(S.func_list)
		sys.path.remove(libpath)
	
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
	
	def funcion_triplet(S,code, key, prime, second):
		"""
		Just makeup names for the keystroke
		functions to bind to events in active windows
		:param code:   evdev event.code not used
		:param key:    ecodes.key button name
		:param prime:  first  class of active window
		:param second: second class of active window
		:return: 3 derived function names
		"""
		#print(f'{code},{key},{prime},{second}')
		clean_prime   = clean_function_name(prime)
		clean_second = clean_function_name(second)
		root         = 'fnc_'+key
		child        = 'fnc_'+clean_prime+'_'+key
		grand_child  = 'fnc_'+clean_prime+'_'+clean_second+'_'+key
		return root,child,grand_child

	def create_naming_dict(S,only_new=False):
		"""
		combine the eventset with the windowset to
		a dictionary
		:param only_new:  store only funtions not in found in key_def.py
		:return:  dictionary code -> prime class -> sub class
		"""
		
		#ic()
		event_dict={}
		
		def store_triplet(code,key,prime,second):
			root,child,grand_child=S.funcion_triplet(code,key,prime,second)
			if only_new and grand_child in S.func_list:
				return
			print(f'{code},{key},{prime},{second}')
			if not code in event_dict:
				event_dict[code]\
					={'func': None ,'active': root}
			event_dict[code][prime]=\
				{'func':None ,'active' : child}
			event_dict[code][prime][second]=\
				{'func': None,'active' : grand_child}
			
		for prime,second in S.windowset:
			for code,event_name in S.eventset:
				store_triplet(code,event_name,prime,second)
		#print(json.dumps(event_dict,indent=4))
		return event_dict
	
	def write_configuration_dict(S,d,f,name):
		def tabs(level):
			return '\n'+'\t' * level
			
		f.write(f'\n{name}={{')
		
		def write_level(d,level=0):
			_tabs=tabs(level)
			comma=''
			for key in d:
				if level > 0:
					f.write(f'{_tabs}{comma}"{key}":')
				else:
					f.write(f'{_tabs}{comma}{key}:')
					
				if isinstance(d[key],dict):
					f.write('{')
					write_level(d[key],level+1)
				else:
					f.write(f'{d[key]}')
				comma=','
			f.write(f'{_tabs}}}')
		write_level(d)
		#f.write('\n}')
	
	def write_func_def(S,name,f):
		if S.func_list and name in S.func_list:
			return
		f.write(f'\ndef {name}(P,ev):')
		f.write(f'\n\tpass')
		f.write('\n')
	
	def write_func_defs(S,f):
		code_keys=S.eventset.read_sorted_list()
		##ic(code_keys)
		if not code_keys:
			return
		
		windows = S.windowset.read_sorted_list()
		ic(windows)
		##ic(windows)
		if not windows:
			return
		
		for code,key in code_keys:
			root,_child,_grand_child=S.funcion_triplet(code,key,'null','null')
			S.write_func_def(root,f)
		
		for prime,second in windows:
			#ic(prime,second)
			for code,key in code_keys:
				_root,child,grand_child=S.funcion_triplet(code,key,prime,second)
				S.write_func_def(child,f)
				S.write_func_def(grand_child,f)
				
	def create_first_config(S):
		text=f'''
		\n"""configuration and data of hid {S.event_by_id}."""
		__version__ = "1.0.0"
		__author__ = "B. van der Burg"
		PACKAGE_NAME = "rattenkonig"
		'''
		make_config_dir(S.configdir,text)
		with open(S.config_file_path,'w') as f:
			f.write(file_header(S.event_by_id))
			S.write_func_defs(f)
			d=S.create_naming_dict()
			f.write(FILE_MARK)
			S.write_configuration_dict(d,f,LOOKUP)
			
	def update_config(S):
		def backup():
			i=1
			stam=S.config_file_path[:-3]
			while True:
				bckf=f'{stam}_{i:03d}bck.py'
				if not os.path.isfile(bckf):
					break
				i+=1
			shutil.copy(S.config_file_path,bckf)
		
		def append_new():
			if not S.lookup:
				S.import_config()
			new_dict =  S.create_naming_dict(only_new=True)
			if not new_dict:
				return
			backup()
			with open(S.config_file_path,'r') as f:
				code_text=f.read()
			lines=code_text.split('\n')
			line_iter=iter(lines)
			with open(S.config_file_path,'w') as f:
				try:
					while True:
						line = next(line_iter)
						if "'''TABLE START" in line:
							break
						f.write(line)
						f.write('\n')
						print(line)
				except StopIteration:
					ic(f'Demaged "{S.config_file_path}')
					exit(414)
					
				f.write(f'\n#appended {time.asctime()}\n')
				S.write_func_defs(f)
				f.write(FILE_MARK)
				try:
					while True:
						line = next(line_iter)
						if  LOOKUP+'={' in line:
							while True:
								f.write(line)
								f.write('\n')
								print(line)
								line = next(line_iter)
				except StopIteration:
					pass
				f.write(f'\n#appended {time.asctime()}\n')
				dict_to_add=f'append_{LOOKUP}'
				S.write_configuration_dict(new_dict,f,dict_to_add)
				f.write(f'\n{LOOKUP}.update({dict_to_add})\n')

		if len(S.eventset) == 0:
			#ic(S.eventset)
			return
		if not os.path.isfile(S.config_file_path):
			S.create_first_config()
			return
		
		append_new()
		
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
		# d=device.create_naming_dict()
		# device.write_func_defs()
		# device.write_configuration_dict(d)
		device.update_config()
		print(device)

if __name__ == '__main__':
	main()