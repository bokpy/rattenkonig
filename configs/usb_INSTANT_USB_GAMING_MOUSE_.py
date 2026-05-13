# "/home/bob/python/rattenkonig/configs/usb_INSTANT_USB_GAMING_MOUSE_.py"
# Sat Apr 25 16:08:16 2026

import evdev
from evdev import ecodes as ec
from icecream import ic
ic.configureOutput(includeContext=True)

piper=None
tag = 0x30fa15400110
sibs = [ "usb-INSTANT_USB_GAMING_MOUSE-event-mouse", "usb-INSTANT_USB_GAMING_MOUSE-if01-event-kbd"]

def act_syn_report(event): # code 0
	global piper
	pass
	#piper.squeak_event(event)

def act_syn_config(event): # code 1
	global piper
	pass
	#piper.squeak_event(event)

def act_syn_mt_report(event): # code 2
	global piper
	pass
	#piper.squeak_event(event)

def act_4(event): # code 4
	global piper
	pass
	#piper.squeak_event(event)

def act_syn_dropped(event): # code 3
	global piper
	pass
	#piper.squeak_event(event)

def act_20(event): # code 20
	global piper
	pass
	#piper.squeak_event(event)

def act_btn_left(event): # code 272
	global piper
	# if not piper.match_active_window():
	#     piper.squeak_event(event)
	# return
	piper.squeak_event(event)

def act_btn_right(event): # code 273
	global piper
	# if not piper.match_active_window():
	#     piper.squeak_event(event)
	# return
	piper.squeak_event(event)

def act_btn_middle(event): # code 274
	global piper
	# if not piper.match_active_window():
	#     piper.squeak_event(event)
	# return
	piper.squeak_event(event)

def act_btn_side(event): # code 275
	ic()
	global piper
	# if not piper.match_active_window():
	#     piper.squeak_event(event)
	# return
	piper.squeak_event(event)

def act_btn_extra(event): # code 276
	ic()
	global piper
	# if not piper.match_active_window():
	#     piper.squeak_event(event)
	# return
	piper.squeak_event(event)

def act_btn_0(event): # code 256
	ic()
	global piper
	# if not piper.match_active_window():
	#     piper.squeak_event(event)
	# return
	piper.squeak_event(event)

def act_key_7(event): # code 6 Top back Undo CTRL-Z
	global piper
	nw,nc,cc = piper.id_active_window()
	
	if (event.value ==1 ) and ('FreeCAD' in cc) :
		piper.simultaneous_keys(ec.KEY_LEFTCTRL,ec.KEY_Z)
		return
	
def act_key_6(event): # code 6 Top Front Delete
	global piper
	nw,nc,cc = piper.id_active_window()
	
	if (event.value ==1 ) and ('FreeCAD' in cc) :
		piper.type_key(ec.KEY_DELETE)
		return
	
G2_KEYS=[(ec.KEY_Q,ec.KEY_Y) # Sketch dimensions Pei
	,(ec.KEY_Q,ec.KEY_D,ec.KEY_X)] # Draft Snap Pei

G4_KEYS=[(ec.KEY_P,ec.KEY_Q,ec.KEY_R) # Sketch Draw Pei
	,(ec.KEY_Q,ec.KEY_D,ec.KEY_S)] # Draft Extra Pei
G2_G4=0

def act_key_5(event): # code 6 Button G5 front left side
	global piper,G2_G4
	nw,nc,cc = piper.id_active_window()
	if (event.value ==1 ) and ('FreeCAD' in cc) :
		G2_G4=( G2_G4+1 ) %2
		return

def act_key_4(event): # code 5
	global piper,G2_G4,G4_KEYS
	#('Tasks', 'freecad', 'FreeCAD'  )
	nw,nc,cc = piper.id_active_window()
	val=event.value
	if (val==1) and ('FreeCAD' in cc) :
		piper.type_keys(*G4_KEYS[G2_G4])
		return

def act_key_3(event): # code 4
	ic()
	global piper
	nw,nc,cc = piper.id_active_window()
	val=event.value
	if (val==1) and ('FreeCAD' in cc) :
		piper.type_keys(ec.KEY_Q,ec.KEY_Q)
		return
	piper.squeak_event(event)


def act_key_2( event ):  # code 3
	global piper,G2_G4,G2_KEYS
	nw, nc, cc = piper.id_active_window( )
	val = event.value
	if (val == 1) and ('FreeCAD' in cc):
		ic(G2_KEYS[G2_G4])
		piper.type_keys( *G2_KEYS[G2_G4])
		return

def act_key_1(event): # code 2
	ic()
	global piper
	nw, nc, cc = piper.id_active_window( )
	val = event.value
	if (val == 1) and ('FreeCAD' in cc):
		piper.type_key( ec.KEY_Q ).type_key( ec.KEY_H )
		return

def act_rel_x(event): # code 0
	global piper
	piper.squeak_event(event)

def act_rel_y(event): # code 1
	global piper
	# if not piper.match_active_window():
	#     piper.squeak_event(event)
	# return
	piper.squeak_event(event)

def act_rel_wheel(event): # code 8
	global piper
	# if not piper.match_active_window():
	#     piper.squeak_event(event)
	# return
	piper.squeak_event(event)

def act_rel_wheel_hi_res(event): # code 11
	global piper
	# if not piper.match_active_window():
	#     piper.squeak_event(event)
	# return
	piper.squeak_event(event)

def act_rel_hwheel(event): # code 6
	global piper
	# if not piper.match_active_window():
	#     piper.squeak_event(event)
	# return
	piper.squeak_event(event)

def act_rel_hwheel_hi_res(event): # code 12
	global piper
	# if not piper.match_active_window():
	#     piper.squeak_event(event)
	# return
	piper.squeak_event(event)

def act_abs_volume(event): # code 32
	global piper
	pass
	#piper.squeak_event(event)

def act_msc_scan(event): # code 4
	global piper
	pass
	#piper.squeak_event(event)

event_lookup = {
 0:{
	   0:act_syn_report
	,  1:act_syn_config
	,  2:act_syn_mt_report
	,  4:act_4
	,  3:act_syn_dropped
	, 20:act_20
	}
,1:{
	 272:act_btn_left
	,273:act_btn_right
	,274:act_btn_middle
	,275:act_btn_side
	,276:act_btn_extra
	,256:act_btn_0
	,  8:act_key_7
	,  7:act_key_6
	,  6:act_key_5
	,  5:act_key_4
	,  4:act_key_3
	,  3:act_key_2
	,  2:act_key_1
	}
,2:{
	   0:act_rel_x
	,  1:act_rel_y
	,  8:act_rel_wheel
	, 11:act_rel_wheel_hi_res
	,  6:act_rel_hwheel
	, 12:act_rel_hwheel_hi_res
	}
,3:{
	  32:act_abs_volume
	}
,4:{
	   4:act_msc_scan
	}
,5:{
	}
,17:{
	}
,18:{
	}
,20:{
	}
,21:{
	}
,22:{
	}
,23:{
	}
,31:{
	}
}
