# "/home/bob/python/rattenkonig/configs/2_4G_Mouse.py"
# Sat Apr 25 12:58:24 2026

import evdev
from evdev import ecodes as ec

piper=None
tag = 0x1ea700660110
sibs = [ "usb-1ea7_2.4G_Mouse-event-kbd", "usb-1ea7_2.4G_Mouse-event-if01", "usb-1ea7_2.4G_Mouse-if01-event-mouse", "2.4G_Mouse_Consumer_Control", "2.4G_Mouse_System_Control"]


def act_syn_report(event): # code 0
    global piper
    pass
    #piper.squeak_event(event)

def act_syn_config(event): # code 1
    global piper
    pass
    #piper.squeak_event(event)

def act_4(event): # code 4
    global piper
    pass
    #piper.squeak_event(event)

def act_17(event): # code 17
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

def act_syn_mt_report(event): # code 2
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
    piper.squeak_event(event)

def act_key_s(event): # code 31
    global piper
    # if not piper.match_active_window():
    #     piper.squeak_event(event)
    # return
    piper.squeak_event(event)

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

def act_abs_misc(event): # code 40
    global piper
    pass
    #piper.squeak_event(event)

def act_abs_volume(event): # code 32
    global piper
    pass
    #piper.squeak_event(event)

def act_msc_scan(event): # code 4
    global piper
    pass
    #piper.squeak_event(event)

def act_led_numl(event): # code 0
    global piper
    pass
    #piper.squeak_event(event)

def act_led_capsl(event): # code 1
    global piper
    pass
    #piper.squeak_event(event)

def act_led_scrolll(event): # code 2
    global piper
    pass
    #piper.squeak_event(event)

def act_led_compose(event): # code 3
    global piper
    pass
    #piper.squeak_event(event)

def act_led_kana(event): # code 4
    global piper
    pass
    #piper.squeak_event(event)

event_lookup = {
 0:{
       0:act_syn_report
    ,  1:act_syn_config
    ,  4:act_4
    , 17:act_17
    , 20:act_20
    ,  3:act_syn_dropped
    ,  2:act_syn_mt_report
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
    , 31:act_key_s
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
      40:act_abs_misc
    , 32:act_abs_volume
    }
,4:{
       4:act_msc_scan
    }
,5:{
    }
,17:{
       0:act_led_numl
    ,  1:act_led_capsl
    ,  2:act_led_scrolll
    ,  3:act_led_compose
    ,  4:act_led_kana
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
