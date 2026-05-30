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
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QObject, pyqtSignal,pyqtSlot ,QThread
from PyQt6.QtWidgets import QApplication, QTreeWidgetItem, QWidget,QTableWidgetItem
#from qasync import asyncSlot, QEventLoop, QApplication

from PyQt6.QtWidgets import QSizePolicy as sp
EXPANDING=sp.Policy.Expanding
FIXED=sp.Policy.Fixed
IGNORED =sp.Policy.Ignored
MAXIMUM=sp.Policy. Maximum
MINIMUM=sp.Policy.Minimum
MINIMUMEXPANDING=sp.Policy.MinimumExpanding
PREFERRED=sp.Policy.Preferred

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

# class DeviceEvent(dict):
# 	def __init__(S,event):
# 		super().__init__(S)
# 		S.event = event
# 		S['prime'],S['secondary']=get_active_class_class()
# 		S['type']=event.type
# 		S['code']=event.code
# 		S['name']=name_event(event)
# 		S.key=f"{S['prime']}{S['secondary']}{S['type']:02d}{S['code']:03d}"
#
# 	def __str__(S):
# 		return f"DeviceEvent({S['type']:2d},{S['code']:03d},{S['name']},{S['prime']},{S['secondary']})"
#
# 	def __lt__(S,O):
# 		return S.key < O.key

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
	
class WorkerEventReader(QObject):
	# class class
	signal_new_window  = pyqtSignal(str,str)
	# event code event name
	signal_new_event      = pyqtSignal(int,str)
	#finished         = pyqtSignal()
	
	def __init__(S, device):
		super().__init__()
		print(f'EventReader({device})')
		S.device    = device
		S.running = True
		
	def run(S):
		if not S.running:
			return
		eset=S.device.eventset
		wset=S.device.windowset
		
		while S.running :
			event = S.device.read_one()
			if not event or not event.type or event.type == 4:
				time.sleep(0.1)
				continue
			
			name = name_event(event)
			if eset.stores_new((event.code,name)):
				S.signal_new_event.emit(event.code,name)
			
			c1,c2=get_active_class_class()
			if wset.stores_new((c1,c2)):
				S.signal_new_window.emit(c1,c2)
			time.sleep(0.3)
		print('EventReader.get_events stopped.')
		S.running=False
		#S.finished.emit()

class HID_Device(evdev.InputDevice):
	def __init__(S,event_by_id,event_path):
		S.event_by_id = event_by_id
		evdev.InputDevice.__init__(S,event_path)
		S.configdir = CONFIGDIR + event_by_id +'/'
		S.eventset     = HidSet(S.configdir+'events.json')
		S.windowset = HidSet(S.configdir+'windows.json')
		S.read_sets()
		
	def write_sets(S):
		os.makedirs(S.configdir,exist_ok=True)
		S.windowset.writeset()
		S.eventset.writeset()

	def read_sets(S):
		if not os.path.isdir(S.configdir):
			return
		S.windowset.readset()
		S.eventset.readset()

	def end(S):
		S.ungrab()
		S.close()
	
	async def call_me(S,action):
	#def call_me(S):
		try:
			#async for event in dev.async_read_loop():
			async for event in S.async_read_loop():
				action(event)
		except Exception as e:
			ic(e)
	
	def register_user_events(S):
		window = None
		saved_window_flags = None
		event_table_row     = 0
		window_table_row = 0
		on_top_button=None
		save_button=None
		on_top=False
		
		S.grab()
		event_reader=WorkerEventReader(S)
		event_reader_thread=QThread()

		def display_event(code,name):
			nonlocal window_table_row,event_table_row,save_button
			#print(f'display_event({code:03d},"{name}")')
			tw=S.event_table_widget
			if tw.rowCount()<=event_table_row:
				tw.insertRow(event_table_row)
			strcode=f'{code:03d}'
			tw.setItem(event_table_row, 0,QTableWidgetItem(strcode ))
			tw.setItem(event_table_row, 1,QTableWidgetItem(name ))
			save_button.setText('save')
			#some scrolling if needed
			index = tw.model().index(event_table_row,0)
			tw.scrollTo(index)
			tw.update()
			event_table_row+=1
		
		def display_classes(prime , second):
			nonlocal event_table_row,window_table_row,save_button
			#print(f'display_classes("{prime }", "{second}")')
			tw=S.event_table_widget
			if tw.rowCount()<=window_table_row:
				tw.insertRow(window_table_row)
			tw.setItem(window_table_row, 2,QTableWidgetItem(prime ))
			tw.setItem(window_table_row, 3,QTableWidgetItem(second ))
			save_button.setText('save')
			
			#some scrolling if needed
			index = tw.model().index(window_table_row,2)
			tw.scrollTo(index)
			tw.update()
			window_table_row+=1
			
		def stay_on_top_toggle():
			nonlocal window,saved_window_flags,on_top_button,on_top
			if not saved_window_flags:
				saved_window_flags=window.windowFlags()
			if on_top:
				on_top_button.setText('Down')
				window.setWindowFlags(saved_window_flags)
			else:
				on_top_button.setText('Up')
				flags = saved_window_flags | Qt.WindowType.WindowStaysOnTopHint
				window.setWindowFlags(flags)
			on_top=not on_top
			window.show()
		
		def save_sets():
			nonlocal save_button
			S.write_sets()
			save_button.setText('Saved')
			
		def the_end():
			nonlocal event_reader,window,event_reader_thread
			#nicely stop the event_reader thread
			event_reader.running = False
			event_reader_thread.quit()
			# quit is quit do no more
			# ic(event_reader_thread)
			# event_reader_thread.wait()
			# ic(event_reader_thread)
			# del event_reader_thread
			# ic(event_reader_thread)
			window.close()
			#ic(window)
			S.ungrab()
			app.quit()
			#ic(app)

		app=QApplication(sys.argv)

		# main window
		window=QtWidgets.QWidget(windowTitle=f'Event and Window selection for a base "{S.name}" config')
		window.resize(800, 600)
		layout=QtWidgets.QVBoxLayout()
		window.setLayout(layout)
		
		#QTableWidget
		tw=S.event_table_widget=QtWidgets.QTableWidget(window)
		sizePolicy = QtWidgets.QSizePolicy(EXPANDING, EXPANDING)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(tw.sizePolicy().hasHeightForWidth())
		tw.setSizePolicy(sizePolicy)
		tw.setColumnCount(5)
		tw.setColumnWidth(0,50)
		tw.setColumnWidth(1,120)
		tw.setColumnWidth(2,140)
		tw.setColumnWidth(3,140)
		# tw.setColumnWidth(4,240)
		tw.setHorizontalHeaderLabels(('code','event','class','class'))
		#tw.setRowCount(10)
		layout.addWidget(tw)
		
		#test items
		# row=0
		# tw.setItem(row, 0, QTableWidgetItem('one'))
		# tw.setItem(row, 1, QTableWidgetItem('Last Name'))
		# tw.setItem(row, 2, QTableWidgetItem('Age'))
		# row += 1
		
		#add control buttons
		on_top_button,save_button,ok_button=add_buttons(('Ontop','Save','OK'),window, layout)
		ok_button.clicked.connect(the_end)
		save_button.clicked.connect(save_sets)
		on_top_button.clicked.connect(stay_on_top_toggle)

		# reflect what was saved
		for item in S.eventset:
			display_event(*item)
		for item in S.windowset:
			print(f'window {item=}')
			display_classes(*item)
		save_button.setText('saved')
		
		# event_reader thread setup
		event_reader.signal_new_event.connect(display_event)
		event_reader.signal_new_window.connect(display_classes)
		event_reader.moveToThread(event_reader_thread)
		event_reader_thread.started.connect(event_reader.run)
		event_reader_thread.start()

		window.show()
		app.exec()

def get_hid_devices():
	global DETECTEDHIDS
	DETECTEDHIDS=[]
	for by_id_path in os.listdir('/dev/input/by-id'):
		#print(f'{'/dev/input/by-id/'+by_id_path}')
		abs_path = get_abs_path('/dev/input/by-id/'+by_id_path)
		if '/dev/input/event' in abs_path:
			DETECTEDHIDS.append(HID_Device(event_by_id=by_id_path,event_path=abs_path))
	return DETECTEDHIDS

def add_buttons(names,window,layout):
	buttons=[]
	def make_button(name):
		button = QtWidgets.QPushButton(parent=window)
		button.setText(name)
		button_layout.addWidget(button)
		buttons.append(button)
	
	spacer=QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
	layout.addItem(spacer)
	button_layout=QtWidgets.QHBoxLayout()
	layout.addItem(button_layout)
	spacer=QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
	button_layout.addItem(spacer)
	
	#Single button
	if isinstance(names,str):
		make_button(names)
		return buttons[0]

	# buttons in a row
	for label in names:
		make_button(label)
	return buttons

def device_selector_gui():
	global DETECTEDHIDS
	if not DETECTEDHIDS:
		DETECTEDHIDS=get_hid_devices()
	app = QApplication(sys.argv)
	window = QWidget(windowTitle='HID devices by id.')
	window.resize(800, 600)
	layout = QtWidgets.QVBoxLayout()
	window.setLayout(layout)
	label = QtWidgets.QLabel(parent=window)
	font = QtGui.QFont()
	font.setFamily("C059")
	font.setPointSize(22)
	label.setFont(font)
	layout.addWidget(label)
	label.setText('Check the devices to configure')
	
	hid_boxes=[]
	for hid in DETECTEDHIDS:
		checkBox = QtWidgets.QCheckBox(parent=window)
		checkBox.setText(hid.event_by_id)
		hid_boxes.append((checkBox,hid))
		layout.addWidget(checkBox)
	
	# spacer=QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
	# layout.addItem(spacer)
	ok_button = add_buttons('OK',window,layout)
	ok_button.clicked.connect(window.close)
	window.show()
	app.exec()
	
	checked  = [ hid for checkbox,hid in hid_boxes if checkbox.isChecked() ]
	return checked

def device_select_one_gui():
	global DETECTEDHIDS
	if not DETECTEDHIDS:
		get_hid_devices()
		
	stop=False
	app=QApplication(sys.argv)
	window=QWidget(windowTitle='HID devices by id.')
	window.resize(800, 600)
	layout=QtWidgets.QVBoxLayout()
	window.setLayout(layout)
	label=QtWidgets.QLabel(parent=window)
	font=QtGui.QFont()
	font.setFamily("C059")
	font.setPointSize(22)
	label.setFont(font)
	layout.addWidget(label)
	label.setText('Select a device to configure')
	
	def stopper():
		nonlocal stop,window
		stop=True
		window.close()
		#app.quit()
		#raise StopIteration
	
	hid_boxes=[]
	for hid in DETECTEDHIDS:
		radioButton=QtWidgets.QRadioButton(parent=window)
		radioButton.setText(hid.event_by_id)
		hid_boxes.append((radioButton, hid))
		layout.addWidget(radioButton)
	radioButton.setChecked(True)
	stop_button,ok_button=add_buttons(('Stop','OK'),window,layout)
	ok_button.clicked.connect(window.close)
	stop_button.clicked.connect(stopper)
	window.show()
	app.exec()
	
	if stop:
		return None
	for radioButton, hid in hid_boxes:
		if radioButton.isChecked():
			return hid

async def main():
	# print (get_active_class_class())
	# exit(0)
	hid = device_select_one_gui()
	print(f'Selected: {hid}')
	hid.register_user_events()
	
	exit(0)
	
def configs_creator():
	while True:
		hid = device_select_one_gui()
		if not hid:
			print(f'configs_creator return.')
			return
		print(f'"{hid}" selected.')
		hid.register_user_events()

if __name__ == '__main__':
	# get_hid_devices()
	# for i in range(2,6):
	# 	DETECTEDHIDS[i].register_user_events()
	#print(f'{sys.argv}')
	configs_creator()
	#asyncio.run(main())