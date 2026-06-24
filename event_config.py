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

SENTINEL           = "~~~~~~ SENTINEL ~~~~~~"
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
		return 'k'+ks.capitalize()
		#return CamelCase(_key)
	elif _btn:
		bs=_btn.split('_')[1]
		if len (bs) > 8 :
			bs = no_vowels(bs)
		#return CamelCase(_btn)
		return 'b'+bs.capitalize()
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

class EventFnc:
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
		S.class_name  = 'EventFnc'
		
	def __str__(S):
		return f'{S.class_name}({S.code},{S.key},{S.clss},{S.title})'
	
	def is_sentinel(S):
		return S.key==SENTINEL
	
	def compare(S, O):
		# print(f'compare: {S.def_func} - {other_func_def}')
		if O.key==SENTINEL:
			return -1
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
	
	def __eq__(S,O):
		return S.compare(O) == 0
	
	def __hash__(S):
		return hash(str(S))
	
	def store(S,f):
		f.write('\n\n')
		f.write(S.payload)
	
class EventFncNew(EventFnc):
	def __init__(S,code,key,clss='',title=''):
		super().__init__(code,key,clss,title)
		S.class_name = 'EventFncNew'
		_clss = yn(clss,'_','')
		_ttle= yn(title,'_','')
		_ev_key=event_key(code,clss,title)
		S.payload = f"""{MARKER}({code},{key},{clss},{title})
{DEF}{clss}{_clss}{key}{_ttle}{title}{PARAMS}
\tpass
{LOOKUP}['{_ev_key}']=None
#{LOOKUP}['{_ev_key}']={FNC}{clss}{_clss}{key}{_ttle}{title}"""


#class EventFncStored(EventFnc):

marker_patern = MARKER+r'\(([^)]+)\)'
re_marker = re.compile(marker_patern)

class EventFncStored(EventFnc):
	
	def __init__(S,par):
		print(f'EventFncStored {par=}')
		match = re_marker.findall(par)
		if not match:
			print(f'No valid Marker line in : {par=}')
			ic()
			exit(413)
		code,key,clss,title = match[0].split(',')
		print(code,key,clss,title)
		super().__init__(code,key,clss,title)
		S.class_name='EventFncStored'
		S.payload = par.strip()
		
class EventFncConfig:
	
	def __init__(S,config_file_path,code_keys,clss_title):
		S.config_file_path=config_file_path
		S.code_keys=code_keys
		S.clss_title=clss_title
		S.gen_fnc_list=[]
		S.file_fnc_set=set()
		
	def generate_fncs(S):
		fnc_set=set()
		for code,key in S.code_keys:
			fnc_set.add(EventFncNew(code,key))
		for code,key in S.code_keys:
			for clss,title in S.clss_title:
				fnc_set.add(EventFncNew(code,key,clss,title))
				fnc_set.add(EventFncNew(code,key,clss))
		S.gen_fnc_list=list(fnc_set)
		S.gen_fnc_list.sort()
		
	def read_config_file(S):
		S.file_fnc_set=set()
		with open(S.config_file_path,'r') as f:
			try:
				content= f.read()
			except Exception as e:
				print(f'Reading "{S.config_file_path}" Failed.')
				ic(e)
				exit(1)
		fncs=content.split(MARKER)
		fncs.pop(0) # remove header
		for fnc in fncs:
			print('#'*30)
			payload=MARKER+fnc
			print(payload)
			S.file_fnc_set.add(EventFncStored(payload))

	def write_file(S,name='test',backup=True):
		if backup:
			S.make_backup()
		S.file_fnc_set.update(S.gen_fnc_list)
		new_list=list(S.file_fnc_set)
		new_list.sort()
		with open(S.config_file_path,'w') as f:
			f.write(file_header(name))
			for fnc in new_list:
				fnc.store(f)
				
	def make_backup(S):
		i=0
		cf = os.path.dirname(S.config_file_path) + '/' +os.path.basename(S.config_file_path)
		while True:
			i+=1
			try_path = cf +f'_{i:03d}'+'.bck'
			if not os.path.exists(try_path):
				break
		os.rename(S.config_file_path,try_path)
		
def test_proto_list():
	clss_win=[["hidDeviceSetupPy", ""], ["jetbrainspycharm", ""], ["konsole", ""], ["Navigator", ""]]
	btns=[[273, "bRIGHT"], [11, "rS"], [8, "rL"], [0, "rX"], [274, "bMIDDLE"], [1, "rY"], [272, "bLEFT"], [275, "bSIDE"], [276, "bEXTRA"]]
	eventconfig=EventFncConfig('TEST.py',btns,clss_win)
	eventconfig.generate_fncs()
	for i in eventconfig.gen_fnc_list:
		i.store(sys.stdout)
	
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
	test_proto_list()
	exit(0)
	