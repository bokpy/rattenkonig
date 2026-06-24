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
import argparse
import piper
import asyncio
import atexit
from X11_Utils import get_active_title_class_class


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
KEYSFILEPY        = 'key_def.py'
KEYSFILE             = ' key_def'
LOOKUP              = 'hid_lookup'
DETECTEDHIDS = None

CLASS_INDEX=0
TITLE_INDEX=1

CODE_INDEX=0
BUTTON_INDEX=1

SENTINEL           = "~~~~~~ SENTINEL ~~~~~~"
MARKER             =  "# ~~~ # "
FNC                      =  'fnc_'
DEF                      =  'def ' + FNC
LDEF                    =  len(DEF)
PARAMS             =  '(P,ev):'
LPARAMS           =  len(PARAMS)
PIPER = piper.PiedPiper()


def file_header(name):
	return f'''# rattenkonig key button configuration
# date:  {time.asctime()}
#
# default(S, event)    print an event for debuging
#
# message(S, s)    print a string as typed from a keyboard without capslock on.
#
# nap(S, snooze=0.01)    do sleep
#
# hold(S, *args)    press and hold a number of keys and/or buttons simultaneous.
#
# release(S, *args)    release keys/buttons previous pressed and holded
#
# report_move(S, ev_code, ev_value)    send a relative move event to the UInput device
#
# simultaneous_keys(S, *args)    press  keys together and also release.
#
# passthrough_code(S, ev_type, ev_code, ev_value)    send an event to the UInput device.
#
# passthrough(S, event)    send an event to the UInput device.
#     use to pass trough un altered events
#
# syn_report(S)
#     simulate a single key or button press
#
# type_keys(S, *args)    type the keys in args like typed from a keyboard

from evdev import ecodes as ec
id='{name}'

{LOOKUP}={{}}
'''
def import_from_path(module_name, file_path):
	#ic(module_name, file_path)
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

def event_key(code,clss,tittle):
	if isinstance(code,int):
		code=f'{code:03d}'
	key=code+clss+tittle
	key=re.sub(r'[^a-zA-Z0-9]','',key)
	return key

re_square_bracket=re.compile(r'\[([^,]+),')
re_parentheses=re.compile(r'\(([^)]+)\)')
re_relative=re.compile(r'(rel_[_a-z]+)')

event_name_re=re.compile(r"(KEY_\w+)|(BTN_\w+)|(REL_\w+)|(ABS_\w+)")

def name_event(event):
	# key event at 1779512964.993459, 274 (BTN_MIDDLE), up
	# relative axis event at 1781505193.907004, REL_Y
	cat_event = str(categorize(event)) #.lower()
	match =  event_name_re.findall(cat_event)
	if len(match)<1:
		print(cat_event)
		return 'BadEvent'
	_key,_btn,_rel,_abs = match[0]
	if _key:
		ks=_key.split('_')[1]
		if len (ks) > 8 :
			ks = no_vowels(ks)
		#return CamelCase(_btn)
		return 'k'+ks
		return CamelCase(_key)
	elif _btn:
		bs=_btn.split('_')[1]
		if len (bs) > 8 :
			bs = no_vowels(bs)
		#return CamelCase(_btn)
		return 'b'+bs
	elif _rel:
		#return CamelCase(_rel)
		return 'r'+_rel[-1:]
	return CamelCase(_abs)
	
def CamelCase(name):
	if ':' in name:
		name=name.split(':')[1]
	name=name.replace('.','_')
	name=re.sub(r'[^a-zA-Z0-9_]','',name)
	words = name.split('_')
	return words[0] + ''.join(word[0].upper() + word[1:] if word else '' for word in words[1:])

def no_vowels(txt):
	return re.sub(r'[aeiouAEIOU]','',txt)

def fnc_lookup_key(code,clss=None,title=None):
	cd = f'{code:03d}'
	if not clss:
		return cd
	ret = cd + '_' + CamelCase(clss)
	if not title:
		return ret
	return ret + '_' + CamelCase(title)

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
	def __init__(S,source_path):
		S.dest=None
		with open(source_path,'r') as f:
			S.lines = f.readlines()
		S.lines_count = len(S.lines)
		S.index = 0
		
	def set_output(S,open_file):
		S.dest=open_file
		return S
		
	def __iter__(S):
		S.index = 0
		return S
	
	def __next__(S):
		if S.index >= S.lines_count:
			return SENTINEL
		S.dest.write(S.lines[S.index])
		S.index+=1
		new_line_count=0
		while S.index < S.lines_count:
			line     = S.lines[S.index]
			print(f'-->{line}<--')
			match=re_def_fnc.findall(line)
			if match:
				return match[0].strip()
			S.dest.write(S.lines[S.index])
			S.index+=1
		return SENTINEL
	
def yn(true,yes,no):
	if true:
		return yes
	return no
		
re_one_char=re.compile(r'KEY_([A-Z])$',re.I)
re_title =re.compile(r':(\w+) ')

def title_exstract(txt):
	if not txt:
		return ''
	match = re_title.findall(txt)
	if not match:
		return ''
	txt=match[0]
	if  len(txt)>12:
		txt=no_vowels(txt)
	return CamelCase(txt)

class FuntionPrototype:
	def __init__(S,code,key,clss='',title=''):
		if key == SENTINEL:
			S.key=SENTINEL
			S.code='999'
			return
		S.code              = code
		S.key                 = key
		S.clss                 = clss
		S.title                = title
		S.payload         = None
		
	def __str__(S):
		return f'FuntionPrototype({S.code},{S.key},{S.clss},{S.title})'
	
	def is_sentinel(S):
		return S.key==SENTINEL
	
	def compare(S, O):
		# print(f'compare: {S.def_func} - {other_func_def}')
		if O.key==SENTINEL:
			return -1
		# other_kern=other_func_def[LDEF:-LPARAMS:]
		# other_split=other_kern.split('_')
		# other_split+=['', '']
		# other_key=other_split[0]
		# other_clss=other_split[1]
		# other_title=other_split[2]
		
		if S.clss>O.clss:
			return 1
		if S.clss<O.clss:
			return -1
		if S.key>O.key:
			return 1
		if S.key<O.key:
			return -1
		if S.title>O.title:
			return 1
		if S.title<O.title:
			return -1
		return 0
	
	def __lt__(S,O):
		return S.compare(O) < 0
	
	def __hash__(S):
		return hash(str(S))
	
class NewPrototype(FuntionPrototype):
	def __init__(S,code,key,clss='',title=''):
		super().__init__(code,key,clss,title)
		_clss = yn(clss,'_','')
		_ttle= yn(title,'_','')
		_ev_key=event_key(code,clss,title)
		S.payload = f"""{MARKER}{code},{key},{clss},{title}
{DEF}{clss}{_clss}{key}{_ttle}{title}{PARAMS}
\tpass
{LOOKUP}['{_ev_key}']=None
#{LOOKUP}['{_ev_key}']={FNC}{clss}{_clss}{key}{_ttle}{title}"""

	def def_function(S):
		return f'def {FNC}{S.base_name}{PARAMS}'
	
	def naming_base(S):
		_clss  = '' if S.clss  =='' else '_'
		_title = '' if S.title =='' else '_'
		return f'{S.key}{_clss}{S.clss}{_title}{S.title}'
	
	def fnc_name(S):
		# primo_ = '' if S.primo=='' else '_'
		# sec_ = '' if S.title =='' else '_'
		# clean_primo = CamelCase(S.primo)
		# clean_sec_ = CamelCase(S.title)
		return f'{FNC}{S.base_name}'

	def write_prototype(S,open_file):
		open_file.write(f'\n{S.def_function()}')
		open_file.write('\n\tpass')
		lookup_key=fnc_lookup_key(S.code,S.clss,S.title)
		open_file.write(f'\n#{LOOKUP}["{lookup_key}"]={S.fnc_name()}')
		open_file.write(f'\n{LOOKUP}["{lookup_key}"]=None')
		open_file.write(f'\n# added  {time.asctime()}\n')
	
def protoList(keyset,class_title_set):
	class_title_set.append(('',''))
	proto_set={ NewPrototype(code,key,clss,title)
				for code,key in keyset for clss,title in class_title_set }
	for proto in proto_set:
		print(proto)
	return proto_set
	
	
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
	trigger_events=(
	ec.EV_KEY
	# , ec.EV_ABS
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
			S.inputdevice=evdev.InputDevice(S.event_path)
			S.inputdevice.grab()
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
		print(f'config_update({S.event_by_id})')
		bck_count=1
		
		def write_first_time_config():
			with open(S.config_file_path,'w') as f:
				f.write(file_header(S.event_by_id))
				it_new=FunctionIterator(S.eventset, S.windowset)
				new=next(it_new)
				while not new.is_sentinel():
					new.write_prototype(sys.stdout)
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
			ic(S.config_file_path)
			write_first_time_config()
			return
		
		it_new=FunctionIterator(S.eventset, S.windowset)
		new=next(it_new)
		#old_config=backup()
		#rev_line = '\n'+'# REVISION : '+str(bck_count)+'\n'
		it_old_class=PreviousConfigIterator(S.config_file_path)
		with open(S.config_file_path,'w') as new_config:
			it_old_class.set_output(new_config)
			it_old = iter(it_old_class)
			old   = next(it_old)
			new = next(it_new)
			while not (old==SENTINEL and new.is_sentinel()):
				
				# print(f'\n{old} ->\n{new}{new.is_sentinel()=}')
				comp=new.compare(old)
				# print(f'\n{comp=}')
				if comp == 0 :
					#new_config.write('\n# COPY  OLD SKIP NEW\n')
					old   = next(it_old)
					new = next(it_new)
					continue
				if comp<0:
					#new_config.write('\n# WRITE NEW\n')
					new.write_prototype(new_config)
					#new_config.write(rev_line)
					new=next(it_new)
					continue
				#new_config.write('\n# WRITE OLD\n')
				old = next(it_old)

	async def event_listener(S):
		DOTS=90
		_dot=DOTS
		async for event in S.inputdevice.async_read_loop():
			if not event.type in  HID_Device.trigger_events:
				continue
			#print(f'event_listener {evdev.categorize(event)}')
			# continue
			title,clss,_=get_active_title_class_class()
			code = str(event.code)
			# print(f'{code},{title},{clss},{_} -> {evdev.categorize(event)}')
			
			action = S.lookup.get(fnc_lookup_key(code,clss,title))
			if action:
				print(f'hit "{code+clss+title}"')
				action(PIPER,event)
				continue
			action = S.lookup.get(fnc_lookup_key(code,clss))
			if action:
				print(f'hit "{code+clss}"')
				action(PIPER,event)
				continue
			action = S.lookup.get(fnc_lookup_key(code))
			if action:
				print(f'hit "{code}"')
				action(PIPER,event)
				continue
			# print(f'NO KEY: {code},{title},{primo},{secundo} ')
			# name = name_event(event)
			# S.eventset.stores_new((event.code,name))
			# S.windowset.stores_new((primo,secundo))
			#PIPER.passthrough(event)
			_dot-=1
			if _dot < 0:
				print(f'<')
				_dot=DOTS
				continue
			print('.',end='',flush=True)

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
	
def test_proto_list():
	clss_win=[["hidDeviceSetupPy", ""], ["jetbrainspycharm", ""], ["konsole", ""], ["Navigator", ""]]
	btns=[[273, "bRIGHT"], [11, "rS"], [8, "rL"], [0, "rX"], [274, "bMIDDLE"], [1, "rY"], [272, "bLEFT"], [275, "bSIDE"], [276, "bEXTRA"]]
	l=protoList(btns,clss_win)
	
if __name__ == '__main__':
	test_proto_list()
	exit(0)
	# CONFIGDIR         = args.configdir
	# if CONFIGDIR[-1:] != '/':
	# 	CONFIGDIR+= '/'
	# get_caps()
	# exit(0)
	# print( get_active_title_class_class())
	# # get_active_title_class_class()
	# test_update()
	# exit(0)
	tomcat=kill_switch()
	try:
		asyncio.run(hid_read_loop())
	except KeyboardInterrupt:
		print(f'Terminated by KeyboardInterrupt')
	
		
	# finally :
	