# "/home/bob/python/rattenkonig/configs/USB_Gaming_Mouse.py"
# Sun Nov 30 12:12:32 2025

import evdev
from evdev import ecodes as ec

piper=None
tag = 0x4d9fc4d0110
sibs = [ "usb-04d9_USB_Gaming_Mouse-event-mouse", "usb-04d9_USB_Gaming_Mouse-if01-event-kbd", "usb-04d9_USB_Gaming_Mouse-event-if02", "USB_Gaming_Mouse"]


def freecad_window_key_presses(event,key_string):
    global piper
    if event.value != 1:
        return False
    if not piper.match_active_window(name='FreeCAD'):
        return False
    piper.message(key_string)
    return True

    return wrapper
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

def act_20(event): # code 20
    global piper
    pass
    #piper.squeak_event(event)

def act_syn_dropped(event): # code 3
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
    global piper
    # if not piper.match_active_window():
    #     piper.squeak_event(event)
    # return
    piper.squeak_event(event)

def act_btn_extra(event): # code 276
    global piper
    # if not piper.match_active_window():
    #     piper.squeak_event(event)
    # return
    piper.squeak_event(event)

def act_btn_forward(event): # code 277
    global piper
    # if not piper.match_active_window():
    #     piper.squeak_event(event)
    # return
    piper.squeak_event(event)

def act_btn_back(event): # code 278
    global piper
    # if not piper.match_active_window():
    #     piper.squeak_event(event)
    # return
    piper.squeak_event(event)

def act_btn_task(event): # code 279
    global piper
    # if not piper.match_active_window():
    #     piper.squeak_event(event)
    # return
    piper.squeak_event(event)

def act_btn_0(event): # code 256
    global piper
    # if not piper.match_active_window():
    #     piper.squeak_event(event)
    # return
    print('act_btn_0')

def act_key_3(event): # code 4
    global piper
    # if not piper.match_active_window():
    #     piper.squeak_event(event)
    # return
    print('act_key_3')

def act_key_2(event): # code 3
    global piper
    nw,nc,cc = piper.id_active_window()
    val=event.value
    # constraints pei menu
    if (val==1 ) and ('FreeCAD' in nw) :
        piper.message("qd")
        return

def act_key_1(event): # code 2
    global piper
    freecad_window_key_presses(event, 'd')

def act_key_4(event): # code 5
    global piper
    # if not piper.match_active_window():
    #     print('act_key_')
    # return
    print('act_key_4')

def act_key_5(event): # code 6
    global piper
    nw,nc,cc = piper.id_active_window()
    val=event.value
    # sketcher geometry pei menu
    if (val==1 ) and ('FreeCAD' in nw) :
        piper.message("qg")
        return
    
def act_key_6(event): # code 7
    global piper
    # if not piper.match_active_window():
    #     print('act_key_')
    # return
    print('act_key_6')

def act_key_9(event): # code 10
    global piper
    # if not piper.match_active_window():
    #     print('act_key_')
    # return
    print('act_key_9')

def act_key_8(event): # code 9
    global piper
    # if not piper.match_active_window():
    #     print('act_key_')
    # return
    print('act_key_8')

def act_key_7(event): # code 8
    global piper
    # if not piper.match_active_window():
    #     print('act_key_')
    # return
    print('act_key_7')

def act_key_0(event): # code 11 mouse button 10
    global piper
    pass
    #print('act_key_')

def act_key_kpplus(event): # code 78 mouse button 11/12?
    global piper
    # if not piper.match_active_window():
    #     print('act_key_')
    # return
    print('act_key_kpplus')

def act_key_kpminus(event): # code 74 mouse button 12/11?
    global piper
    # if not piper.match_active_window():
    #     print('act_key_')
    # return
    print('act_key_kpminus')

def act_rel_x(event): # code 0
    global piper
    # if not piper.match_active_window():
    #     piper.squeak_event(event)
    # return
    piper.squeak_event(event)

def act_rel_y(event): # code 1
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

def act_abs_misc(event): # code 40
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
    , 20:act_20
    ,  3:act_syn_dropped
    }
,1:{
     272:act_btn_left
    ,273:act_btn_right
    ,274:act_btn_middle
    ,275:act_btn_side
    ,276:act_btn_extra
    ,277:act_btn_forward
    ,278:act_btn_back
    ,279:act_btn_task
    ,256:act_btn_0
    ,  4:act_key_3
    ,  3:act_key_2
    ,  2:act_key_1
    ,  5:act_key_4
    ,  6:act_key_5
    ,  7:act_key_6
    , 10:act_key_9
    ,  9:act_key_8
    ,  8:act_key_7
    , 11:act_key_0
    , 78:act_key_kpplus
    , 74:act_key_kpminus
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
      32:act_abs_volume
    , 40:act_abs_misc
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
