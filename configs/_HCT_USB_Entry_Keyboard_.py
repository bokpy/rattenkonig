# "/home/bob/python/rattenkonig/test_litter_config/_HCT_USB_Entry_Keyboard_.py"
# Fri Nov 28 05:39:32 2025

import evdev
from evdev import ecodes as ec

piper=None
tag = 0xc0f400090111
sibs = [ "usb-Hengchangtong_HCT_USB_Entry_Keyboard_000000000015-event-kbd", "usb-Hengchangtong_HCT_USB_Entry_Keyboard_000000000015-event-if01", "Hengchangtong__HCT_USB_Entry_Keyboard_System_Control", "usb-Hengchangtong_HCT_USB_Entry_Keyboard_000000000015-if01-event-kbd"]


def act_syn_report(event): # code 0
    global piper
    pass
    #piper.write_event(event)

def act_syn_config(event): # code 1
    global piper
    pass
    #piper.write_event(event)

def act_4(event): # code 4
    global piper
    pass
    #piper.write_event(event)

def act_17(event): # code 17
    global piper
    pass
    #piper.write_event(event)

def act_20(event): # code 20
    global piper
    pass
    #piper.write_event(event)

def act_syn_mt_report(event): # code 2
    global piper
    pass
    #piper.write_event(event)

def act_syn_dropped(event): # code 3
    global piper
    pass
    #piper.write_event(event)

def act_key_esc(event): # code 1
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_1(event): # code 2
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_2(event): # code 3
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_3(event): # code 4
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_4(event): # code 5
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_5(event): # code 6
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_6(event): # code 7
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_7(event): # code 8
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_8(event): # code 9
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_9(event): # code 10
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_0(event): # code 11
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_minus(event): # code 12
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_equal(event): # code 13
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_backspace(event): # code 14
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_tab(event): # code 15
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_q(event): # code 16
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    if event.value == 1:
        piper.message('pp').nap(.3).message("Dit is een opdracht.\n")
    #piper.write_event(event)

def act_key_w(event): # code 17
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_e(event): # code 18
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_r(event): # code 19
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_t(event): # code 20
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_y(event): # code 21
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_u(event): # code 22
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_i(event): # code 23
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_o(event): # code 24
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_p(event): # code 25
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_leftbrace(event): # code 26
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_rightbrace(event): # code 27
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_enter(event): # code 28
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_leftctrl(event): # code 29
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_a(event): # code 30
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_s(event): # code 31
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_d(event): # code 32
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f(event): # code 33
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_g(event): # code 34
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_h(event): # code 35
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_j(event): # code 36
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_k(event): # code 37
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_l(event): # code 38
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_semicolon(event): # code 39
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_apostrophe(event): # code 40
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_grave(event): # code 41
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_leftshift(event): # code 42
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_backslash(event): # code 43
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_z(event): # code 44
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_x(event): # code 45
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_c(event): # code 46
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_v(event): # code 47
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_b(event): # code 48
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_n(event): # code 49
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_m(event): # code 50
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_comma(event): # code 51
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_dot(event): # code 52
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_slash(event): # code 53
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_rightshift(event): # code 54
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kpasterisk(event): # code 55
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_leftalt(event): # code 56
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_space(event): # code 57
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_capslock(event): # code 58
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)


# Gui.activateWorkbench("PartDesignWorkbench")
# Gui.activateWorkbench("PartWorkbench")
# Gui.activateWorkbench("SketcherWorkbench")
# Gui.activateWorkbench("DraftWorkbench")
# Gui.activateWorkbench("SpreadsheetWorkbench")

def act_key_f1(event): # code 59
    global piper
    print(' act_key_f1')
    if event.value == 1:
        piper.message('pp').nap(0.3).message("PartDesignWorkbench")
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return

def act_key_f2(event): # code 60
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    if event.value == 1:
        piper.message('pp').nap(0.3).message("PartWorkbench")


def act_key_f3(event): # code 61
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    if event.value == 1:
        piper.message('pp').nap(0.3).message("SketcherWorkbench")

def act_key_f4(event): # code 62
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    if event.value == 1:
        piper.message('pp').nap(0.3).message("DraftWorkbench")

def act_key_f5(event): # code 63
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    if event.value == 1:
        piper.message('pp').nap(0.3).message("SpreadsheetWorkbench")

def act_key_f6(event): # code 64
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f7(event): # code 65
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f8(event): # code 66
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f9(event): # code 67
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f10(event): # code 68
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_numlock(event): # code 69
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_scrolllock(event): # code 70
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kp7(event): # code 71
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kp8(event): # code 72
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kp9(event): # code 73
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kpminus(event): # code 74
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kp4(event): # code 75
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kp5(event): # code 76
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kp6(event): # code 77
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kpplus(event): # code 78
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kp1(event): # code 79
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kp2(event): # code 80
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kp3(event): # code 81
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kp0(event): # code 82
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kpdot(event): # code 83
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_zenkakuhankaku(event): # code 85
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_102nd(event): # code 86
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f11(event): # code 87
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f12(event): # code 88
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_ro(event): # code 89
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_katakana(event): # code 90
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_hiragana(event): # code 91
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_henkan(event): # code 92
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_katakanahiragana(event): # code 93
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_muhenkan(event): # code 94
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kpjpcomma(event): # code 95
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kpenter(event): # code 96
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_rightctrl(event): # code 97
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kpslash(event): # code 98
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_sysrq(event): # code 99
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_rightalt(event): # code 100
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_home(event): # code 102
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_up(event): # code 103
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_pageup(event): # code 104
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_left(event): # code 105
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_right(event): # code 106
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_end(event): # code 107
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_down(event): # code 108
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_pagedown(event): # code 109
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_insert(event): # code 110
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_delete(event): # code 111
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_min_interesting(event): # code 113
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_volumedown(event): # code 114
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_volumeup(event): # code 115
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_power(event): # code 116
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kpequal(event): # code 117
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_pause(event): # code 119
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kpcomma(event): # code 121
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_hangeul(event): # code 122
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_hanja(event): # code 123
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_yen(event): # code 124
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_leftmeta(event): # code 125
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_rightmeta(event): # code 126
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_compose(event): # code 127
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_stop(event): # code 128
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_again(event): # code 129
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_props(event): # code 130
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_undo(event): # code 131
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_front(event): # code 132
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_copy(event): # code 133
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_open(event): # code 134
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_paste(event): # code 135
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_find(event): # code 136
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_cut(event): # code 137
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_help(event): # code 138
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_calc(event): # code 140
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_sleep(event): # code 142
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_www(event): # code 150
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_coffee(event): # code 152
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_back(event): # code 158
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_forward(event): # code 159
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_ejectcd(event): # code 161
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_nextsong(event): # code 163
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_playpause(event): # code 164
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_previoussong(event): # code 165
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_stopcd(event): # code 166
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_refresh(event): # code 173
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_edit(event): # code 176
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_scrollup(event): # code 177
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_scrolldown(event): # code 178
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kpleftparen(event): # code 179
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kprightparen(event): # code 180
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f13(event): # code 183
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f14(event): # code 184
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f15(event): # code 185
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f16(event): # code 186
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f17(event): # code 187
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f18(event): # code 188
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f19(event): # code 189
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f20(event): # code 190
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f21(event): # code 191
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f22(event): # code 192
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f23(event): # code 193
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_f24(event): # code 194
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_unknown(event): # code 240
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_scale(event): # code 120
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_menu(event): # code 139
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_file(event): # code 144
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_mail(event): # code 155
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_bookmarks(event): # code 156
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_record(event): # code 167
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_rewind(event): # code 168
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_phone(event): # code 169
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_config(event): # code 171
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_homepage(event): # code 172
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_exit(event): # code 174
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_new(event): # code 181
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_redo(event): # code 182
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_all_applications(event): # code 204
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_close(event): # code 206
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_play(event): # code 207
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_fastforward(event): # code 208
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_bassboost(event): # code 209
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_print(event): # code 210
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_camera(event): # code 212
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_chat(event): # code 216
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_search(event): # code 217
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_finance(event): # code 219
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_cancel(event): # code 223
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_brightnessdown(event): # code 224
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_brightnessup(event): # code 225
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kbdillumtoggle(event): # code 228
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kbdillumdown(event): # code 229
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kbdillumup(event): # code 230
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_send(event): # code 231
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_reply(event): # code 232
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_forwardmail(event): # code 233
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_save(event): # code 234
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_documents(event): # code 235
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_video_next(event): # code 241
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_brightness_auto(event): # code 244
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_btn_0(event): # code 256
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_select(event): # code 353
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_goto(event): # code 354
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_info(event): # code 358
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_program(event): # code 362
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_pvr(event): # code 366
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_subtitle(event): # code 370
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_full_screen(event): # code 372
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_keyboard(event): # code 374
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_aspect_ratio(event): # code 375
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_pc(event): # code 376
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_tv(event): # code 377
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_tv2(event): # code 378
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_vcr(event): # code 379
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_vcr2(event): # code 380
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_sat(event): # code 381
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_cd(event): # code 383
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_tape(event): # code 384
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_tuner(event): # code 386
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_player(event): # code 387
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_dvd(event): # code 389
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_audio(event): # code 392
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_video(event): # code 393
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_memo(event): # code 396
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_calendar(event): # code 397
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_red(event): # code 398
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_green(event): # code 399
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_yellow(event): # code 400
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_blue(event): # code 401
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_channelup(event): # code 402
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_channeldown(event): # code 403
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_last(event): # code 405
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_next(event): # code 407
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_restart(event): # code 408
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_slow(event): # code 409
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_shuffle(event): # code 410
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_previous(event): # code 412
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_videophone(event): # code 416
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_games(event): # code 417
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_zoomin(event): # code 418
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_zoomout(event): # code 419
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_zoomreset(event): # code 420
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_wordprocessor(event): # code 421
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_editor(event): # code 422
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_spreadsheet(event): # code 423
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_graphicseditor(event): # code 424
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_presentation(event): # code 425
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_database(event): # code 426
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_news(event): # code 427
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_voicemail(event): # code 428
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_addressbook(event): # code 429
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_messenger(event): # code 430
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_brightness_toggle(event): # code 431
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_spellcheck(event): # code 432
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_logoff(event): # code 433
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_media_repeat(event): # code 439
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_images(event): # code 442
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_buttonconfig(event): # code 576
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_taskmanager(event): # code 577
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_journal(event): # code 578
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_controlpanel(event): # code 579
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_appselect(event): # code 580
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_screensaver(event): # code 581
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_voicecommand(event): # code 582
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_assistant(event): # code 583
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kbd_layout_next(event): # code 584
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_emoji_picker(event): # code 585
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_dictate(event): # code 586
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_camera_access_enable(event): # code 587
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_camera_access_disable(event): # code 588
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_camera_access_toggle(event): # code 589
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_brightness_min(event): # code 592
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_brightness_max(event): # code 593
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kbdinputassist_prev(event): # code 608
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kbdinputassist_next(event): # code 609
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kbdinputassist_prevgroup(event): # code 610
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kbdinputassist_nextgroup(event): # code 611
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kbdinputassist_accept(event): # code 612
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_kbdinputassist_cancel(event): # code 613
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_key_wakeup(event): # code 143
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_rel_hwheel(event): # code 6
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_rel_hwheel_hi_res(event): # code 12
    global piper
    # if not piper.match_active_window():
    #     piper.write_event(event)
    # return
    piper.write_event(event)

def act_abs_volume(event): # code 32
    global piper
    pass
    #piper.write_event(event)

def act_msc_scan(event): # code 4
    global piper
    pass
    #piper.write_event(event)

def act_led_numl(event): # code 0
    global piper
    pass
    #piper.write_event(event)

def act_led_capsl(event): # code 1
    global piper
    pass
    #piper.write_event(event)

def act_led_scrolll(event): # code 2
    global piper
    pass
    #piper.write_event(event)

def act_led_compose(event): # code 3
    global piper
    pass
    #piper.write_event(event)

def act_led_kana(event): # code 4
    global piper
    pass
    #piper.write_event(event)

event_lookup = {
 0:{
       0:act_syn_report
    ,  1:act_syn_config
    ,  4:act_4
    , 17:act_17
    , 20:act_20
    ,  2:act_syn_mt_report
    ,  3:act_syn_dropped
    }
,1:{
       1:act_key_esc
    ,  2:act_key_1
    ,  3:act_key_2
    ,  4:act_key_3
    ,  5:act_key_4
    ,  6:act_key_5
    ,  7:act_key_6
    ,  8:act_key_7
    ,  9:act_key_8
    , 10:act_key_9
    , 11:act_key_0
    , 12:act_key_minus
    , 13:act_key_equal
    , 14:act_key_backspace
    , 15:act_key_tab
    , 16:act_key_q
    , 17:act_key_w
    , 18:act_key_e
    , 19:act_key_r
    , 20:act_key_t
    , 21:act_key_y
    , 22:act_key_u
    , 23:act_key_i
    , 24:act_key_o
    , 25:act_key_p
    , 26:act_key_leftbrace
    , 27:act_key_rightbrace
    , 28:act_key_enter
    , 29:act_key_leftctrl
    , 30:act_key_a
    , 31:act_key_s
    , 32:act_key_d
    , 33:act_key_f
    , 34:act_key_g
    , 35:act_key_h
    , 36:act_key_j
    , 37:act_key_k
    , 38:act_key_l
    , 39:act_key_semicolon
    , 40:act_key_apostrophe
    , 41:act_key_grave
    , 42:act_key_leftshift
    , 43:act_key_backslash
    , 44:act_key_z
    , 45:act_key_x
    , 46:act_key_c
    , 47:act_key_v
    , 48:act_key_b
    , 49:act_key_n
    , 50:act_key_m
    , 51:act_key_comma
    , 52:act_key_dot
    , 53:act_key_slash
    , 54:act_key_rightshift
    , 55:act_key_kpasterisk
    , 56:act_key_leftalt
    , 57:act_key_space
    , 58:act_key_capslock
    , 59:act_key_f1
    , 60:act_key_f2
    , 61:act_key_f3
    , 62:act_key_f4
    , 63:act_key_f5
    , 64:act_key_f6
    , 65:act_key_f7
    , 66:act_key_f8
    , 67:act_key_f9
    , 68:act_key_f10
    , 69:act_key_numlock
    , 70:act_key_scrolllock
    , 71:act_key_kp7
    , 72:act_key_kp8
    , 73:act_key_kp9
    , 74:act_key_kpminus
    , 75:act_key_kp4
    , 76:act_key_kp5
    , 77:act_key_kp6
    , 78:act_key_kpplus
    , 79:act_key_kp1
    , 80:act_key_kp2
    , 81:act_key_kp3
    , 82:act_key_kp0
    , 83:act_key_kpdot
    , 85:act_key_zenkakuhankaku
    , 86:act_key_102nd
    , 87:act_key_f11
    , 88:act_key_f12
    , 89:act_key_ro
    , 90:act_key_katakana
    , 91:act_key_hiragana
    , 92:act_key_henkan
    , 93:act_key_katakanahiragana
    , 94:act_key_muhenkan
    , 95:act_key_kpjpcomma
    , 96:act_key_kpenter
    , 97:act_key_rightctrl
    , 98:act_key_kpslash
    , 99:act_key_sysrq
    ,100:act_key_rightalt
    ,102:act_key_home
    ,103:act_key_up
    ,104:act_key_pageup
    ,105:act_key_left
    ,106:act_key_right
    ,107:act_key_end
    ,108:act_key_down
    ,109:act_key_pagedown
    ,110:act_key_insert
    ,111:act_key_delete
    ,113:act_key_min_interesting
    ,114:act_key_volumedown
    ,115:act_key_volumeup
    ,116:act_key_power
    ,117:act_key_kpequal
    ,119:act_key_pause
    ,121:act_key_kpcomma
    ,122:act_key_hangeul
    ,123:act_key_hanja
    ,124:act_key_yen
    ,125:act_key_leftmeta
    ,126:act_key_rightmeta
    ,127:act_key_compose
    ,128:act_key_stop
    ,129:act_key_again
    ,130:act_key_props
    ,131:act_key_undo
    ,132:act_key_front
    ,133:act_key_copy
    ,134:act_key_open
    ,135:act_key_paste
    ,136:act_key_find
    ,137:act_key_cut
    ,138:act_key_help
    ,140:act_key_calc
    ,142:act_key_sleep
    ,150:act_key_www
    ,152:act_key_coffee
    ,158:act_key_back
    ,159:act_key_forward
    ,161:act_key_ejectcd
    ,163:act_key_nextsong
    ,164:act_key_playpause
    ,165:act_key_previoussong
    ,166:act_key_stopcd
    ,173:act_key_refresh
    ,176:act_key_edit
    ,177:act_key_scrollup
    ,178:act_key_scrolldown
    ,179:act_key_kpleftparen
    ,180:act_key_kprightparen
    ,183:act_key_f13
    ,184:act_key_f14
    ,185:act_key_f15
    ,186:act_key_f16
    ,187:act_key_f17
    ,188:act_key_f18
    ,189:act_key_f19
    ,190:act_key_f20
    ,191:act_key_f21
    ,192:act_key_f22
    ,193:act_key_f23
    ,194:act_key_f24
    ,240:act_key_unknown
    ,120:act_key_scale
    ,139:act_key_menu
    ,144:act_key_file
    ,155:act_key_mail
    ,156:act_key_bookmarks
    ,167:act_key_record
    ,168:act_key_rewind
    ,169:act_key_phone
    ,171:act_key_config
    ,172:act_key_homepage
    ,174:act_key_exit
    ,181:act_key_new
    ,182:act_key_redo
    ,204:act_key_all_applications
    ,206:act_key_close
    ,207:act_key_play
    ,208:act_key_fastforward
    ,209:act_key_bassboost
    ,210:act_key_print
    ,212:act_key_camera
    ,216:act_key_chat
    ,217:act_key_search
    ,219:act_key_finance
    ,223:act_key_cancel
    ,224:act_key_brightnessdown
    ,225:act_key_brightnessup
    ,228:act_key_kbdillumtoggle
    ,229:act_key_kbdillumdown
    ,230:act_key_kbdillumup
    ,231:act_key_send
    ,232:act_key_reply
    ,233:act_key_forwardmail
    ,234:act_key_save
    ,235:act_key_documents
    ,241:act_key_video_next
    ,244:act_key_brightness_auto
    ,256:act_btn_0
    ,353:act_key_select
    ,354:act_key_goto
    ,358:act_key_info
    ,362:act_key_program
    ,366:act_key_pvr
    ,370:act_key_subtitle
    ,372:act_key_full_screen
    ,374:act_key_keyboard
    ,375:act_key_aspect_ratio
    ,376:act_key_pc
    ,377:act_key_tv
    ,378:act_key_tv2
    ,379:act_key_vcr
    ,380:act_key_vcr2
    ,381:act_key_sat
    ,383:act_key_cd
    ,384:act_key_tape
    ,386:act_key_tuner
    ,387:act_key_player
    ,389:act_key_dvd
    ,392:act_key_audio
    ,393:act_key_video
    ,396:act_key_memo
    ,397:act_key_calendar
    ,398:act_key_red
    ,399:act_key_green
    ,400:act_key_yellow
    ,401:act_key_blue
    ,402:act_key_channelup
    ,403:act_key_channeldown
    ,405:act_key_last
    ,407:act_key_next
    ,408:act_key_restart
    ,409:act_key_slow
    ,410:act_key_shuffle
    ,412:act_key_previous
    ,416:act_key_videophone
    ,417:act_key_games
    ,418:act_key_zoomin
    ,419:act_key_zoomout
    ,420:act_key_zoomreset
    ,421:act_key_wordprocessor
    ,422:act_key_editor
    ,423:act_key_spreadsheet
    ,424:act_key_graphicseditor
    ,425:act_key_presentation
    ,426:act_key_database
    ,427:act_key_news
    ,428:act_key_voicemail
    ,429:act_key_addressbook
    ,430:act_key_messenger
    ,431:act_key_brightness_toggle
    ,432:act_key_spellcheck
    ,433:act_key_logoff
    ,439:act_key_media_repeat
    ,442:act_key_images
    ,576:act_key_buttonconfig
    ,577:act_key_taskmanager
    ,578:act_key_journal
    ,579:act_key_controlpanel
    ,580:act_key_appselect
    ,581:act_key_screensaver
    ,582:act_key_voicecommand
    ,583:act_key_assistant
    ,584:act_key_kbd_layout_next
    ,585:act_key_emoji_picker
    ,586:act_key_dictate
    ,587:act_key_camera_access_enable
    ,588:act_key_camera_access_disable
    ,589:act_key_camera_access_toggle
    ,592:act_key_brightness_min
    ,593:act_key_brightness_max
    ,608:act_key_kbdinputassist_prev
    ,609:act_key_kbdinputassist_next
    ,610:act_key_kbdinputassist_prevgroup
    ,611:act_key_kbdinputassist_nextgroup
    ,612:act_key_kbdinputassist_accept
    ,613:act_key_kbdinputassist_cancel
    ,143:act_key_wakeup
    }
,2:{
       6:act_rel_hwheel
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
