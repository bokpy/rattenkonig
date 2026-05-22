#!/bin/python3
import os
import sys
import evdev
from evdev import ecodes as ec
import asyncio
import time

from pexpect import run
from Xlib import X, display
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget
from icecream import ic
ic.configureOutput(includeContext=True)

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
	ic(window_id_prop)
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

class HID_Device(evdev.InputDevice):
	def __init__(S,event_by_id,event_path):
		S.event_by_id = event_by_id
		evdev.InputDevice.__init__(S,event_path)
		S.know_events = set()
		S.quite_widget=None
		
	def close(S):
		S.super().ungrab()
		S.super().close()
	
	async def call_me(S,action):
	#def call_me(S):
		try:
			#async for event in dev.async_read_loop():
			async for event in S.async_read_loop():
				action(event)
		except Exception as e:
			ic(e)
	
	async def gather_events(S):
		def get_event(event):
			code_type=(event.code,event.type)
			if not code_type in S.know_events:
				S.know_events.add(code_type)
				print(f'New event {evdev.categorize(event)}')
				print(f'{event}')
				# item=QtWidgets.QTreeWidgetItem(S.quite_widget)
				# item.setText(0, S.event_by_id)
				# item.setText(0, S.event_by_id)
	
		#S.quite_widget = device_actions_table(S.event_by_id)
		#await asyncio.gather(S.call_me(get_event))
		await S.call_me(get_event)
	
def get_hid_devices():
	hid_devices=[]
	for by_id_path in os.listdir('/dev/input/by-id'):
		#print(f'{'/dev/input/by-id/'+by_id_path}')
		abs_path = get_abs_path('/dev/input/by-id/'+by_id_path)
		if '/dev/input/event' in abs_path:
			hid_devices.append(HID_Device(event_by_id=by_id_path,event_path=abs_path))
	return hid_devices

def add_ok_button(window,layout):
	spacer=QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
	layout.addItem(spacer)
	okLayout=QtWidgets.QHBoxLayout()
	layout.addItem(okLayout)
	okButton=QtWidgets.QPushButton(parent=window)
	okButton.setText("OK")
	okSpacer=QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
	okLayout.addItem(okSpacer)
	okLayout.addWidget(okButton)
	okButton.clicked.connect(window.close)
	
def device_selector_gui():
	HIDs = get_hid_devices()
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
	for hid in HIDs:
		checkBox = QtWidgets.QCheckBox(parent=window)
		checkBox.setText(hid.event_by_id)
		hid_boxes.append((checkBox,hid))
		layout.addWidget(checkBox)
	
	# spacer=QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
	# layout.addItem(spacer)
	add_ok_button(window,layout)
	window.show()
	app.exec()
	
	checked  = [ hid for checkbox,hid in hid_boxes if checkbox.isChecked() ]
	return checked

def device_select_one_gui():
	HIDs=get_hid_devices()
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
	
	hid_boxes=[]
	for hid in HIDs:
		radioButton=QtWidgets.QRadioButton(parent=window)
		radioButton.setText(hid.event_by_id)
		hid_boxes.append((radioButton, hid))
		layout.addWidget(radioButton)
	radioButton.setChecked(True)
	add_ok_button(window,layout)
	window.show()
	app.exec()
	
	for radioButton, hid in hid_boxes:
		if radioButton.isChecked():
			return hid

def device_actions_table(name):
	app=QApplication(sys.argv)
	
	window=QtWidgets.QWidget(windowTitle=f'Test actions for "{name}"')
	window.resize(800, 600)
	layout=QtWidgets.QVBoxLayout()
	window.setLayout(layout)
	tree = QtWidgets.QTreeWidget(window)
	tree.setColumnCount(4)
	tree.setHeaderLabels(('name','class','class','function'))
	layout.addWidget(tree)
	add_ok_button(window,layout)
	window.show()
	app.exec()
	
async def main():
	# print (get_active_class_class())
	# exit(0)
	hid = device_select_one_gui()
	print(f'Selected: {hid}')
	hid.grab()
	#asyncio.waitrun(
	await hid.gather_events()
	#device_actions_gui(hid)
	exit(0)
	
	hids = device_selector_gui()
	for hid in hids:
		print(hid)
	
	exit(0)
	
	HIDs = get_hid_devices()
	for hid in HIDs:
		print(hid)

if __name__ == '__main__':
	print(f'{sys.argv}')
	device_actions_table('device actions table')
	#asyncio.run(main())