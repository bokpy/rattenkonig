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
import piper
import asyncio
import atexit

from icecream import ic
ic.configureOutput(includeContext=True)


CONFIGDIR         = "configs/"
KEYSFILEPY        = 'key_def.py'
KEYSFILE             = ' key_def'
LOOKUP              = 'hid_lookup'
DETECTEDHIDS = None

SENTINEL            = "~~~~~~ SENTINEL ~~~~~~"
FNC                      =  'fnc_'
DEF                      =  'def ' + FNC
LDEF                    =  len(DEF)
PARAMS             =  '(P,ev):'
LPARAMS           =  len(PARAMS)
PIPER = piper.PiedPiper()

if not os.path.exists(CONFIGDIR):
	os.makedirs(CONFIGDIR)
	
def file_header(name):
	return f'''# rattenkonig key button configuration
# date:  {time.asctime()}
id='{name}'

{LOOKUP}={{}}
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
			#print(f'No file "{S.filepath}"')
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
	
	def stores_new(S,tup):
		"""
		store a tuple
		:return: True if new else False
		"""
		if tup in S:
			return False
		S.add(tup)
		return True
	
class HidReadCopyConfig:
	def __init__(S,source_path,dest_file):
		if source_path and os.path.isfile(source_path):
			S.source=open(source_path,'r')
		else:
			S.source=None
		S.dest=dest_file
		S.current_func=None
		S.copy_to_first_function()
		
	def copy_to_first_function(S):
		if not S.source:
			S.current_func=SENTINEL
			return
		S.copy_to_next()
		
	def copy_to_next(S):
		if S.current_func:
			S.dest.write(S.current_func+'\n')
		while True:
			line = S.source.readline()
			print(f'line: "{line}"')
			if not line:
				S.current_func=SENTINEL
				return SENTINEL
			if line[:LDEF] is DEF:
				S.current_func=line.strip()
				return S.current_func
			S.dest.write(line)
			
	def advance_a_function(S):
		while True:
			yield S.current_func
			if S.current_func is SENTINEL:
				continue
			S.copy_to_next()
			
class FuntionPrototype:
	def __init__(S,code,key,primo='',secundo=''):
		S.key=key
		S.code=code
		S.primo=primo
		S.secundo=secundo
		
	def __lt__(S,O):
		if S.key != O.key:
			return S.key<O.key
		if S.primo != O.primo:
			return S.primo<O.primo
		return  S.secundo < O.secundo
	
	def __str__(S):
		primo_ = '' if S.primo=='' else '_'
		sec_ = '' if S.secundo =='' else '_'
		return f'def {FNC}{S.key}{primo_}{S.primo}{sec_}{S.secundo}{PARAMS} # {S.code}'
	
	def fnc_name(S):
		primo_ = '' if S.primo=='' else '_'
		sec_ = '' if S.secundo =='' else '_'
		return f'{FNC}{S.key}{primo_}{S.primo}{sec_}{S.secundo}'
	
	def fnc_key(S):
		return f'{S.code}{S.primo}{S.secundo}'
	
	def write_prototype(S,open_file):
		open_file.write(f'\n\n{str(S)}')
		open_file.write('\n\tpass')
		open_file.write(f'\n#{LOOKUP}[{S.fnc_key()}]={S.fnc_name()}')
		open_file.write(f'\n{LOOKUP}[{S.fnc_key()}]=None')

class HidFunctionYielder:

	def __init__(S,keyset,windowset):
		
		
		# find distinct secundos
		windows=list(windowset)
		windows.append(('',''))
		#windows.append((SENTINEL,SENTINEL))
		windows.sort()
		
		# if there is only one combination of class,class the
		# second class name is useless
		distinct=set()
		previous=(None,None)
		for proto in windows:
			if ( proto[0] is previous[0]) and not (proto[1] is previous[1]):
				distinct.add(proto)
			previous = proto
		
		# make the redundant class names '' so invisible
		for i in range(0,len(windows)):
			if windows[i][0]  not in distinct:
				windows[i]=(windows[i][0] ,'')
		
		# if there are distinct classes with the same name combined
		# with different second class names it is confiniend to
		# make a common root entry in the lookup
		
		for proto in distinct:
			windows.append((proto[0],''))
			
		poul = [
			FuntionPrototype (code, key, *wins)
			for  code, key in  keyset
			for wins in windows
		]
		
		poul.append(FuntionPrototype (0,SENTINEL,SENTINEL,SENTINEL))
		poul.sort()
		S.poul=poul
		S.current=None
	
	def next_event_func(S):
		for function in S.poul:
			S.current=function
			yield str(function)
		while True:
			yield S.current
	
	def write_prototype(S,f):
		S.current.write_prototype(f)
		
	# def trio_generator(S,code,key,prime='',second=''):
	# 	def ret(code,key,prime='',second=''):
	# 		p_='_'
	# 		if  prime == '':
	# 			p_=''
	# 		s_='_'
	# 		if second == '':
	# 			s_=''
	# 		func = f'{key}{p_}{prime}{s_}{second}'
	# 		#func = DEF+clean_function_name(func)+PARAMS
	# 		func = clean_function_name(func)
	# 		indice = f'{code}{prime}{second}'
	# 		return func,indice
	# 	yield ret(code,key)
	# 	yield  ret(code,key,prime)
	# 	yield  ret(code,key,prime,second)
	# 	raise StopIteration
	
	# def __next__(S):
	# 	for code,key in S.keys:
	# 		return ret(code,key)
	# 	for prim,sec in S.wins:
	# 		for code,key in S.keys:
	# 			return  ret(code,key,prim)
	# 			return  ret(code,key,prim,sec)
		
	# def key_def_func(S):
	# 	def ret(code,key,prime='',second=''):
	# 		p_='_'
	# 		if  prime == '':
	# 			p_=''
	# 		s_='_'
	# 		if second == '':
	# 			s_=''
	# 		func = f'{key}{p_}{prime}{s_}{second}'
	# 		#func = DEF+clean_function_name(func)+PARAMS
	# 		func = clean_function_name(func)
	# 		indice = f'{code}{prime}{second}'
	# 		return func,indice
	#
	# 	for code,key in S.keys:
	# 		yield ret(code,key)
	# 	for prim,sec in S.wins:
	# 		for code,key in S.keys:
	# 			yield  ret(code,key,prim)
	# 			yield  ret(code,key,prim,sec)
	#
	# 	#raise StopIteration
	#
class HID_Device:
	def __init__(S,event_by_id,event_path=None):
		S.event_by_id = event_by_id
		if not event_path:
			event_path = get_abs_path('/dev/input/by-id/'+event_by_id)
			#event_path = os.readlink(abs_p)
			print(f'Event path: {event_path}')
		S.event_path = event_path
		
		S.event_no= f'{int(re.search('[0-9]+$',S.event_path).group()):02d}'
		
		S.configdir  = CONFIGDIR + clean_function_name(event_by_id) +'/'
		#S.hash = str(hash(event_by_id))
		S.config_file_path=S.configdir+KEYSFILEPY
	
		try:
			os.makedirs(S.configdir,exist_ok=True)
		except os.error as e:
			ic(e)
			exit(e.errno)
		S.eventset      = HidSet(S.configdir+'events.json')
		S.windowset  = HidSet(S.configdir+'windows.json')
		S.read_sets()
		# ic(list(S.windowset))
		# S.eventset.show()
		S.import_config() # sets S.lookup
		#S.func_set = None
		#S.hash = str(hash(event_by_id))
		S.inputdevice=None
		
	def __str__(S):
		bid=S.event_by_id
		if len(bid)>20:
			bid = bid[:8]+'...'+bid[-8:]
		ev=int(S.event_path[16:])
		return f'HID_Device({ev:02d},"{bid}")'
		
	def __lt__(S,O):
		return S.event_by_id < O.event_by_id
	
	def is_configured(S):
		return not S.lookup is None
	
	def import_config(S):
		if not os.path.isfile(S.config_file_path):
			#S.lookup=S.func_set=None
			S.lookup=None
			return False
		print(f'Import: "{S.config_file_path}"')
		key_def  = import_from_path(
			"key_def",S.config_file_path)
		S.lookup = key_def.hid_lookup
		return True
	
	def connect(S):
		ic(S)
		if not S.inputdevice:
			S.inputdevice=evdev.InputDevice(S.event_path)
			S.inputdevice.grab()
			atexit.register(S.disconnect)
			
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
		
		def backup():
			i=1
			stam=S.config_file_path[:-3]
			while True:
				bckf=f'{stam}_{i:03d}bck.py'
				if not os.path.isfile(bckf):
					break
				i+=1
			os.rename(S.config_file_path,bckf)
			return bckf
		
		new_gen = HidFunctionYielder(S.eventset,S.windowset)
		func = new_gen.next_event_func()
		new=next(func )
		
		if not os.path.isfile(S.config_file_path):
			# Write a first configuration framework
			with open(S.config_file_path,'w') as f:
				f.write(file_header(S.event_by_id))
				while not SENTINEL in new:
					new_gen.write_prototype(f)
					new = next(func )
			return
		# merge sort old with new
		old_config_file = backup()
		with open(S.config_file_path,'w') as f:
			read_old=HidReadCopyConfig(old_config_file,f)
			old_func=read_old.advance_a_function()
			old = next(old_func)
			while not (  SENTINEL in old and  SENTINEL in new):
				if old is new:
					old   = next(old_func)
					new = next(func )
					continue
				if new < old:
					new_gen.write_prototype(f)
					new = next(func )
					continue
				old = next(old_func)
		

		# def update_config(S):
		# 	def backup():
		# 		i=1
		# 		stam=S.config_file_path[:-3]
		# 		while True:
		# 			bckf=f'{stam}_{i:03d}bck.py'
		# 			if not os.path.isfile(bckf):
		# 				break
		# 			i+=1
		# 		os.rename(S.config_file_path,bckf)
		# 		return bckf
		#
		# 	# def write_func( key,func,f):
		# 	# 	f.write(f'\n{DEF}{func}{PARAMS}')
		# 	# 	f.write('\n\tpass')
		# 	# 	f.write('\n')
		# 	# 	f.write(f'\n{LOOKUP}["{key}"]=None')
		# 	# 	f.write(f'\n# {LOOKUP}["{key}"]={FNC}{func}')
		# 	# 	f.write('\n')
		# 		#f.flush()
		#
		# 	old_config=None
		# 	if os.path.isfile(S.config_file_path):
		# 		old_config=backup()
		# 	with open(S.config_file_path,'w') as new_config:
		# 		if not old_config:
		# 			new_config.write(file_header(S.event_by_id))
		# 		old_gen   = HidReadCopyConfig(old_config,new_config)
		# 		new_gen = HidFunctionYielder(S.eventset,S.windowset)
		# 		last_read = old_gen.read_next()
		# 		for func,key in new_gen.key_def_func():
		# 			if last_read == func:
		# 				print(f'{func} was configure so copy')
		# 				last_read=old_gen.read_next()
		# 				continue
		# 			if func < last_read:
		# 				print(f'{func} is new')
		# 				write_func(key,func,new_config)
		# 				continue
		# 			#print(f'{last_readfunc} < {}' copy is new)
		# 			last_read=old_gen.read_next()
		# 		# don't forget the tail
		# 		while last_read != SENTINEL:
		# 			last_read=old_gen.read_next()
		
	async def event_listener(S):
		async for event in S.inputdevice.async_read_loop():
			# print(f'event_listener {evdev.categorize(event)}')
			# continue
			primo,secundo=get_active_class_class()
			code = str(event.code)
			print(f'{code},{primo},{secundo} -> {evdev.categorize(event)}')
			action = S.lookup.get(code + primo + secundo )
			if action:
				action(PIPER,event)
				continue
			action = S.lookup.get(code + primo )
			if action:
				action(PIPER,event)
				continue
			action = S.lookup.get(code  )
			if action:
				action(PIPER,event)
				continue
			ic(code,primo,secundo)
			name = name_event(event)
			S.eventset.stores_new((event.code,name))
			S.windowset.stores_new((primo,secundo))
			PIPER.squeak_event(event)

	async def event_listener_off(S):
		event = await  S.inputdevice.async_read()
		#print(f'event_listener {evdev.categorize(event)}')
		ic(event)
		# continue
		primo,secundo=get_active_class_class()
		code = str(event.code)
		print(f'{code},{primo},{secundo} -> {evdev.categorize(event)}')
		action = S.lookup.get(code + primo + secundo )
		if action:
			action(PIPER,event)
			return
		action = S.lookup.get(code + primo )
		if action:
			action(PIPER,event)
			return
		action = S.lookup.get(code  )
		if action:
			action(PIPER,event)
			return
		ic(code,primo,secundo)
		name = S.name_event(event)
		S.eventset.stores_new((event.code,name))
		S.windowset.stores_new((primo,secundo))
		PIPER.squeak_event(event)

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

def test_update():
	hid=HID_Device('usb-INSTANT_USB_GAMING_MOUSE-if01-event-kbd')
	print(hid.event_no)
	new_gen = HidFunctionYielder(hid.eventset,hid.windowset,sys.stdout)
	func = new_gen.next_event_func()
	read_func=HidReadCopyConfig('/home/bob/python/rattenkonig/configs/usb_INSTANT_USB_GAMING_MOUSE_if01_event_kbd/key_def_001bck.py',
	                  sys.stdout)
	old_func=read_func.advance_a_function()
	
	old = next(old_func);new=next(func )
	while not (  SENTINEL in old and  SENTINEL in new):
		if old is new:
			old = next(old_func)
			new = next(func )
			continue
		if new < old:
			new_gen.write_prototype()
			new = next(func )
			continue
		old = next(old_func)

async def  hid_read_loop():
	get_hid_devices()
	tasks=[]
	# loop = asyncio.new_event_loop()
	# loop.run_forever()
	for hid in DETECTEDHIDS:
		if hid.is_configured():
			hid.connect()
			tasks.append(hid.event_listener())
			print(f'{hid} task added')
	await asyncio.gather(*tasks)
	
def main():
	get_hid_devices()
	for hid in DETECTEDHIDS:
		hid.update_config()
			
if __name__ == '__main__':
	# test_update()
	# exit(0)
	
	try:
		asyncio.run(hid_read_loop())
	except KeyboardInterrupt:
		print(f'{sys.argv[0]} KeyboardInterrupt')