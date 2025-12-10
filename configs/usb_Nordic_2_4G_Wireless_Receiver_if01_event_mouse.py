# "/home/bob/python/rattenkonig/test_litter_config/usb_Nordic_2_4G_Wireless_Receiver_if01_event_mouse.py"
# Mon Nov 24 12:33:35 2025

import evdev
from evdev import ecodes as ec
import piper

piper=None
tag = 0x25a7fa100110
sibs = [ "usb-Nordic_2.4G_Wireless_Receiver-if01-event-mouse"]

def FreeCAD_check_value_1(event):
    global piper
    if not event.value == 1:
        return False
    return piper.match_active_window(name='FreeCAD')

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

def act_btn_left(event): # code 272
    global piper 
    print('act_btn_left')

def act_btn_right(event): # code 273
    # ('Insert Length', 'freecad', 'FreeCAD')
    # ('Expression Editor', 'freecad', 'FreeCAD')
    global piper
    nw,nc,cc = piper.id_active_window()
    val=event.value
    if (val==1 ) and ('FreeCAD' in cc) :
        if 'Insert ' in nw:
            piper.message("=")
            return
        if 'Expression' in nw:
            piper.message("Spreadsheet.")
            return
    piper.squeak_event(event)

def act_btn_middle(event): # code 274
    global piper 
    if FreeCAD_check_value_1(event):
        piper.message('v').nap().message('f')

front='1';top='2';right='3';back='4';bottom='5';left='6'

tumble = { front:top, top:back , back:bottom, bottom:front}
spin     = { left:front, front:right,right:back,     back:left}
current_face = front

def act_btn_side(event):  # code 275
    global piper,current_face, tumble
    if FreeCAD_check_value_1(event):
        if current_face in tumble:
            current_face = tumble[current_face]
        else:
            current_face=front
        piper.message(current_face)

def act_btn_extra(event):  # code 276
    global piper,current_face,spin
    if FreeCAD_check_value_1(event):
        if current_face in spin:
            current_face=spin[current_face]
        else:
            current_face=front
        piper.message(current_face)

def rel_x_y(event):
    global piper
    nw,nc,cc = piper.id_active_window()
    if 'FreeCAD' in nw :
        piper.press_and_hold(ec.BTN_MIDDLE).squeak_event(event).release(ec.BTN_MIDDLE)
        return
    if 'PrusaSlicer' in nw :
        return # PrusaSlicer doesn't like this
        #print ('rel_x_y(PrusaSlicer)')
        piper.press_and_hold(ec.BTN_LEFT,ec.BTN_RIGHT)
        print(piper.device.active_keys(verbose=True))
        piper.squeak_event(event)
        piper.release(ec.BTN_RIGHT,ec.BTN_LEFT)
        print(piper.device.active_keys(verbose=True))

def act_rel_x(event): # code 0
    rel_x_y(event)

def act_rel_y(event): # code 1
    rel_x_y(event)

def act_rel_hwheel(event): # code 6
    global piper 
    piper.squeak_event(event)

def act_rel_wheel(event): # code 8
    global piper 
    piper.squeak_event(event)

def act_rel_wheel_hi_res(event): # code 11
    global piper 
    piper.squeak_event(event)

def act_rel_hwheel_hi_res(event): # code 12
    global piper 
    piper.squeak_event(event)

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
    }
,1:{
     272:act_btn_left
    ,273:act_btn_right
    ,274:act_btn_middle
    ,275:act_btn_side
    ,276:act_btn_extra
    }
,2:{
       0:act_rel_x
    ,  1:act_rel_y
    ,  6:act_rel_hwheel
    ,  8:act_rel_wheel
    , 11:act_rel_wheel_hi_res
    , 12:act_rel_hwheel_hi_res
    }
,3:{
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
