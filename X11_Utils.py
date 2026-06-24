import time
from Xlib import X,display
from Xlib.error import BadWindow

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
	#ic(cls_prop)
	if not cls_prop:
		return (None,None)
	cc = cls_prop.value.decode('utf-8', 'ignore')
	cc = cc.split('\x00')
	return ( cc[0],cc[1])

# from PyQt6.QtWidgets import QApplication
#
# class ClipboardText:
# 	def __init__(S):
# 		S.board=QApplication.clipboard()
#
# 	def clip(S):
# 		#clipboard = QApplication.clipboard()
# 		#tekst = clipboard.text(mode=clipboard.Mode.Selection)
#
# 		return S.board.text()
	
def get_active_title_class_class():
	d = display.Display()
	root = d.screen().root

	win_id = root.get_full_property(
		d.intern_atom('_NET_ACTIVE_WINDOW'),
		0
	).value[0]

	window = d.create_resource_object('window', win_id)
	try:
		titel = window.get_wm_name()
		if isinstance(titel,bytes):
			titel = titel.decode('utf-8', 'ignore')
		wm_class = window.get_wm_class()
		return titel, *wm_class
	except BadWindow:
		return '','',''

def window_onder_muis():
	d = display.Display()
	root = d.screen().root

	pointer = root.query_pointer()
	window = pointer.child

	if window == 0:
		return None, None

	titel = window.get_wm_name()
	wm_class = window.get_wm_class()

	return titel, wm_class

def window_onder_muis_2():
	d = display.Display()
	root = d.screen().root

	win = root.query_pointer().child

	while win:
		try:
			wm_class = win.get_wm_class()
			titel = win.get_wm_name()
			if wm_class:
				return titel, wm_class
			win = win.query_tree().parent
		except Exception:
			break

	return None, None
	

if __name__ == '__main__':
	print(f'\nget_actieve_title_class_class()')
	for  i in range(0,5):
		time.sleep(1)
		titel, primo,secundo = get_active_title_class_class()
		print("Titel:", titel)
		print("Class:", primo,secundo)
	
	print(f'\nwindow_onder_muis()')
	titel, wm_class=window_onder_muis()
	print("Titel:", titel)
	print("Class:", wm_class)
	
	print(f'\nwindow_onder_muis_2()')
	titel, wm_class=window_onder_muis_2()
	print("Titel:", titel)
	print("Class:", wm_class)
	
	# board=ClipboardText()
	# for i in range(0,5):
	# 	print (f'{i:02d}:"{board.clip()}"')
	# 	time.sleep(1)