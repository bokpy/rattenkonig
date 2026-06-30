#!/bin/python3
import os
import sys
import argparse
import threading
import hid_device as hd
from event_config import  gen_code_key_class_title
import re
import json
import time
from evdev import ecodes as ec
from Xlib import X, display
import asyncio
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import (
QIcon
,QAction
)
from PyQt6.QtCore import (
 Qt
,QObject
,pyqtSignal
,pyqtSlot
,QThread
)
from PyQt6.QtWidgets import (
 QApplication
,QMainWindow
,QTreeWidgetItem
,QWidget
,QTableWidgetItem
,QHeaderView
)
from PyQt6 import uic
#from qasync import asyncSlot, QEventLoop, QApplication
#from ui.eventSelector import Ui_MainWindow
from PyQt6.QtWidgets import QSizePolicy as sp

EXPANDING=sp.Policy.Expanding
FIXED=sp.Policy.Fixed
IGNORED =sp.Policy.Ignored
MAXIMUM=sp.Policy. Maximum
MINIMUM=sp.Policy.Minimum
MINIMUMEXPANDING=sp.Policy.MinimumExpanding
PREFERRED=sp.Policy.Preferred

DEVICE_TO_SETUP=None

from icecream import ic
ic.configureOutput(includeContext=True)


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

hd.CONFIGDIR = args.configdir
if hd.CONFIGDIR[-1:] != '/':
	hd.CONFIGDIR+= '/'

def limit_string_len(string,length):
	ls=len(string)
	if ls<=length:
		return string
	over_length = ls - length
	if over_length < 3:
		return string[:-over_length]
	lfront=length//2
	lback=length-lfront
	return string[:lfront-2] + '...' + string[1-lback:]

TRIGGEREVENTS={ec.EV_REL,ec.EV_ABS,ec.EV_KEY}

class WorkerEventReader(QObject):
	# class class
	signal_new_window  = pyqtSignal(str,str)
	# event code event name
	signal_new_event      = pyqtSignal(int,str)
	#finished         = pyqtSignal()
	signal_paused = pyqtSignal()
	
	def __init__(S):
		super().__init__()
		S.running = True
		
	def pause(S):
		global DEVICE_TO_SETUP
		DEVICE_TO_SETUP=None
		
	def disconnect_setup_device(S):
		global DEVICE_TO_SETUP
		if DEVICE_TO_SETUP:
			DEVICE_TO_SETUP.disconnect()
		DEVICE_TO_SETUP = None
		
	def set_device(S,device):
		global DEVICE_TO_SETUP
		S.disconnect_setup_device()
		if not device:
			return
		device.connect()
		DEVICE_TO_SETUP = device
		
	def run(S):
		global  DEVICE_TO_SETUP
		
		while S.running:
			if not DEVICE_TO_SETUP:
				S.signal_paused.emit()
				time.sleep(.4)
				continue
			event = DEVICE_TO_SETUP.inputdevice.read_one()
			if not event or event.type not in TRIGGEREVENTS:
				time.sleep(0.02)
				continue
			
			code,key,clss,title=gen_code_key_class_title(event)
			# ic(code,key,clss,title)
			# ic(event)
			
			if DEVICE_TO_SETUP.eventset.stores_new(( code,key)):
				S.signal_new_event.emit(code,key)
			
			if DEVICE_TO_SETUP.windowset.stores_new((clss,title)):
				S.signal_new_window.emit(clss,title)
			#time.sleep(0.1)
		print('EventReader.run() stopped.')

class DeviceSetupGui(QMainWindow):
	
	DEVICEPAGE,EVENTPAGE=0,1
	
	def __init__(S):
		super().__init__()
		S.setWindowTitle('Piper')
		S.resize(800, 600)
		S.setWindowIcon(QIcon('./data/Pied Piper 1.jpeg'))
		S.on_top=False
		
		S.page_stack=QtWidgets.QStackedWidget(S)
		S.setCentralWidget(S.page_stack)
		S.device_selector_gui = DeviceSelectorGui()
		S.key_class_sel_gui      = KeyClassGui()
		
		S.page_stack.insertWidget(S.DEVICEPAGE,S.device_selector_gui)
		S.page_stack.insertWidget(S.EVENTPAGE ,S.key_class_sel_gui)
		
		S.key_class_sel_gui.eventTable.setHorizontalHeaderLabels(['code','event','number','class','class'])
		
		#S.device_selector_gui.quit_button.clicked.connect(S.save)
		S.device_selector_gui.ok_button.clicked.connect(S.page_toggle)
		S.key_class_sel_gui.back_button.clicked.connect(S.page_toggle)
		
		S.device_selector_gui.quit_button.clicked.connect(S.quit)
		S.key_class_sel_gui.quit_button.clicked.connect(S.quit)
		
		S.device_selector_gui.ontop_button.clicked.connect(S.stay_on_top)
		S.key_class_sel_gui.ontop_button.clicked.connect(S.stay_on_top)
		S.update()
		S.layout().update()
	
	def quit(S):
		S.device_selector_gui.close()
		S.key_class_sel_gui.stop()
		S.close()
	
	def stay_on_top(S):
		if S.on_top:
			S.setWindowFlags(Qt.WindowType.Window)
		else:
			S.setWindowFlags(
			Qt.WindowType.Window
			|Qt.WindowType.WindowStaysOnTopHint
			|Qt.WindowType.X11BypassWindowManagerHint
			)
		S.on_top = not S.on_top
		S.show()
	# def actualize_event(S):
	# 	global DEVICE_TO_SETUP
	# 	dss = S.device_selector_gui.selected
	# 	ic(dss,DEVICE_TO_SETUP)
	# 	S.key_class_sel_gui.event_reader.change_device(dss)
	# 	S.key_class_sel_gui.update_table()
	#
	def page_toggle(S):
		if not S.device_selector_gui.selected:
			print(f'No selected device.')
			return
		page={S.EVENTPAGE:'event page',S.DEVICEPAGE:'device page'}
		if S.page_stack.currentIndex() == S.DEVICEPAGE:
			S.key_class_sel_gui.change_device(S.device_selector_gui.selected)
			S.page_stack.setCurrentIndex(S.EVENTPAGE)
			S.setWindowTitle(f'HID "{DEVICE_TO_SETUP.event_by_id}"')
		else:
			S.key_class_sel_gui.change_device(None)
			S.page_stack.setCurrentIndex(S.DEVICEPAGE)
			S.setWindowTitle(f'Device Selection')
		print(f'current page_stack {page[S.page_stack.currentIndex()]}')
		S.update()

CODECOL  =0
KEYCOL      =1
CLASSCOL =2
TITLECOL  =3

class KeyClassGui(QtWidgets.QWidget):
#class KeyClassGui(QMainWindow):
	def __init__(S):
		super().__init__()
		w=800
		h=600
		S.setObjectName("Code_Key_Class_Title")
		S.resize(w,h)
		S.setWindowIcon(QIcon('./data/Pied Piper 1.jpeg'))
		layout=QtWidgets.QVBoxLayout(S)
		et = S.eventTable=QtWidgets.QTableWidget(S)
		layout.addWidget(et)
		et.setColumnCount(5)
		i=0;rest_width=w-40
		for width in 60,160,230,230,00:
			#print(f'{rest_width=}')
			if width == 0:
				et.setColumnWidth(i,rest_width)
			else:
				et.setColumnWidth(i,width)
			rest_width-=width
			i+=1
		S.table_header_set=False
		S.event_table_row=S.window_table_row=0

		S.ontop_button,S.commit_button,S.save_button,S.clear_button, S.quit_button, S.back_button\
			=add_buttons(('Ontop','Commit','Save','Clear','Quit', 'Back'), S, layout)
		S.setLayout(layout)
		
		#ok_button.clicked.connect(S.stop)
		S.clear_button.clicked.connect(S.wipe_clean)
		S.save_button.clicked.connect(S.save)
		S.commit_button.clicked.connect(S.ad_mutations)
		# event_reader thread setup
		erW = S.event_reader=WorkerEventReader()
		erT = S.event_reader_thread=QThread()
		erW.signal_new_event.connect(S.display_event)
		erW.signal_new_window.connect(S.display_classes)
		erW.moveToThread(erT)
		erT.started.connect(erW.run)
		erT.start()
		S.update()
		S.layout().update()
	
	def try_to_set_labels(S): # ugly but it works
		if S.table_header_set:
			return
		et = S.eventTable
		headeritem=et.horizontalHeaderItem(0)
		
		if headeritem and headeritem.text() == 'code':
			S.table_header_set = True
			return
		et.setHorizontalHeaderLabels(['code','event','class','title','spare'])
		
		to_content=QHeaderView.ResizeMode.ResizeToContents
		for i in range(0,4):
			et.horizontalHeader().setSectionResizeMode( i ,to_content)
		et.horizontalHeader().setSectionResizeMode(i+1, QtWidgets.QHeaderView.ResizeMode.Stretch)
		# depricated -> et.horizontalHeader().setStretchLastSection(True)

	def stop(S):
		S.event_reader.running=False
		S.event_reader_thread.quit()
		S.event_reader_thread.wait()
		del S.event_reader_thread
		S.close()
	
	def wipe_clean(S):
		global DEVICE_TO_SETUP
		if not DEVICE_TO_SETUP:
			return
		DEVICE_TO_SETUP.clear_config()
		S.eventTable.clear()
		S.table_header_set=False
		S.event_table_row=S.window_table_row=0
		S.update()

	def change_device(S,device):
		ic()
		global DEVICE_TO_SETUP
		S.event_reader.set_device(device)
		if not DEVICE_TO_SETUP:
			return
		S.event_table_row=S.window_table_row=0
		S.eventTable.clear()
		for item in DEVICE_TO_SETUP.eventset:
			S.display_event(*item)
		for item in DEVICE_TO_SETUP.windowset:
			S.display_classes(*item)
		S.update()
		
	def ad_mutations(S):
		global DEVICE_TO_SETUP
		S.save()
		DEVICE_TO_SETUP.config_update()
		S.commit_button.setText('Commited')
		print(f'ad_mutations{DEVICE_TO_SETUP.event_by_id})')
	
	def leave(S):
		global DEVICE_TO_SETUP
		print(f'stores_and_leave({DEVICE_TO_SETUP.event_by_id})')
		S.close()
	
	def save(S):
		global DEVICE_TO_SETUP # print(f'save({WorkerEventReader.device.name})')
		et=S.eventTable
		for i in range(S.window_table_row):
			checkbox=et.cellWidget(i,TITLECOL)
			if not checkbox:
				continue
			if not checkbox.isChecked():
				tT=checkbox.toolTip()
				print(f'Remove {checkbox.toolTip()}')
				try:
					DEVICE_TO_SETUP.windowset.takeout(None,tT)
				except KeyError:
					DEVICE_TO_SETUP.windowset.show()

		DEVICE_TO_SETUP.write_sets()
		S.save_button.setText('Saved')
		S.commit_button.setText('Commit')
		
	def display_event(S,code, name):
		
		#print(f'display_event({code},"{name}")')
		et=S.eventTable
		if et.rowCount()<= S.event_table_row:
			et.insertRow(S.event_table_row)
		et.setItem(S.event_table_row, 0, QTableWidgetItem(code))
		et.setItem(S.event_table_row, 1, QTableWidgetItem(name))
		S.save_button.setText('Save')
		S.commit_button.setText('Commit')
		S.try_to_set_labels()
		# some scrolling if needed
		# index=et.model().index(S.event_table_row, 0)
		# et.scrollTo(index)
		et.update()
		S.event_table_row+=1
		
	def display_classes(S,prime_class,title):
		#print(f'display_classes("{prime_class }", "{title}")')
		et=S.eventTable
		if et.rowCount()<=S.window_table_row:
			# need a new row in the table
			et.insertRow(S.window_table_row)
		cls=limit_string_len(prime_class,24)
		et.setItem(S.window_table_row,CLASSCOL,QTableWidgetItem(cls))
		if title:
			ttl=limit_string_len(title,36)
			title_widget=QtWidgets.QCheckBox(ttl)
			title_widget.setToolTip(title)
			title_widget.setChecked(True)
			et.setCellWidget(S.window_table_row,TITLECOL,title_widget)
			# item=QTableWidgetItem(ttl)
			# item.setFlags( Qt.ItemFlag.ItemIsEnabled
			#                     | Qt.ItemFlag.ItemIsSelectable
			#                     | Qt.ItemFlag.ItemIsUserCheckable
			#                     )
			#et.setItem(S.window_table_row, TITLECOL, item)
		S.save_button.setText('Save')
		S.commit_button.setText('Commit')
		
		# some scrolling if needed
		# index=et.model().index(S.window_table_row, 2)
		# et.scrollTo(index)
		et.update()
		S.window_table_row+=1

def off_display_classes(S, prime_class, title):
	print(f'display_classes("{prime_class}", "{title}")')
	cls=limit_string_len(prime_class, 24)
	ttl=limit_string_len(title, 36)
	et=S.eventTable
	if et.rowCount()<=S.window_table_row:
		et.insertRow(S.window_table_row)
	if title:
		item=QTableWidgetItem(ttl)
		item.setFlags(Qt.ItemFlag.ItemIsEnabled
		              |Qt.ItemFlag.ItemIsSelectable
		              |Qt.ItemFlag.ItemIsUserCheckable
		              )
		et.setItem(S.window_table_row, TITLECOL, item)
	et.setItem(S.window_table_row, CLASSCOL, QTableWidgetItem(cls))
	S.save_button.setText('Save')
	S.commit_button.setText('Commit')
	
	# some scrolling if needed
	# index=et.model().index(S.window_table_row, 2)
	# et.scrollTo(index)
	et.update()
	S.window_table_row+=1

def add_buttons(names,window,layout):
	buttons=[]
	def make_button(name):
		button = QtWidgets.QPushButton(parent=window)
		button.setText(name)
		window.button_layout.addWidget(button)
		buttons.append(button)
	
	spacer=QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
	layout.addItem(spacer)
	window.button_layout=QtWidgets.QHBoxLayout()
	layout.addItem(window.button_layout)
	spacer=QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
	window.button_layout.addItem(spacer)
	
	#Single button
	if isinstance(names,str):
		make_button(names)
		return buttons[0]

	# buttons in a row
	for label in names:
		make_button(label)
	return buttons

class DeviceSelectorGui(QtWidgets.QWidget):
	HIDEVICES=None
	def __init__(S):
		super().__init__()
		#S.QWidget.ser(windowTitle='HID devices by id.')
		layout = QtWidgets.QVBoxLayout()
		S.setLayout(layout)
		if not S.HIDEVICES:
			S.HIDEVICES=hd.get_hid_devices()

		S.hiddict={}
		for hid in S.HIDEVICES:
			event_id = hid.event_no + '   ' +hid.event_by_id
			S.hiddict[event_id] = hid
			radioBut = QtWidgets.QRadioButton(event_id,parent=S)
			layout.addWidget(radioBut)
			radioBut.toggled.connect(S.update)
		S.selected=None
	
		S.ontop_button,S.quit_button,S.ok_button = add_buttons(('Ontop','Quit','OK'),S,layout)
		S.ok_button.clicked.connect(S.leave)
		#S.quit_button.clicked.connect(S.close)
	
	def update(S):
		rb=S.sender()
		if rb.isChecked():
			S.selected=S.hiddict[rb.text()]
			print(f'Button {rb.text()} selected')
			
	def leave(S):
		def show_warning():
			msg = QtWidgets.QMessageBox(S)
			msg.setWindowTitle("Warning")
			msg.setText("Select a Device first or Quit")
			msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
			msg.setStyleSheet("""
						QMessageBox {
							background-color: #FF0000;
							color: #FFFF00;
							font-family: monospace;
							font-size: 16px;
							border: 4px solid #000000;
						}
						/* Force text color on the message label */
				QMessageBox > QLabel {
					color: #FFFF00;
					background-color: #FF0000;
				}
				QMessageBox > QLabel#qt-message-box-label {
					color: #FFFF00;
				}
						QPushButton {
							background-color: #555555;
							color: #FFFF00;
							border: 2px solid #000000;
							padding: 5px 10px;
							font-family: monospace;
						}
						QPushButton:hover {
							background-color: #777777;
						}
					""")
			msg.exec()
			
		if not S.selected:
			show_warning()
			return
		S.close()

def main():
	
	app = QApplication(sys.argv)
	test=2
	if test==0:
		WorkerEventReader.device = hd.HID_Device('usb-Nordic_2.4G_Wireless_Receiver-if01-event-mouse')
		WorkerEventReader.device.connect()
		eventWindowWindow = KeyClassGui()
		eventWindowWindow.update_table()
		eventWindowWindow.show()
	elif test==1:
		selectorWindow = DeviceSelectorGui()
		selectorWindow.show()
	elif test==2:
		setupWindow = DeviceSetupGui()
		setupWindow.show()
	
	app.exec()

def make_checkbox(S,content):
	checkBox = QtWidgets.QCheckBox(S)
	checkBox.setObjectName(u'{content}')
	checkBox.setGeometry(QtCore.QRect(211, 200, 331, 35))
	sizePolicy = QtWidgets.QSizePolicy(EXPANDING, FIXED)
	sizePolicy.setHorizontalStretch(0)
	sizePolicy.setVerticalStretch(0)
	sizePolicy.setHeightForWidth(checkBox.sizePolicy().hasHeightForWidth())
	checkBox.setSizePolicy(sizePolicy)
	return checkBox

	
if __name__ == '__main__':
	main()
	