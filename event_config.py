#!/bin/python3
import os
import sys
from evdev import categorize,ecodes as ec
import re
import json
import time
from X11_Utils import get_active_title_class_class
from icecream import ic
ic.configureOutput(includeContext=True)

def JDUMP(jsn):
	print(json.dumps(jsn,indent=4))
	
def eat_all(*args):
	pass

PRINT=print 
PRINT=eat_all

#CONFIGDIR         = None # args.configdir
KEYSFILEPY        = 'key_def.py'
KEYSFILE             = ' key_def'
LOOKUP              = 'hid_lookup'
DETECTEDHIDS = None

CLASS_INDEX=0
TITLE_INDEX=1

CODE_INDEX=0
BUTTON_INDEX=1

#SENTINEL           = "~~~~~~ SENTINEL ~~~~~~"
MARKER             =  "# ~~~ # "
LMARKER           = len(MARKER)
FNC                      =  'fnc_'
DEF                      =  'def ' + FNC
LDEF                    =  len(DEF)
PARAMS             =  '(P,ev):'
LPARAMS           =  len(PARAMS)


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
# relay_code(S, ev_type, ev_code, ev_value)    send an event to the UInput device.
#
# relay(S, event)    send an event to the UInput device.
#     use to pass trough un altered events
#
# syn_report(S)
#     simulate a single key or button press
#
# type_keys(S, *args)    type the keys in args like typed from a keyboard

from evdev import ecodes as ec
id='{name}'

{LOOKUP}={{}}

# BEE AWARE: edits above the next marker will be lost,
#  everyting below is conserved between saves
'''

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
		# split of 'KEY_'
		ks=_key.split('_')[1]
		if len (ks) > 8 :
			ks = no_vowels(ks)
		return 'k'+ks.capitalize()
	if _btn:
		# split of 'BTN_'
		bs=_btn.split('_')[1]
		if len (bs) > 8 :
			bs = no_vowels(bs)
		return 'b'+bs.capitalize()
	if _rel:
		# split of 'REL_'
		#rs=_rel.split('_')[1]
		rs=_rel[4:]
		return 'r'+ trim_to_camel(rs)
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

def yn(true,yes,no):
	if true:
		return yes
	return no
		
re_one_char=re.compile(r'KEY_([A-Z])$',re.I)
re_title =re.compile(r':(\w+) ')

MAXTITLELEN = 8
MAXCLASSLEN=12
LENKEY = 4 + MAXCLASSLEN +MAXTITLELEN + 2
NOCLSS = ' '*MAXCLASSLEN
NOTITLE= ' '*MAXTITLELEN

def compose_sorting_key(code,clss='',title=''):
	cd=f'{code:04d}'
	cl =clss.ljust(MAXCLASSLEN)[:MAXCLASSLEN]
	tl = title.ljust(MAXTITLELEN)[:MAXTITLELEN]
	return cl + '-' + tl + '-' + cd

def compose_3_sorting_keys(code,clss,title):
	cd=f'{code:04d}'
	cl =clss.ljust(MAXCLASSLEN)[:MAXCLASSLEN]
	tl = title.ljust(MAXTITLELEN)[:MAXTITLELEN]
	return (cl + '-' + tl + '-' + cd
		        , cl + '-' + NOTITLE + '-' + cd
		        , NOCLSS+ '-' + NOTITLE + '-' + cd)

word_re=re.compile(r'([a-zA-Z]+)')
title_re=re.compile(r':\s*(\w+)')

def gen_code_key_class_title(event):
	def reduce_class(clss,length=8):
		clss = re.sub(r'(\W+)','_',clss)
		if len(clss) <= length:
			return clss
		
		x=clss[0].upper() + no_vowels(clss[1:])
		if len(x) <= length:
			return x
		return x[length:].upper()
		
	def reduce_title(title,length=10):
		#ic(title)
		match = title_re.findall(title)
		if match:
			#ic(match[0])
			return match[0]
		if len(title) <= length:
			#ic(title)
			return title
		match = word_re.findall(title)
		max=''
		for  word in match:
			
			if len(word) > len(max):
				max=word
		if len(max) <= length:
			#ic(max)
			return max
		x=max[0].upper() + no_vowels(max[1:])
		if len(x) <= length:
			#ic(x)
			return x
		#ic(x.upper)
		return x.upper()

	title, clss, _=get_active_title_class_class()
	clss  = reduce_class(clss)
	title = reduce_title(title)
	event_name=name_event(event)
	return event.code, event_name, clss, title

class EventFnc:
	def __init__(S,sorting_key):
		S.sorting_key = sorting_key
		S.class_name  = 'EventFnc'
		
	def __str__(S):
		return f'{S.class_name}({S.sorting_key})'
	
	def __lt__(S,O):
		return S.sorting_key < O.sorting_key
	
	def __eq__(S,O):
		return S.sorting_key == O.sorting_key
	
	def __hash__(S):
		return hash(S.sorting_key)
	
	def write_sorting_key(S,f):
		f.write(f'\n\n{MARKER}{S.sorting_key}\n')
	
class EventFncNew(EventFnc):
	def __init__(S,code,key,clss='',title=''):
		super().__init__(compose_sorting_key(code,clss,title))
		S.class_name = 'EventFncNew'
		S.code=code
		S.key=key
		S.clss=clss
		S.title = title
		if title == '' : return
		match = re.findall(r'\W+',title)
		if not match: return
		match = re_title.findall(title)
		if match:
			S.title=match[0]
			return
		S.title = ''
		
	def write_code_block(S,f):
		S.write_sorting_key(f)
		_clss = yn(S.clss,'_','')
		_ttle= yn(S.title,'_','')
		func_name=f'{S.key}{_clss}{S.clss}{_ttle}{S.title}'
		f.write(f"""{DEF}{func_name}{PARAMS}
\tpass
#\tprint(f'{func_name}')
{LOOKUP}['{S.sorting_key}']=None
#{LOOKUP}['{S.sorting_key}']={FNC}{func_name}""")


#class EventFncStored(EventFnc):

marker_patern = MARKER+r'\(([^)]+)\)'
re_marker = re.compile(marker_patern)

class EventFncStored(EventFnc):
	
	def __init__(S,block):
		"""
		extract the key save the rest
		:param block: key code and look_up entry between two markers
		"""
		super().__init__(block[:LENKEY])
		S.class_name='EventFncStored'
		S.payload = block.strip()
		
	def write_code_block(S,f):
		f.write(f'\n\n{MARKER}{S.payload}')
	
		
class EventFncConfig:
	'''
	read the config file at "config_file_path" if it
	already exists.
	Create event filter function models
	Merge new fuctions into the config file.
	'''
	
	def __init__(S,config_file_path,code_keys,clss_title):
		S.config_file_path=config_file_path
		S.code_keys=code_keys
		S.clss_title=clss_title
		S.gen_fnc_list=[]
		S.file_fnc_set=set()
		S.user_data=''
		
	def generate_fncs(S):
		'''
		generate a set of function models by combining the
		code_keys with clss_title iterables
		:return: by side effect a sorted S.gen_fnc_list
		'''
		fnc_set=set()
		for code,key in S.code_keys:
			fnc_set.add(EventFncNew(code,key))
		for code,key in S.code_keys:
			for clss,title in S.clss_title:
				fnc_set.add(EventFncNew(code,key,clss,title))
				fnc_set.add(EventFncNew(code,key,clss))
		S.gen_fnc_list=list(fnc_set)
		#print("S.gen_fnc_list.sort()")
		S.gen_fnc_list.sort()
		# print("S.gen_fnc_list.sort()")
		# for fnc in S.gen_fnc_list:
		# 	print(fnc)
		
	def read_config_file(S):
		S.file_fnc_set=set()
		if not os.path.isfile(S.config_file_path):
			return
		
		with open(S.config_file_path,'r') as f:
			try:
				content= f.read()
			except Exception as e:
				print(f'Reading "{S.config_file_path}" Failed.')
				ic(e)
				exit(1)
		blocks=content.split(MARKER)
		blocks.pop(0) # remove header
		S.user_data = blocks.pop(0) # save what the user added
		
		for block in blocks:
			print('#'*30)
			print(block)
			S.file_fnc_set.add(EventFncStored(block))

	def write_file(S,backup=True):
		S.read_config_file()
		if backup:
			S.make_backup()
		S.generate_fncs()
		S.file_fnc_set.update(S.gen_fnc_list)
		new_list=list(S.file_fnc_set)
		new_list.sort()
		with open(S.config_file_path,'w') as f:
			f.write(file_header(S.config_file_path))
			f.write('\n'+MARKER+'\n')
			f.write(S.user_data)
			for fnc in new_list:
				fnc.write_code_block(f)
				
	def make_backup(S):
		if not os.path.isfile(S.config_file_path):
			return
		i=0
		cf = os.path.dirname(S.config_file_path) + '/' +os.path.basename(S.config_file_path)
		while True:
			i+=1
			try_path = cf +f'_{i:03d}'+'.bck'
			if not os.path.exists(try_path):
				break
		os.rename(S.config_file_path,try_path)
		
def trim_to_camel(txt):
	txt=re.sub(r'(\W+)','_',txt)
	#print(txt)
	words=txt.split('_')
	ret=words.pop(0).capitalize()
	for word in words:
		ret+= word[:1].upper()
		ret+= no_vowels(word[1:])
	return ret

def test_to_camel():
	tt=''''
	Clearing config: /home/bob/FreeCAD/mouse_keys/usbNordic24GWirelessReceiverif01eventmouse/windows.json
display_event(008,"rWHEEL")
display_classes("hiddevicesetuppy", "HDSbNrdc24")
display_event(011,"rWHEELHIRES")
EventReader.run() stopped.
HID_Device(04,"usb-Nord...nt-mouse") disconnected
Pied Piper left Hamelin.
'''
	tts=tt.split('\n')
	for txt in tts:
		print(txt)
		print(trim_to_camel(txt))
		

def test_stored_fnc():
	payload='''# ~~~ # (276,bEXTRA,jetbrainspycharm,)
def fnc_jetbrainspycharm_bEXTRA(P, ev):
	pass
hid_lookup['276jetbrainspycharm']=None
# hid_lookup['276jetbrainspycharm']=fnc_jetbrainspycharm_bEXTRA'''
	stored_fnc=EventFncStored(payload)
	#stored_fnc=EventFncStored()

if __name__ == '__main__':
	#test_stored_fnc()
	#test_to_camel()
	print (f'No TEST in "{__file__}')
	exit(0)
	