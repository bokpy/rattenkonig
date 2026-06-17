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
#from Xlib.Xutil import StateMap
import piper
import asyncio
import atexit
from X11_Utils import get_active_title_class_class

from icecream import ic
ic.configureOutput(includeContext=True)

def JDUMP(jsn):
	print(json.dumps(jsn,indent=4))

CONFIGDIR         = "configs/"
KEYSFILEPY        = 'key_def.py'
KEYSFILE             = ' key_def'
LOOKUP              = 'hid_lookup'
DETECTEDHIDS = None

CLASS_INDEX=0
TITLE_INDEX=1

CODE_INDEX=0
BUTTON_INDEX=1

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

re_square_bracket=re.compile(r'\[([^,]+),')
re_parentheses=re.compile(r'\(([^)]+)\)')
re_relative=re.compile(r'(rel_[_a-z]+)')

def name_event(event):
# 	def match_square_brackets(strng):
# 		splt1=strng.split('[')
# 		if len(splt1) < 2:
# 			return None
# 		splt2=splt1[1].split(']')
# 		if len(splt2) < 2:
# 			return None
# 		splt3=splt2[0].split(',')
# 		return splt3[0].strip()
#
# 	def match_parentheses(strng):
# 		splt1=strng.split('(')
# 		if len(splt1) < 2:
# 			return None
# 		splt2=splt1[1].split(')')
# 		if len(splt2) < 2:
# 			return None
# 		return splt2[0]
#
	# key event at 1779512964.993459, 274 (BTN_MIDDLE), up
	# relative axis event at 1781505193.907004, REL_Y
	cat_event = str(categorize(event)).lower()
	ic(cat_event)
	if 'key event at ' in cat_event:
		
		match=re_square_bracket.findall(cat_event)
		ic(match)
		if match:
			return match[0].strip("'")
			
		match=re_parentheses.findall(cat_event)
		ic(match)
		if match:
			return match[0]
		return 'failed about 124'
	match = re_relative.findall(cat_event)
	if match:
		return match[0]
	return 'failed about 129'
	
	
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
		if len(S)==0:
			print(f'Not writing empty set "{S.filepath}"')
			return
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
	
	def takeout(S, item1,item2):
		print(f' takeout({item1} , {item2}) ',end='')
		if item1 and item2:
			S.remove((item1,item2))
			print ( f' -1 -2')
			return
		if item1:
			for item in S:
				if item1==item[0]:
					S.remove(item)
					
					print ( f' -1 xx')
					return
			return
		if item2:
			for item in S:
				if item2==item[1]:
					S.remove(item)
					S.add((item[0],''))
					print ( f' xx -2')
					print (f'store: ({item[0]},"")')
					return

#re_def_fnc=re.compile(f'{DEF}\w+{PARAMS}$')
re_def_fnc=re.compile(r'def fnc_\w+\(P,ev\):')

class PreviousConfigIterator:
	def __init__(S,source_path,dest_file):
		S.dest=dest_file
		S.current_func=SENTINEL
		S.source=None
		S.source_path=source_path
		S.open_old_config()
		
		
	def open_old_config(S):
		if not S.source_path:
			S.source=None
			S.line_red = SENTINEL
			return
		try:
			S.source=open(S.source_path,'r')
			S.line_red = None
		except Exception as e:
			ic(e)
			exit(1)
			
	def __iter__(S):
		if S.source:
			S.source.close()
		S.open_old_config()
		return S
 
	def __next__(S):
		if not S.source:
			return SENTINEL
			
		if S.line_red:
			S.dest.write(S.line_red)
		while True:
			S.line_red=S.source.readline()
			if not S.line_red:
				S.source.close()
				S.source=None
				return SENTINEL
			match=re_def_fnc.findall(S.line_red)
			if match:
				return match[0].strip()
			S.dest.write(S.line_red )
			
def fnc_lookup_key(code,first_class,title):
	return f'{code}{first_class}{title}'

re_one_char=re.compile(r'KEY_([A-Z])$',re.I)
class FuntionPrototype:
	def __init__(S,code,key,primo='',title=''):
		S.key=key
		match=re_one_char.findall(key)
		if match:
			S.key=match[0].upper()
		S.code=code
		S.primo=primo
		S.title=title
		S.base_name=S.naming_base()
		S.def_func=S.def_function()
		
	def __str__(S):
		return f'FuntionPrototype("{S.def_func}")'
	
	def is_sentinel(S):
		return S.key==SENTINEL
		
	def compare(S,other_func_def):
		if other_func_def == SENTINEL:
			return -1
		sl=len(S.def_func)
		ol=len(other_func_def)
		if sl > ol:
			return 1
		if sl < ol:
			return -1
		if S.def_func > other_func_def:
			return 1
		if S.def_func < other_func_def:
			return -1
		return 0
		
	def __lt__(S,O):
		return S.compare(O.def_func) < 0
		# if S.key != O.key:
		# 	return S.key<O.key
		# if S.primo != O.primo:
		# 	return S.primo<O.primo
		# return  S.title < O.title
	
	def def_function(S):
		return f'def {FNC}{S.base_name}{PARAMS}'
	
	def naming_base(S):
		primo_ = '' if S.primo=='' else '_'
		sec_ = '' if S.title =='' else '_'
		clean_primo = clean_function_name(S.primo)
		clean_sec      = clean_function_name(S.title)
		return f'{S.key}{primo_}{clean_primo}{sec_}{clean_sec}'
	
	def fnc_name(S):
		# primo_ = '' if S.primo=='' else '_'
		# sec_ = '' if S.title =='' else '_'
		# clean_primo = clean_function_name(S.primo)
		# clean_sec_ = clean_function_name(S.title)
		return f'{FNC}{S.base_name}'

	def write_prototype(S,open_file):
		open_file.write(f'\n\n{S.def_function()}')
		open_file.write('\n\tpass')
		lookup_key=fnc_lookup_key(S.code,S.primo,S.title)
		open_file.write(f'\n#{LOOKUP}["{lookup_key}"]={S.fnc_name()}')
		open_file.write(f'\n{LOOKUP}["{lookup_key}"]=None')

class FunctionIterator:

	def __init__(S,keyset,class_title_set):
		
		def key_class_title_tup(clss='',title=''):
			return [FuntionPrototype(code,key,clss,title) for code,key in keyset ]
			
		# find same class names with different window titles
		class_dict={}
		for clss,title in class_title_set:
			if clss in class_dict:
				# class with more than one title
				class_dict[clss].append(title)
				continue
			class_dict[clss]=[title]
			
		keys_solo  =key_class_title_tup()
		
		keys_class = []
		for clss  in class_dict:
			keys_class+=key_class_title_tup(clss)
			
		keys_class_title = []
		for clss,titles in class_dict.items():
			if len(titles)<2:
				continue
			for title in titles:
				if not title:
					continue
				keys_class_title+=key_class_title_tup(clss,title)
		
		# JDUMP(keys_solo)
		# JDUMP(keys_class)
		# JDUMP(keys_class_title)
		S.poul=keys_solo + keys_class + keys_class_title
		S.poul.sort()
		# for item in S.poul:
		# 	print(item)
		S.index=-1
		S.length=len(S.poul)
		S.current=None
	
	def __iter__(S):
		S.index=-1
		S.current=None
		return S
		
	def __next__(S):
		S.index+=1
		if S.index >= S.length:
			S.current=FuntionPrototype(999,SENTINEL)
			return  FuntionPrototype(999,SENTINEL)
		S.current=S.poul[S.index]
		return  S.current
	
	def write_prototype(S,f):
		S.current.write_prototype(f)
		
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
		print(f'config_update({S.event_by_id})')
		bck_count=1
		
		def write_first_time_config():
			with open(S.config_file_path,'w') as f:
				f.write(file_header(S.event_by_id))
				it_new=FunctionIterator(S.eventset, S.windowset)
				new=next(it_new)
				while not new.is_sentinel():
					new.write_prototype(f)
					new=next(it_new)
		
		def backup():
			nonlocal bck_count
			stam=S.config_file_path[:-3]
			while True:
				bckf=f'{stam}_{bck_count:03d}bck.py'
				if not os.path.isfile(bckf):
					break
				bck_count+=1
			os.rename(S.config_file_path,bckf)
			return bckf
		
		if not os.path.isfile(S.config_file_path):
			write_first_time_config()
			return
		
		it_new=FunctionIterator(S.eventset, S.windowset)
		new=next(it_new)
		old_config=backup()
		rev_line = '\n'+'# REVISION : '+str(bck_count)+'\n'
		with open(S.config_file_path,'w') as new_config:
			it_old=PreviousConfigIterator(old_config,new_config)
			old=next(it_old)
			
			while not (old==SENTINEL and new.is_sentinel()):
				print(f'\n{old} ->\n{new}{new.is_sentinel()=}')
				comp=new.compare(old)
				print(f'\n{comp=}')
				if comp == 0 :
					new_config.write('\nCOPY  OLD SCIP NEW\n')
					old   = next(it_old)
					new = next(it_new)
					continue
				if comp<0:
					new_config.write('\nWRITE NEW\n')
					new.write_prototype(new_config)
					new_config.write(rev_line)
					new=next(it_new)
					continue
				new_config.write('\nWRITE OLD\n')
				old=next(it_old)
		# new_gen = FunctionIterator(S.eventset, S.windowset)
		# func = new_gen.next_event_func()
		# new=next(func )
		#
		# if not os.path.isfile(S.config_file_path):
		# 	print(f'{S.config_file_path} does not exist')
		# 	# Write first time configuration framework
		# 	with open(S.config_file_path,'w') as f:
		# 		f.write(file_header(S.event_by_id))
		# 		while not SENTINEL in str(new):
		# 			new_gen.write_prototype(f)
		# 			new = next(func )
		# 	return
		# # merge sort old with new
		# old_config_file = backup()
		# with open(S.config_file_path,'w') as f:
		# 	read_old=PreviousConfigIterator(old_config_file,f)
		# 	old_func=read_old.advance_a_function()
		# 	old = next(old_func)
		# 	while not (  SENTINEL in old and  SENTINEL in new):
		# 		# new is a FuntionPrototype
		# 		# old is a string "def fnc_(event_cat..)(P,ev):"
		# 		compared = new.compare(old)
		# 		if not compared:
		# 			# old == new so copy the old edited
		# 			old   = next(old_func)
		# 			new = next(func )
		# 			continue
		# 		if compared < 0:
		# 			# old > new put new in front of old
		# 			new_gen.write_prototype(f)
		# 			new = next(func )
		# 			continue
		# 		# compared > 0 so old < new
		# 		# copy o;d and advance
		# 		old = next(old_func)
		#
	async def event_listener(S):
		async for event in S.inputdevice.async_read_loop():
			# print(f'event_listener {evdev.categorize(event)}')
			# continue
			title,primo,secundo=get_active_title_class_class()
			code = str(event.code)
			print(f'{code},{title},{primo},{secundo} -> {evdev.categorize(event)}')
			
			action = S.lookup.get(fnc_lookup_key(code,primo,title))
			if action:
				action(PIPER,event)
				continue
			action = S.lookup.get(fnc_lookup_key(code,primo))
			if action:
				action(PIPER,event)
				continue
			action = S.lookup.get(fnc_lookup_key(code) )
			if action:
				action(PIPER,event)
				continue
			print(f'NO KEY: {code},{title},{primo},{secundo} ')
			# name = name_event(event)
			# S.eventset.stores_new((event.code,name))
			# S.windowset.stores_new((primo,secundo))
			PIPER.squeak_event(event)

	# async def event_listener_off(S):
	# 	event = await  S.inputdevice.async_read()
	# 	#print(f'event_listener {evdev.categorize(event)}')
	# 	ic(event)
	# 	# continue
	# 	primo,secundo=get_active_class_class()
	# 	code = str(event.code)
	# 	print(f'{code},{primo},{secundo} -> {evdev.categorize(event)}')
	# 	action = S.lookup.get(code + primo + secundo )
	# 	if action:
	# 		action(PIPER,event)
	# 		return
	# 	action = S.lookup.get(code + primo )
	# 	if action:
	# 		action(PIPER,event)
	# 		return
	# 	action = S.lookup.get(code  )
	# 	if action:
	# 		action(PIPER,event)
	# 		return
	# 	ic(code,primo,secundo)
	# 	name = S.name_event(event)
	# 	S.eventset.stores_new((event.code,name))
	# 	S.windowset.stores_new((primo,secundo))
	# 	PIPER.squeak_event(event)

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
	#hid=HID_Device('usb-INSTANT_USB_GAMING_MOUSE-if01-event-kbd')
	hid=HID_Device("usb-Nordic_2.4G_Wireless_Receiver-if01-event-mouse")
	print(hid.event_no)
	
	it_new = FunctionIterator(hid.eventset, hid.windowset)
	new =next(it_new)
	it_old   =PreviousConfigIterator(
		'/home/bob/python/rattenkonig/configs/usb_INSTANT_USB_GAMING_MOUSE_if01_event_kbd/key_def_001bck.py',
					  sys.stdout)
	old = next(it_old)
	emergency_break=120
	while not (  old == SENTINEL and  new.is_sentinel()):
		if emergency_break < 0:
			print(f'\nemergency_break')
			exit(560)
		emergency_break-=1
		print(f'\n{old} ->\n{new}{new.is_sentinel()=}')
		
		comp = new.compare(old)
		print(f'\n{comp=}')
		if not comp:
			old   = next(it_old)
			new = next(it_new )
			continue
		if comp < 0:
			new.write_prototype(sys.stdout)
			new = next(it_new )
			continue
		old = next(it_old)

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
	# print( get_active_title_class_class())
	# # get_active_title_class_class()
	test_update()
	exit(0)
	
	try:
		asyncio.run(hid_read_loop())
	except KeyboardInterrupt:
		print(f'{sys.argv[0]} KeyboardInterrupt')