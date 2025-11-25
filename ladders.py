from evdev import ecodes as ec
from icecream import ic
ic.configureOutput(includeContext=True)

event_types_by_name={
    "EV_SYN":0
    ,"EV_KEY":1
    ,"EV_REL":2
    ,"EV_ABS":3
    ,"EV_MSC":4
    ,"EV_SW":5
    ,"EV_LED":17
    ,"EV_SND":18
    ,"EV_REP":20
    ,"EV_FF":21
    ,"EV_PWR":22
    ,"EV_FF_STATUS":23
    ,"EV_MAX":31
    ,"EV_CNT":32
}
event_types_by_number={v: k for k, v in event_types_by_name.items()}
ev_types=[0,1,2,3,4,5,17,18,20,21,22,23,31]

bus_type={
1:"Pci",
2:"Isapnp",
3:"Usb",
4:"Hil",
5:"Bluetooth",
6:"Virtual",
16:"Isa",
17:"I8042",
18:"Xtkbd",
19:"Rs232",
20:"Gameport",
21:"Parport",
22:"Amiga",
23:"Adb",
24:"I2c",
25:"Host",
26:"Gsc",
27:"Atari",
28:"Spi",
29:"Rmi",
30:"Cec",
31:"Intel_ishtp",
32:"Amd_sfh"
}
ascii_to_evdev = {
    0: (None, False)
    , 7: (None, False)
    , 8: (14, False)
    , 9: (15, False)
    , 10: (28, False)
    , 13: (28, False)
    , 27: (1, False)
    , 32: (57, False)
    , 48: (11, False)  # 0
    , 49: (2, False)  # 1
    , 50: (3, False)  # 2
    , 51: (4, False)  # 3
    , 52: (5, False)  # 4
    , 53: (6, False)  # 5
    , 54: (7, False)  # 6
    , 55: (8, False)  # 7
    , 56: (9, False)  # 8
    , 57: (10, False)  # 9
    , 33: (2, True)  # !
    , 64: (3, True)  # @
    , 35: (4, True)  # #
    , 36: (5, True)  # $
    , 37: (6, True)  # %
    , 94: (7, True)  # ^
    , 38: (8, True)  # &
    , 42: (9, True)  # *
    , 40: (10, True)  # (
    , 41: (11, True)  # )
    , 97: (30, False)  # a
    , 98: (48, False)  # b
    , 99: (46, False)  # c
    , 100: (32, False)  # d
    , 101: (18, False)  # e
    , 102: (33, False)  # f
    , 103: (34, False)  # g
    , 104: (35, False)  # h
    , 105: (23, False)  # i
    , 106: (36, False)  # j
    , 107: (37, False)  # k
    , 108: (38, False)  # l
    , 109: (50, False)  # m
    , 110: (49, False)  # n
    , 111: (24, False)  # o
    , 112: (25, False)  # p
    , 113: (16, False)  # q
    , 114: (19, False)  # r
    , 115: (31, False)  # s
    , 116: (20, False)  # t
    , 117: (22, False)  # u
    , 118: (47, False)  # v
    , 119: (17, False)  # w
    , 120: (45, False)  # x
    , 121: (21, False)  # y
    , 122: (44, False)  # z
    , 65: (30, True)  # A
    , 66: (48, True)  # B
    , 67: (46, True)  # C
    , 68: (32, True)  # D
    , 69: (18, True)  # E
    , 70: (33, True)  # F
    , 71: (34, True)  # G
    , 72: (35, True)  # H
    , 73: (23, True)  # I
    , 74: (36, True)  # J
    , 75: (37, True)  # K
    , 76: (38, True)  # L
    , 77: (50, True)  # M
    , 78: (49, True)  # N
    , 79: (24, True)  # O
    , 80: (25, True)  # P
    , 81: (16, True)  # Q
    , 82: (19, True)  # R
    , 83: (31, True)  # S
    , 84: (20, True)  # T
    , 85: (22, True)  # U
    , 86: (47, True)  # V
    , 87: (17, True)  # W
    , 88: (45, True)  # X
    , 89: (21, True)  # Y
    , 90: (44, True)  # Z
    , 45: (12, False)  # -
    , 95: (12, True)  # _
    , 61: (13, False)  # =
    , 43: (13, True)  # +
    , 91: (26, False)  # [
    , 123: (26, True)  # {
    , 93: (27, False)  # ]
    , 125: (27, True)  # }
    , 92: (43, False)  # \
    , 124: (43, True)  # |
    , 59: (39, False)  # ;
    , 58: (39, True)  # :
    , 39: (40, False)  # '
    , 34: (40, True)  # "
    , 44: (51, False)  # ,
    , 60: (51, True)  # <
    , 46: (52, False)  # .
    , 62: (52, True)  # >
    , 47: (53, False)  # /
    , 63: (53, True)  # ?
    , 96: (41, False)  # `
    , 126: (41, True)  # ~
}

key_to_str={
    0:"KEY_RESERVED"
    ,1:"KEY_ESC"
    ,2:"KEY_1"
    ,3:"KEY_2"
    ,4:"KEY_3"
    ,5:"KEY_4"
    ,6:"KEY_5"
    ,7:"KEY_6"
    ,8:"KEY_7"
    ,9:"KEY_8"
    ,10:"KEY_9"
    ,11:"KEY_0"
    ,12:"KEY_MINUS"
    ,13:"KEY_EQUAL"
    ,14:"KEY_BACKSPACE"
    ,15:"KEY_TAB"
    ,16:"KEY_Q"
    ,17:"KEY_W"
    ,18:"KEY_E"
    ,19:"KEY_R"
    ,20:"KEY_T"
    ,21:"KEY_Y"
    ,22:"KEY_U"
    ,23:"KEY_I"
    ,24:"KEY_O"
    ,25:"KEY_P"
    ,26:"KEY_LEFTBRACE"
    ,27:"KEY_RIGHTBRACE"
    ,28:"KEY_ENTER"
    ,29:"KEY_LEFTCTRL"
    ,30:"KEY_A"
    ,31:"KEY_S"
    ,32:"KEY_D"
    ,33:"KEY_F"
    ,34:"KEY_G"
    ,35:"KEY_H"
    ,36:"KEY_J"
    ,37:"KEY_K"
    ,38:"KEY_L"
    ,39:"KEY_SEMICOLON"
    ,40:"KEY_APOSTROPHE"
    ,41:"KEY_GRAVE"
    ,42:"KEY_LEFTSHIFT"
    ,43:"KEY_BACKSLASH"
    ,44:"KEY_Z"
    ,45:"KEY_X"
    ,46:"KEY_C"
    ,47:"KEY_V"
    ,48:"KEY_B"
    ,49:"KEY_N"
    ,50:"KEY_M"
    ,51:"KEY_COMMA"
    ,52:"KEY_DOT"
    ,53:"KEY_SLASH"
    ,54:"KEY_RIGHTSHIFT"
    ,55:"KEY_KPASTERISK"
    ,56:"KEY_LEFTALT"
    ,57:"KEY_SPACE"
    ,58:"KEY_CAPSLOCK"
    ,59:"KEY_F1"
    ,60:"KEY_F2"
    ,61:"KEY_F3"
    ,62:"KEY_F4"
    ,63:"KEY_F5"
    ,64:"KEY_F6"
    ,65:"KEY_F7"
    ,66:"KEY_F8"
    ,67:"KEY_F9"
    ,68:"KEY_F10"
    ,69:"KEY_NUMLOCK"
    ,70:"KEY_SCROLLLOCK"
    ,71:"KEY_KP7"
    ,72:"KEY_KP8"
    ,73:"KEY_KP9"
    ,74:"KEY_KPMINUS"
    ,75:"KEY_KP4"
    ,76:"KEY_KP5"
    ,77:"KEY_KP6"
    ,78:"KEY_KPPLUS"
    ,79:"KEY_KP1"
    ,80:"KEY_KP2"
    ,81:"KEY_KP3"
    ,82:"KEY_KP0"
    ,83:"KEY_KPDOT"
    ,85:"KEY_ZENKAKUHANKAKU"
    ,86:"KEY_102ND"
    ,87:"KEY_F11"
    ,88:"KEY_F12"
    ,89:"KEY_RO"
    ,90:"KEY_KATAKANA"
    ,91:"KEY_HIRAGANA"
    ,92:"KEY_HENKAN"
    ,93:"KEY_KATAKANAHIRAGANA"
    ,94:"KEY_MUHENKAN"
    ,95:"KEY_KPJPCOMMA"
    ,96:"KEY_KPENTER"
    ,97:"KEY_RIGHTCTRL"
    ,98:"KEY_KPSLASH"
    ,99:"KEY_SYSRQ"
    ,100:"KEY_RIGHTALT"
    ,101:"KEY_LINEFEED"
    ,102:"KEY_HOME"
    ,103:"KEY_UP"
    ,104:"KEY_PAGEUP"
    ,105:"KEY_LEFT"
    ,106:"KEY_RIGHT"
    ,107:"KEY_END"
    ,108:"KEY_DOWN"
    ,109:"KEY_PAGEDOWN"
    ,110:"KEY_INSERT"
    ,111:"KEY_DELETE"
    ,112:"KEY_MACRO"
    ,113:"KEY_MUTE"
    ,114:"KEY_VOLUMEDOWN"
    ,115:"KEY_VOLUMEUP"
    ,116:"KEY_POWER"
    ,117:"KEY_KPEQUAL"
    ,118:"KEY_KPPLUSMINUS"
    ,119:"KEY_PAUSE"
    ,120:"KEY_SCALE"
    ,121:"KEY_KPCOMMA"
    ,122:"KEY_HANGEUL"
    ,123:"KEY_HANJA"
    ,124:"KEY_YEN"
    ,125:"KEY_LEFTMETA"
    ,126:"KEY_RIGHTMETA"
    ,127:"KEY_COMPOSE"
    ,128:"KEY_STOP"
    ,129:"KEY_AGAIN"
    ,130:"KEY_PROPS"
    ,131:"KEY_UNDO"
    ,132:"KEY_FRONT"
    ,133:"KEY_COPY"
    ,134:"KEY_OPEN"
    ,135:"KEY_PASTE"
    ,136:"KEY_FIND"
    ,137:"KEY_CUT"
    ,138:"KEY_HELP"
    ,139:"KEY_MENU"
    ,140:"KEY_CALC"
    ,141:"KEY_SETUP"
    ,142:"KEY_SLEEP"
    ,143:"KEY_WAKEUP"
    ,144:"KEY_FILE"
    ,145:"KEY_SENDFILE"
    ,146:"KEY_DELETEFILE"
    ,147:"KEY_XFER"
    ,148:"KEY_PROG1"
    ,149:"KEY_PROG2"
    ,150:"KEY_WWW"
    ,151:"KEY_MSDOS"
    ,152:"KEY_COFFEE"
    ,153:"KEY_ROTATE_DISPLAY"
    ,154:"KEY_CYCLEWINDOWS"
    ,155:"KEY_MAIL"
    ,156:"KEY_BOOKMARKS"
    ,157:"KEY_COMPUTER"
    ,158:"KEY_BACK"
    ,159:"KEY_FORWARD"
    ,160:"KEY_CLOSECD"
    ,161:"KEY_EJECTCD"
    ,162:"KEY_EJECTCLOSECD"
    ,163:"KEY_NEXTSONG"
    ,164:"KEY_PLAYPAUSE"
    ,165:"KEY_PREVIOUSSONG"
    ,166:"KEY_STOPCD"
    ,167:"KEY_RECORD"
    ,168:"KEY_REWIND"
    ,169:"KEY_PHONE"
    ,170:"KEY_ISO"
    ,171:"KEY_CONFIG"
    ,172:"KEY_HOMEPAGE"
    ,173:"KEY_REFRESH"
    ,174:"KEY_EXIT"
    ,175:"KEY_MOVE"
    ,176:"KEY_EDIT"
    ,177:"KEY_SCROLLUP"
    ,178:"KEY_SCROLLDOWN"
    ,179:"KEY_KPLEFTPAREN"
    ,180:"KEY_KPRIGHTPAREN"
    ,181:"KEY_NEW"
    ,182:"KEY_REDO"
    ,183:"KEY_F13"
    ,184:"KEY_F14"
    ,185:"KEY_F15"
    ,186:"KEY_F16"
    ,187:"KEY_F17"
    ,188:"KEY_F18"
    ,189:"KEY_F19"
    ,190:"KEY_F20"
    ,191:"KEY_F21"
    ,192:"KEY_F22"
    ,193:"KEY_F23"
    ,194:"KEY_F24"
    ,200:"KEY_PLAYCD"
    ,201:"KEY_PAUSECD"
    ,202:"KEY_PROG3"
    ,203:"KEY_PROG4"
    ,204:"KEY_ALL_APPLICATIONS"
    ,205:"KEY_SUSPEND"
    ,206:"KEY_CLOSE"
    ,207:"KEY_PLAY"
    ,208:"KEY_FASTFORWARD"
    ,209:"KEY_BASSBOOST"
    ,210:"KEY_PRINT"
    ,211:"KEY_HP"
    ,212:"KEY_CAMERA"
    ,213:"KEY_SOUND"
    ,214:"KEY_QUESTION"
    ,215:"KEY_EMAIL"
    ,216:"KEY_CHAT"
    ,217:"KEY_SEARCH"
    ,218:"KEY_CONNECT"
    ,219:"KEY_FINANCE"
    ,220:"KEY_SPORT"
    ,221:"KEY_SHOP"
    ,222:"KEY_ALTERASE"
    ,223:"KEY_CANCEL"
    ,224:"KEY_BRIGHTNESSDOWN"
    ,225:"KEY_BRIGHTNESSUP"
    ,226:"KEY_MEDIA"
    ,227:"KEY_SWITCHVIDEOMODE"
    ,228:"KEY_KBDILLUMTOGGLE"
    ,229:"KEY_KBDILLUMDOWN"
    ,230:"KEY_KBDILLUMUP"
    ,231:"KEY_SEND"
    ,232:"KEY_REPLY"
    ,233:"KEY_FORWARDMAIL"
    ,234:"KEY_SAVE"
    ,235:"KEY_DOCUMENTS"
    ,236:"KEY_BATTERY"
    ,237:"KEY_BLUETOOTH"
    ,238:"KEY_WLAN"
    ,239:"KEY_UWB"
    ,240:"KEY_UNKNOWN"
    ,241:"KEY_VIDEO_NEXT"
    ,242:"KEY_VIDEO_PREV"
    ,243:"KEY_BRIGHTNESS_CYCLE"
    ,244:"KEY_BRIGHTNESS_AUTO"
    ,245:"KEY_DISPLAY_OFF"
    ,246:"KEY_WWAN"
    ,247:"KEY_RFKILL"
    ,248:"KEY_MICMUTE"
    ,0x160:"KEY_OK"
    ,0x161:"KEY_SELECT"
    ,0x162:"KEY_GOTO"
    ,0x163:"KEY_CLEAR"
    ,0x164:"KEY_POWER2"
    ,0x165:"KEY_OPTION"
    ,0x166:"KEY_INFO"
    ,0x167:"KEY_TIME"
    ,0x168:"KEY_VENDOR"
    ,0x169:"KEY_ARCHIVE"
    ,0x16a:"KEY_PROGRAM"
    ,0x16b:"KEY_CHANNEL"
    ,0x16c:"KEY_FAVORITES"
    ,0x16d:"KEY_EPG"
    ,0x16e:"KEY_PVR"
    ,0x16f:"KEY_MHP"
    ,0x170:"KEY_LANGUAGE"
    ,0x171:"KEY_TITLE"
    ,0x172:"KEY_SUBTITLE"
    ,0x173:"KEY_ANGLE"
    ,0x174:"KEY_FULL_SCREEN"
    ,0x175:"KEY_MODE"
    ,0x176:"KEY_KEYBOARD"
    ,0x177:"KEY_ASPECT_RATIO"
    ,0x178:"KEY_PC"
    ,0x179:"KEY_TV"
    ,0x17a:"KEY_TV2"
    ,0x17b:"KEY_VCR"
    ,0x17c:"KEY_VCR2"
    ,0x17d:"KEY_SAT"
    ,0x17e:"KEY_SAT2"
    ,0x17f:"KEY_CD"
    ,0x180:"KEY_TAPE"
    ,0x181:"KEY_RADIO"
    ,0x182:"KEY_TUNER"
    ,0x183:"KEY_PLAYER"
    ,0x184:"KEY_TEXT"
    ,0x185:"KEY_DVD"
    ,0x186:"KEY_AUX"
    ,0x187:"KEY_MP3"
    ,0x188:"KEY_AUDIO"
    ,0x189:"KEY_VIDEO"
    ,0x18a:"KEY_DIRECTORY"
    ,0x18b:"KEY_LIST"
    ,0x18c:"KEY_MEMO"
    ,0x18d:"KEY_CALENDAR"
    ,0x18e:"KEY_RED"
    ,0x18f:"KEY_GREEN"
    ,0x190:"KEY_YELLOW"
    ,0x191:"KEY_BLUE"
    ,0x192:"KEY_CHANNELUP"
    ,0x193:"KEY_CHANNELDOWN"
    ,0x194:"KEY_FIRST"
    ,0x195:"KEY_LAST"
    ,0x196:"KEY_AB"
    ,0x197:"KEY_NEXT"
    ,0x198:"KEY_RESTART"
    ,0x199:"KEY_SLOW"
    ,0x19a:"KEY_SHUFFLE"
    ,0x19b:"KEY_BREAK"
    ,0x19c:"KEY_PREVIOUS"
    ,0x19d:"KEY_DIGITS"
    ,0x19e:"KEY_TEEN"
    ,0x19f:"KEY_TWEN"
    ,0x1a0:"KEY_VIDEOPHONE"
    ,0x1a1:"KEY_GAMES"
    ,0x1a2:"KEY_ZOOMIN"
    ,0x1a3:"KEY_ZOOMOUT"
    ,0x1a4:"KEY_ZOOMRESET"
    ,0x1a5:"KEY_WORDPROCESSOR"
    ,0x1a6:"KEY_EDITOR"
    ,0x1a7:"KEY_SPREADSHEET"
    ,0x1a8:"KEY_GRAPHICSEDITOR"
    ,0x1a9:"KEY_PRESENTATION"
    ,0x1aa:"KEY_DATABASE"
    ,0x1ab:"KEY_NEWS"
    ,0x1ac:"KEY_VOICEMAIL"
    ,0x1ad:"KEY_ADDRESSBOOK"
    ,0x1ae:"KEY_MESSENGER"
    ,0x1af:"KEY_DISPLAYTOGGLE"
    ,0x1b0:"KEY_SPELLCHECK"
    ,0x1b1:"KEY_LOGOFF"
    ,0x1b2:"KEY_DOLLAR"
    ,0x1b3:"KEY_EURO"
    ,0x1b4:"KEY_FRAMEBACK"
    ,0x1b5:"KEY_FRAMEFORWARD"
    ,0x1b6:"KEY_CONTEXT_MENU"
    ,0x1b7:"KEY_MEDIA_REPEAT"
    ,0x1b8:"KEY_10CHANNELSUP"
    ,0x1b9:"KEY_10CHANNELSDOWN"
    ,0x1ba:"KEY_IMAGES"
    ,0x1bc:"KEY_NOTIFICATION_CENTER"
    ,0x1bd:"KEY_PICKUP_PHONE"
    ,0x1be:"KEY_HANGUP_PHONE"
    ,0x1bf:"KEY_LINK_PHONE"
    ,0x1c0:"KEY_DEL_EOL"
    ,0x1c1:"KEY_DEL_EOS"
    ,0x1c2:"KEY_INS_LINE"
    ,0x1c3:"KEY_DEL_LINE"
    ,0x1d0:"KEY_FN"
    ,0x1d1:"KEY_FN_ESC"
    ,0x1d2:"KEY_FN_F1"
    ,0x1d3:"KEY_FN_F2"
    ,0x1d4:"KEY_FN_F3"
    ,0x1d5:"KEY_FN_F4"
    ,0x1d6:"KEY_FN_F5"
    ,0x1d7:"KEY_FN_F6"
    ,0x1d8:"KEY_FN_F7"
    ,0x1d9:"KEY_FN_F8"
    ,0x1da:"KEY_FN_F9"
    ,0x1db:"KEY_FN_F10"
    ,0x1dc:"KEY_FN_F11"
    ,0x1dd:"KEY_FN_F12"
    ,0x1de:"KEY_FN_1"
    ,0x1df:"KEY_FN_2"
    ,0x1e0:"KEY_FN_D"
    ,0x1e1:"KEY_FN_E"
    ,0x1e2:"KEY_FN_F"
    ,0x1e3:"KEY_FN_S"
    ,0x1e4:"KEY_FN_B"
    ,0x1e5:"KEY_FN_RIGHT_SHIFT"
    ,0x1f1:"KEY_BRL_DOT1"
    ,0x1f2:"KEY_BRL_DOT2"
    ,0x1f3:"KEY_BRL_DOT3"
    ,0x1f4:"KEY_BRL_DOT4"
    ,0x1f5:"KEY_BRL_DOT5"
    ,0x1f6:"KEY_BRL_DOT6"
    ,0x1f7:"KEY_BRL_DOT7"
    ,0x1f8:"KEY_BRL_DOT8"
    ,0x1f9:"KEY_BRL_DOT9"
    ,0x1fa:"KEY_BRL_DOT10"
    ,0x200:"KEY_NUMERIC_0"
    ,0x201:"KEY_NUMERIC_1"
    ,0x202:"KEY_NUMERIC_2"
    ,0x203:"KEY_NUMERIC_3"
    ,0x204:"KEY_NUMERIC_4"
    ,0x205:"KEY_NUMERIC_5"
    ,0x206:"KEY_NUMERIC_6"
    ,0x207:"KEY_NUMERIC_7"
    ,0x208:"KEY_NUMERIC_8"
    ,0x209:"KEY_NUMERIC_9"
    ,0x20a:"KEY_NUMERIC_STAR"
    ,0x20b:"KEY_NUMERIC_POUND"
    ,0x20c:"KEY_NUMERIC_A"
    ,0x20d:"KEY_NUMERIC_B"
    ,0x20e:"KEY_NUMERIC_C"
    ,0x20f:"KEY_NUMERIC_D"
    ,0x210:"KEY_CAMERA_FOCUS"
    ,0x211:"KEY_WPS_BUTTON"
    ,0x212:"KEY_TOUCHPAD_TOGGLE"
    ,0x213:"KEY_TOUCHPAD_ON"
    ,0x214:"KEY_TOUCHPAD_OFF"
    ,0x215:"KEY_CAMERA_ZOOMIN"
    ,0x216:"KEY_CAMERA_ZOOMOUT"
    ,0x217:"KEY_CAMERA_UP"
    ,0x218:"KEY_CAMERA_DOWN"
    ,0x219:"KEY_CAMERA_LEFT"
    ,0x21a:"KEY_CAMERA_RIGHT"
    ,0x21b:"KEY_ATTENDANT_ON"
    ,0x21c:"KEY_ATTENDANT_OFF"
    ,0x21d:"KEY_ATTENDANT_TOGGLE"
    ,0x21e:"KEY_LIGHTS_TOGGLE"
    ,0x230:"KEY_ALS_TOGGLE"
    ,0x231:"KEY_ROTATE_LOCK_TOGGLE"
    ,0x232:"KEY_REFRESH_RATE_TOGGLE"
    ,0x240:"KEY_BUTTONCONFIG"
    ,0x241:"KEY_TASKMANAGER"
    ,0x242:"KEY_JOURNAL"
    ,0x243:"KEY_CONTROLPANEL"
    ,0x244:"KEY_APPSELECT"
    ,0x245:"KEY_SCREENSAVER"
    ,0x246:"KEY_VOICECOMMAND"
    ,0x247:"KEY_ASSISTANT"
    ,0x248:"KEY_KBD_LAYOUT_NEXT"
    ,0x249:"KEY_EMOJI_PICKER"
    ,0x24a:"KEY_DICTATE"
    ,0x24b:"KEY_CAMERA_ACCESS_ENABLE"
    ,0x24c:"KEY_CAMERA_ACCESS_DISABLE"
    ,0x24d:"KEY_CAMERA_ACCESS_TOGGLE"
    ,0x24e:"KEY_ACCESSIBILITY"
    ,0x24f:"KEY_DO_NOT_DISTURB"
    ,0x250:"KEY_BRIGHTNESS_MIN"
    ,0x251:"KEY_BRIGHTNESS_MAX"
    ,0x260:"KEY_KBDINPUTASSIST_PREV"
    ,0x261:"KEY_KBDINPUTASSIST_NEXT"
    ,0x262:"KEY_KBDINPUTASSIST_PREVGROUP"
    ,0x263:"KEY_KBDINPUTASSIST_NEXTGROUP"
    ,0x264:"KEY_KBDINPUTASSIST_ACCEPT"
    ,0x265:"KEY_KBDINPUTASSIST_CANCEL"
    ,0x266:"KEY_RIGHT_UP"
    ,0x267:"KEY_RIGHT_DOWN"
    ,0x268:"KEY_LEFT_UP"
    ,0x269:"KEY_LEFT_DOWN"
    ,0x26a:"KEY_ROOT_MENU"
    ,0x26b:"KEY_MEDIA_TOP_MENU"
    ,0x26c:"KEY_NUMERIC_11"
    ,0x26d:"KEY_NUMERIC_12"
    ,0x26e:"KEY_AUDIO_DESC"
    ,0x26f:"KEY_3D_MODE"
    ,0x270:"KEY_NEXT_FAVORITE"
    ,0x271:"KEY_STOP_RECORD"
    ,0x272:"KEY_PAUSE_RECORD"
    ,0x273:"KEY_VOD"
    ,0x274:"KEY_UNMUTE"
    ,0x275:"KEY_FASTREVERSE"
    ,0x276:"KEY_SLOWREVERSE"
    ,0x277:"KEY_DATA"
    ,0x278:"KEY_ONSCREEN_KEYBOARD"
    ,0x279:"KEY_PRIVACY_SCREEN_TOGGLE"
    ,0x27a:"KEY_SELECTIVE_SCREENSHOT"
    ,0x27b:"KEY_NEXT_ELEMENT"
    ,0x27c:"KEY_PREVIOUS_ELEMENT"
    ,0x27d:"KEY_AUTOPILOT_ENGAGE_TOGGLE"
    ,0x27e:"KEY_MARK_WAYPOINT"
    ,0x27f:"KEY_SOS"
    ,0x280:"KEY_NAV_CHART"
    ,0x281:"KEY_FISHING_CHART"
    ,0x282:"KEY_SINGLE_RANGE_RADAR"
    ,0x283:"KEY_DUAL_RANGE_RADAR"
    ,0x284:"KEY_RADAR_OVERLAY"
    ,0x285:"KEY_TRADITIONAL_SONAR"
    ,0x286:"KEY_CLEARVU_SONAR"
    ,0x287:"KEY_SIDEVU_SONAR"
    ,0x288:"KEY_NAV_INFO"
    ,0x289:"KEY_BRIGHTNESS_MENU"
    ,0x290:"KEY_MACRO1"
    ,0x291:"KEY_MACRO2"
    ,0x292:"KEY_MACRO3"
    ,0x293:"KEY_MACRO4"
    ,0x294:"KEY_MACRO5"
    ,0x295:"KEY_MACRO6"
    ,0x296:"KEY_MACRO7"
    ,0x297:"KEY_MACRO8"
    ,0x298:"KEY_MACRO9"
    ,0x299:"KEY_MACRO10"
    ,0x29a:"KEY_MACRO11"
    ,0x29b:"KEY_MACRO12"
    ,0x29c:"KEY_MACRO13"
    ,0x29d:"KEY_MACRO14"
    ,0x29e:"KEY_MACRO15"
    ,0x29f:"KEY_MACRO16"
    ,0x2a0:"KEY_MACRO17"
    ,0x2a1:"KEY_MACRO18"
    ,0x2a2:"KEY_MACRO19"
    ,0x2a3:"KEY_MACRO20"
    ,0x2a4:"KEY_MACRO21"
    ,0x2a5:"KEY_MACRO22"
    ,0x2a6:"KEY_MACRO23"
    ,0x2a7:"KEY_MACRO24"
    ,0x2a8:"KEY_MACRO25"
    ,0x2a9:"KEY_MACRO26"
    ,0x2aa:"KEY_MACRO27"
    ,0x2ab:"KEY_MACRO28"
    ,0x2ac:"KEY_MACRO29"
    ,0x2ad:"KEY_MACRO30"
    ,0x2b0:"KEY_MACRO_RECORD_START"
    ,0x2b1:"KEY_MACRO_RECORD_STOP"
    ,0x2b2:"KEY_MACRO_PRESET_CYCLE"
    ,0x2b3:"KEY_MACRO_PRESET1"
    ,0x2b4:"KEY_MACRO_PRESET2"
    ,0x2b5:"KEY_MACRO_PRESET3"
    ,0x2b8:"KEY_KBD_LCD_MENU1"
    ,0x2b9:"KEY_KBD_LCD_MENU2"
    ,0x2ba:"KEY_KBD_LCD_MENU3"
    ,0x2bb:"KEY_KBD_LCD_MENU4"
    ,0x2bc:"KEY_KBD_LCD_MENU5"
    ,0x2ff:"KEY_MAX"
}
btn_to_str = {
    #0x100: "BTN_MISC"
      0x100: "BTN_0"
    , 0x101: "BTN_1"
    , 0x102: "BTN_2"
    , 0x103: "BTN_3"
    , 0x104: "BTN_4"
    , 0x105: "BTN_5"
    , 0x106: "BTN_6"
    , 0x107: "BTN_7"
    , 0x108: "BTN_8"
    , 0x109: "BTN_9"
    #, 0x110: "BTN_MOUSE"
    , 0x110: "BTN_LEFT"
    , 0x111: "BTN_RIGHT"
    , 0x112: "BTN_MIDDLE"
    , 0x113: "BTN_SIDE"
    , 0x114: "BTN_EXTRA"
    , 0x115: "BTN_FORWARD"
    , 0x116: "BTN_BACK"
    , 0x117: "BTN_TASK"
    #, 0x120: "BTN_JOYSTICK"
    , 0x120: "BTN_TRIGGER"
    , 0x121: "BTN_THUMB"
    , 0x122: "BTN_THUMB2"
    , 0x123: "BTN_TOP"
    , 0x124: "BTN_TOP2"
    , 0x125: "BTN_PINKIE"
    , 0x126: "BTN_BASE"
    , 0x127: "BTN_BASE2"
    , 0x128: "BTN_BASE3"
    , 0x129: "BTN_BASE4"
    , 0x12a: "BTN_BASE5"
    , 0x12b: "BTN_BASE6"
    , 0x12f: "BTN_DEAD"
    #, 0x130: "BTN_GAMEPAD"
    , 0x130: "BTN_SOUTH"
    , 0x131: "BTN_EAST"
    , 0x132: "BTN_C"
    , 0x133: "BTN_NORTH"
    , 0x134: "BTN_WEST"
    , 0x135: "BTN_Z"
    , 0x136: "BTN_TL"
    , 0x137: "BTN_TR"
    , 0x138: "BTN_TL2"
    , 0x139: "BTN_TR2"
    , 0x13a: "BTN_SELECT"
    , 0x13b: "BTN_START"
    , 0x13c: "BTN_MODE"
    , 0x13d: "BTN_THUMBL"
    , 0x13e: "BTN_THUMBR"
    #, 0x140: "BTN_DIGI"
    , 0x140: "BTN_TOOL_PEN"
    , 0x141: "BTN_TOOL_RUBBER"
    , 0x142: "BTN_TOOL_BRUSH"
    , 0x143: "BTN_TOOL_PENCIL"
    , 0x144: "BTN_TOOL_AIRBRUSH"
    , 0x145: "BTN_TOOL_FINGER"
    , 0x146: "BTN_TOOL_MOUSE"
    , 0x147: "BTN_TOOL_LENS"
    , 0x148: "BTN_TOOL_QUINTTAP"
    , 0x149: "BTN_STYLUS3"
    , 0x14a: "BTN_TOUCH"
    , 0x14b: "BTN_STYLUS"
    , 0x14c: "BTN_STYLUS2"
    , 0x14d: "BTN_TOOL_DOUBLETAP"
    , 0x14e: "BTN_TOOL_TRIPLETAP"
    , 0x14f: "BTN_TOOL_QUADTAP"
    #, 0x150: "BTN_WHEEL"
    , 0x150: "BTN_GEAR_DOWN"
    , 0x151: "BTN_GEAR_UP"
    , 0x220: "BTN_DPAD_UP"
    , 0x221: "BTN_DPAD_DOWN"
    , 0x222: "BTN_DPAD_LEFT"
    , 0x223: "BTN_DPAD_RIGHT"
    #, 0x2c0: "BTN_TRIGGER_HAPPY"
    , 0x2c0: "BTN_TRIGGER_HAPPY1"
    , 0x2c1: "BTN_TRIGGER_HAPPY2"
    , 0x2c2: "BTN_TRIGGER_HAPPY3"
    , 0x2c3: "BTN_TRIGGER_HAPPY4"
    , 0x2c4: "BTN_TRIGGER_HAPPY5"
    , 0x2c5: "BTN_TRIGGER_HAPPY6"
    , 0x2c6: "BTN_TRIGGER_HAPPY7"
    , 0x2c7: "BTN_TRIGGER_HAPPY8"
    , 0x2c8: "BTN_TRIGGER_HAPPY9"
    , 0x2c9: "BTN_TRIGGER_HAPPY10"
    , 0x2ca: "BTN_TRIGGER_HAPPY11"
    , 0x2cb: "BTN_TRIGGER_HAPPY12"
    , 0x2cc: "BTN_TRIGGER_HAPPY13"
    , 0x2cd: "BTN_TRIGGER_HAPPY14"
    , 0x2ce: "BTN_TRIGGER_HAPPY15"
    , 0x2cf: "BTN_TRIGGER_HAPPY16"
    , 0x2d0: "BTN_TRIGGER_HAPPY17"
    , 0x2d1: "BTN_TRIGGER_HAPPY18"
    , 0x2d2: "BTN_TRIGGER_HAPPY19"
    , 0x2d3: "BTN_TRIGGER_HAPPY20"
    , 0x2d4: "BTN_TRIGGER_HAPPY21"
    , 0x2d5: "BTN_TRIGGER_HAPPY22"
    , 0x2d6: "BTN_TRIGGER_HAPPY23"
    , 0x2d7: "BTN_TRIGGER_HAPPY24"
    , 0x2d8: "BTN_TRIGGER_HAPPY25"
    , 0x2d9: "BTN_TRIGGER_HAPPY26"
    , 0x2da: "BTN_TRIGGER_HAPPY27"
    , 0x2db: "BTN_TRIGGER_HAPPY28"
    , 0x2dc: "BTN_TRIGGER_HAPPY29"
    , 0x2dd: "BTN_TRIGGER_HAPPY30"
    , 0x2de: "BTN_TRIGGER_HAPPY31"
    , 0x2df: "BTN_TRIGGER_HAPPY32"
    , 0x2e0: "BTN_TRIGGER_HAPPY33"
    , 0x2e1: "BTN_TRIGGER_HAPPY34"
    , 0x2e2: "BTN_TRIGGER_HAPPY35"
    , 0x2e3: "BTN_TRIGGER_HAPPY36"
    , 0x2e4: "BTN_TRIGGER_HAPPY37"
    , 0x2e5: "BTN_TRIGGER_HAPPY38"
    , 0x2e6: "BTN_TRIGGER_HAPPY39"
    , 0x2e7: "BTN_TRIGGER_HAPPY40"
}

ev_type_no_to_str   ={
     0x00:"EV_SYN"
    ,0x01:"EV_KEY"
    ,0x02:"EV_REL"
    ,0x03:"EV_ABS"
    ,0x04:"EV_MSC"
    ,0x05:"EV_SW"
    ,0x11:"EV_LED"
    ,0x12:"EV_SND"
    ,0x14:"EV_REP"
    ,0x15:"EV_FF"
    ,0x16:"EV_PWR"
    ,0x17:"EV_FF_STATUS"
    ,0x1f:"EV_MAX"
    #(EV_MAX+1):"EV_CNT"
}
ev_syn_no_to_str    ={
     0:"SYN_REPORT"
    ,1:"SYN_CONFIG"
    ,2:"SYN_MT_REPORT"
    ,3:"SYN_DROPPED"
    ,0xf:"SYN_MAX"
    #(SYN_MAX+1):"SYN_CNT"
}

ev_key_no_to_str    = {
    0: "KEY_RESERVED"
    , 1: "KEY_ESC"
    , 2: "KEY_1"
    , 3: "KEY_2"
    , 4: "KEY_3"
    , 5: "KEY_4"
    , 6: "KEY_5"
    , 7: "KEY_6"
    , 8: "KEY_7"
    , 9: "KEY_8"
    , 10: "KEY_9"
    , 11: "KEY_0"
    , 12: "KEY_MINUS"
    , 13: "KEY_EQUAL"
    , 14: "KEY_BACKSPACE"
    , 15: "KEY_TAB"
    , 16: "KEY_Q"
    , 17: "KEY_W"
    , 18: "KEY_E"
    , 19: "KEY_R"
    , 20: "KEY_T"
    , 21: "KEY_Y"
    , 22: "KEY_U"
    , 23: "KEY_I"
    , 24: "KEY_O"
    , 25: "KEY_P"
    , 26: "KEY_LEFTBRACE"
    , 27: "KEY_RIGHTBRACE"
    , 28: "KEY_ENTER"
    , 29: "KEY_LEFTCTRL"
    , 30: "KEY_A"
    , 31: "KEY_S"
    , 32: "KEY_D"
    , 33: "KEY_F"
    , 34: "KEY_G"
    , 35: "KEY_H"
    , 36: "KEY_J"
    , 37: "KEY_K"
    , 38: "KEY_L"
    , 39: "KEY_SEMICOLON"
    , 40: "KEY_APOSTROPHE"
    , 41: "KEY_GRAVE"
    , 42: "KEY_LEFTSHIFT"
    , 43: "KEY_BACKSLASH"
    , 44: "KEY_Z"
    , 45: "KEY_X"
    , 46: "KEY_C"
    , 47: "KEY_V"
    , 48: "KEY_B"
    , 49: "KEY_N"
    , 50: "KEY_M"
    , 51: "KEY_COMMA"
    , 52: "KEY_DOT"
    , 53: "KEY_SLASH"
    , 54: "KEY_RIGHTSHIFT"
    , 55: "KEY_KPASTERISK"
    , 56: "KEY_LEFTALT"
    , 57: "KEY_SPACE"
    , 58: "KEY_CAPSLOCK"
    , 59: "KEY_F1"
    , 60: "KEY_F2"
    , 61: "KEY_F3"
    , 62: "KEY_F4"
    , 63: "KEY_F5"
    , 64: "KEY_F6"
    , 65: "KEY_F7"
    , 66: "KEY_F8"
    , 67: "KEY_F9"
    , 68: "KEY_F10"
    , 69: "KEY_NUMLOCK"
    , 70: "KEY_SCROLLLOCK"
    , 71: "KEY_KP7"
    , 72: "KEY_KP8"
    , 73: "KEY_KP9"
    , 74: "KEY_KPMINUS"
    , 75: "KEY_KP4"
    , 76: "KEY_KP5"
    , 77: "KEY_KP6"
    , 78: "KEY_KPPLUS"
    , 79: "KEY_KP1"
    , 80: "KEY_KP2"
    , 81: "KEY_KP3"
    , 82: "KEY_KP0"
    , 83: "KEY_KPDOT"
    , 85: "KEY_ZENKAKUHANKAKU"
    , 86: "KEY_102ND"
    , 87: "KEY_F11"
    , 88: "KEY_F12"
    , 89: "KEY_RO"
    , 90: "KEY_KATAKANA"
    , 91: "KEY_HIRAGANA"
    , 92: "KEY_HENKAN"
    , 93: "KEY_KATAKANAHIRAGANA"
    , 94: "KEY_MUHENKAN"
    , 95: "KEY_KPJPCOMMA"
    , 96: "KEY_KPENTER"
    , 97: "KEY_RIGHTCTRL"
    , 98: "KEY_KPSLASH"
    , 99: "KEY_SYSRQ"
    , 100: "KEY_RIGHTALT"
    , 101: "KEY_LINEFEED"
    , 102: "KEY_HOME"
    , 103: "KEY_UP"
    , 104: "KEY_PAGEUP"
    , 105: "KEY_LEFT"
    , 106: "KEY_RIGHT"
    , 107: "KEY_END"
    , 108: "KEY_DOWN"
    , 109: "KEY_PAGEDOWN"
    , 110: "KEY_INSERT"
    , 111: "KEY_DELETE"
    , 112: "KEY_MACRO"
    , 113: "KEY_MUTE"
    , 114: "KEY_VOLUMEDOWN"
    , 115: "KEY_VOLUMEUP"
    , 116: "KEY_POWER"
    , 117: "KEY_KPEQUAL"
    , 118: "KEY_KPPLUSMINUS"
    , 119: "KEY_PAUSE"
    , 120: "KEY_SCALE"
    , 121: "KEY_KPCOMMA"
    , 122: "KEY_HANGEUL"
    , 123: "KEY_HANJA"
    , 124: "KEY_YEN"
    , 125: "KEY_LEFTMETA"
    , 126: "KEY_RIGHTMETA"
    , 127: "KEY_COMPOSE"
    , 128: "KEY_STOP"
    , 129: "KEY_AGAIN"
    , 130: "KEY_PROPS"
    , 131: "KEY_UNDO"
    , 132: "KEY_FRONT"
    , 133: "KEY_COPY"
    , 134: "KEY_OPEN"
    , 135: "KEY_PASTE"
    , 136: "KEY_FIND"
    , 137: "KEY_CUT"
    , 138: "KEY_HELP"
    , 139: "KEY_MENU"
    , 140: "KEY_CALC"
    , 141: "KEY_SETUP"
    , 142: "KEY_SLEEP"
    , 143: "KEY_WAKEUP"
    , 144: "KEY_FILE"
    , 145: "KEY_SENDFILE"
    , 146: "KEY_DELETEFILE"
    , 147: "KEY_XFER"
    , 148: "KEY_PROG1"
    , 149: "KEY_PROG2"
    , 150: "KEY_WWW"
    , 151: "KEY_MSDOS"
    , 152: "KEY_COFFEE"
    , 153: "KEY_ROTATE_DISPLAY"
    , 154: "KEY_CYCLEWINDOWS"
    , 155: "KEY_MAIL"
    , 156: "KEY_BOOKMARKS"
    , 157: "KEY_COMPUTER"
    , 158: "KEY_BACK"
    , 159: "KEY_FORWARD"
    , 160: "KEY_CLOSECD"
    , 161: "KEY_EJECTCD"
    , 162: "KEY_EJECTCLOSECD"
    , 163: "KEY_NEXTSONG"
    , 164: "KEY_PLAYPAUSE"
    , 165: "KEY_PREVIOUSSONG"
    , 166: "KEY_STOPCD"
    , 167: "KEY_RECORD"
    , 168: "KEY_REWIND"
    , 169: "KEY_PHONE"
    , 170: "KEY_ISO"
    , 171: "KEY_CONFIG"
    , 172: "KEY_HOMEPAGE"
    , 173: "KEY_REFRESH"
    , 174: "KEY_EXIT"
    , 175: "KEY_MOVE"
    , 176: "KEY_EDIT"
    , 177: "KEY_SCROLLUP"
    , 178: "KEY_SCROLLDOWN"
    , 179: "KEY_KPLEFTPAREN"
    , 180: "KEY_KPRIGHTPAREN"
    , 181: "KEY_NEW"
    , 182: "KEY_REDO"
    , 183: "KEY_F13"
    , 184: "KEY_F14"
    , 185: "KEY_F15"
    , 186: "KEY_F16"
    , 187: "KEY_F17"
    , 188: "KEY_F18"
    , 189: "KEY_F19"
    , 190: "KEY_F20"
    , 191: "KEY_F21"
    , 192: "KEY_F22"
    , 193: "KEY_F23"
    , 194: "KEY_F24"
    , 200: "KEY_PLAYCD"
    , 201: "KEY_PAUSECD"
    , 202: "KEY_PROG3"
    , 203: "KEY_PROG4"
    , 204: "KEY_ALL_APPLICATIONS"
    , 205: "KEY_SUSPEND"
    , 206: "KEY_CLOSE"
    , 207: "KEY_PLAY"
    , 208: "KEY_FASTFORWARD"
    , 209: "KEY_BASSBOOST"
    , 210: "KEY_PRINT"
    , 211: "KEY_HP"
    , 212: "KEY_CAMERA"
    , 213: "KEY_SOUND"
    , 214: "KEY_QUESTION"
    , 215: "KEY_EMAIL"
    , 216: "KEY_CHAT"
    , 217: "KEY_SEARCH"
    , 218: "KEY_CONNECT"
    , 219: "KEY_FINANCE"
    , 220: "KEY_SPORT"
    , 221: "KEY_SHOP"
    , 222: "KEY_ALTERASE"
    , 223: "KEY_CANCEL"
    , 224: "KEY_BRIGHTNESSDOWN"
    , 225: "KEY_BRIGHTNESSUP"
    , 226: "KEY_MEDIA"
    , 227: "KEY_SWITCHVIDEOMODE"
    , 228: "KEY_KBDILLUMTOGGLE"
    , 229: "KEY_KBDILLUMDOWN"
    , 230: "KEY_KBDILLUMUP"
    , 231: "KEY_SEND"
    , 232: "KEY_REPLY"
    , 233: "KEY_FORWARDMAIL"
    , 234: "KEY_SAVE"
    , 235: "KEY_DOCUMENTS"
    , 236: "KEY_BATTERY"
    , 237: "KEY_BLUETOOTH"
    , 238: "KEY_WLAN"
    , 239: "KEY_UWB"
    , 240: "KEY_UNKNOWN"
    , 241: "KEY_VIDEO_NEXT"
    , 242: "KEY_VIDEO_PREV"
    , 243: "KEY_BRIGHTNESS_CYCLE"
    , 244: "KEY_BRIGHTNESS_AUTO"
    , 245: "KEY_DISPLAY_OFF"
    , 246: "KEY_WWAN"
    , 247: "KEY_RFKILL"
    , 248: "KEY_MICMUTE"
    , 0x160: "KEY_OK"
    , 0x161: "KEY_SELECT"
    , 0x162: "KEY_GOTO"
    , 0x163: "KEY_CLEAR"
    , 0x164: "KEY_POWER2"
    , 0x165: "KEY_OPTION"
    , 0x166: "KEY_INFO"
    , 0x167: "KEY_TIME"
    , 0x168: "KEY_VENDOR"
    , 0x169: "KEY_ARCHIVE"
    , 0x16a: "KEY_PROGRAM"
    , 0x16b: "KEY_CHANNEL"
    , 0x16c: "KEY_FAVORITES"
    , 0x16d: "KEY_EPG"
    , 0x16e: "KEY_PVR"
    , 0x16f: "KEY_MHP"
    , 0x170: "KEY_LANGUAGE"
    , 0x171: "KEY_TITLE"
    , 0x172: "KEY_SUBTITLE"
    , 0x173: "KEY_ANGLE"
    , 0x174: "KEY_FULL_SCREEN"
    , 0x175: "KEY_MODE"
    , 0x176: "KEY_KEYBOARD"
    , 0x177: "KEY_ASPECT_RATIO"
    , 0x178: "KEY_PC"
    , 0x179: "KEY_TV"
    , 0x17a: "KEY_TV2"
    , 0x17b: "KEY_VCR"
    , 0x17c: "KEY_VCR2"
    , 0x17d: "KEY_SAT"
    , 0x17e: "KEY_SAT2"
    , 0x17f: "KEY_CD"
    , 0x180: "KEY_TAPE"
    , 0x181: "KEY_RADIO"
    , 0x182: "KEY_TUNER"
    , 0x183: "KEY_PLAYER"
    , 0x184: "KEY_TEXT"
    , 0x185: "KEY_DVD"
    , 0x186: "KEY_AUX"
    , 0x187: "KEY_MP3"
    , 0x188: "KEY_AUDIO"
    , 0x189: "KEY_VIDEO"
    , 0x18a: "KEY_DIRECTORY"
    , 0x18b: "KEY_LIST"
    , 0x18c: "KEY_MEMO"
    , 0x18d: "KEY_CALENDAR"
    , 0x18e: "KEY_RED"
    , 0x18f: "KEY_GREEN"
    , 0x190: "KEY_YELLOW"
    , 0x191: "KEY_BLUE"
    , 0x192: "KEY_CHANNELUP"
    , 0x193: "KEY_CHANNELDOWN"
    , 0x194: "KEY_FIRST"
    , 0x195: "KEY_LAST"
    , 0x196: "KEY_AB"
    , 0x197: "KEY_NEXT"
    , 0x198: "KEY_RESTART"
    , 0x199: "KEY_SLOW"
    , 0x19a: "KEY_SHUFFLE"
    , 0x19b: "KEY_BREAK"
    , 0x19c: "KEY_PREVIOUS"
    , 0x19d: "KEY_DIGITS"
    , 0x19e: "KEY_TEEN"
    , 0x19f: "KEY_TWEN"
    , 0x1a0: "KEY_VIDEOPHONE"
    , 0x1a1: "KEY_GAMES"
    , 0x1a2: "KEY_ZOOMIN"
    , 0x1a3: "KEY_ZOOMOUT"
    , 0x1a4: "KEY_ZOOMRESET"
    , 0x1a5: "KEY_WORDPROCESSOR"
    , 0x1a6: "KEY_EDITOR"
    , 0x1a7: "KEY_SPREADSHEET"
    , 0x1a8: "KEY_GRAPHICSEDITOR"
    , 0x1a9: "KEY_PRESENTATION"
    , 0x1aa: "KEY_DATABASE"
    , 0x1ab: "KEY_NEWS"
    , 0x1ac: "KEY_VOICEMAIL"
    , 0x1ad: "KEY_ADDRESSBOOK"
    , 0x1ae: "KEY_MESSENGER"
    , 0x1af: "KEY_DISPLAYTOGGLE"
    , 0x1b0: "KEY_SPELLCHECK"
    , 0x1b1: "KEY_LOGOFF"
    , 0x1b2: "KEY_DOLLAR"
    , 0x1b3: "KEY_EURO"
    , 0x1b4: "KEY_FRAMEBACK"
    , 0x1b5: "KEY_FRAMEFORWARD"
    , 0x1b6: "KEY_CONTEXT_MENU"
    , 0x1b7: "KEY_MEDIA_REPEAT"
    , 0x1b8: "KEY_10CHANNELSUP"
    , 0x1b9: "KEY_10CHANNELSDOWN"
    , 0x1ba: "KEY_IMAGES"
    , 0x1bc: "KEY_NOTIFICATION_CENTER"
    , 0x1bd: "KEY_PICKUP_PHONE"
    , 0x1be: "KEY_HANGUP_PHONE"
    , 0x1bf: "KEY_LINK_PHONE"
    , 0x1c0: "KEY_DEL_EOL"
    , 0x1c1: "KEY_DEL_EOS"
    , 0x1c2: "KEY_INS_LINE"
    , 0x1c3: "KEY_DEL_LINE"
    , 0x1d0: "KEY_FN"
    , 0x1d1: "KEY_FN_ESC"
    , 0x1d2: "KEY_FN_F1"
    , 0x1d3: "KEY_FN_F2"
    , 0x1d4: "KEY_FN_F3"
    , 0x1d5: "KEY_FN_F4"
    , 0x1d6: "KEY_FN_F5"
    , 0x1d7: "KEY_FN_F6"
    , 0x1d8: "KEY_FN_F7"
    , 0x1d9: "KEY_FN_F8"
    , 0x1da: "KEY_FN_F9"
    , 0x1db: "KEY_FN_F10"
    , 0x1dc: "KEY_FN_F11"
    , 0x1dd: "KEY_FN_F12"
    , 0x1de: "KEY_FN_1"
    , 0x1df: "KEY_FN_2"
    , 0x1e0: "KEY_FN_D"
    , 0x1e1: "KEY_FN_E"
    , 0x1e2: "KEY_FN_F"
    , 0x1e3: "KEY_FN_S"
    , 0x1e4: "KEY_FN_B"
    , 0x1e5: "KEY_FN_RIGHT_SHIFT"
    , 0x1f1: "KEY_BRL_DOT1"
    , 0x1f2: "KEY_BRL_DOT2"
    , 0x1f3: "KEY_BRL_DOT3"
    , 0x1f4: "KEY_BRL_DOT4"
    , 0x1f5: "KEY_BRL_DOT5"
    , 0x1f6: "KEY_BRL_DOT6"
    , 0x1f7: "KEY_BRL_DOT7"
    , 0x1f8: "KEY_BRL_DOT8"
    , 0x1f9: "KEY_BRL_DOT9"
    , 0x1fa: "KEY_BRL_DOT10"
    , 0x200: "KEY_NUMERIC_0"
    , 0x201: "KEY_NUMERIC_1"
    , 0x202: "KEY_NUMERIC_2"
    , 0x203: "KEY_NUMERIC_3"
    , 0x204: "KEY_NUMERIC_4"
    , 0x205: "KEY_NUMERIC_5"
    , 0x206: "KEY_NUMERIC_6"
    , 0x207: "KEY_NUMERIC_7"
    , 0x208: "KEY_NUMERIC_8"
    , 0x209: "KEY_NUMERIC_9"
    , 0x20a: "KEY_NUMERIC_STAR"
    , 0x20b: "KEY_NUMERIC_POUND"
    , 0x20c: "KEY_NUMERIC_A"
    , 0x20d: "KEY_NUMERIC_B"
    , 0x20e: "KEY_NUMERIC_C"
    , 0x20f: "KEY_NUMERIC_D"
    , 0x210: "KEY_CAMERA_FOCUS"
    , 0x211: "KEY_WPS_BUTTON"
    , 0x212: "KEY_TOUCHPAD_TOGGLE"
    , 0x213: "KEY_TOUCHPAD_ON"
    , 0x214: "KEY_TOUCHPAD_OFF"
    , 0x215: "KEY_CAMERA_ZOOMIN"
    , 0x216: "KEY_CAMERA_ZOOMOUT"
    , 0x217: "KEY_CAMERA_UP"
    , 0x218: "KEY_CAMERA_DOWN"
    , 0x219: "KEY_CAMERA_LEFT"
    , 0x21a: "KEY_CAMERA_RIGHT"
    , 0x21b: "KEY_ATTENDANT_ON"
    , 0x21c: "KEY_ATTENDANT_OFF"
    , 0x21d: "KEY_ATTENDANT_TOGGLE"
    , 0x21e: "KEY_LIGHTS_TOGGLE"
    , 0x230: "KEY_ALS_TOGGLE"
    , 0x231: "KEY_ROTATE_LOCK_TOGGLE"
    , 0x232: "KEY_REFRESH_RATE_TOGGLE"
    , 0x240: "KEY_BUTTONCONFIG"
    , 0x241: "KEY_TASKMANAGER"
    , 0x242: "KEY_JOURNAL"
    , 0x243: "KEY_CONTROLPANEL"
    , 0x244: "KEY_APPSELECT"
    , 0x245: "KEY_SCREENSAVER"
    , 0x246: "KEY_VOICECOMMAND"
    , 0x247: "KEY_ASSISTANT"
    , 0x248: "KEY_KBD_LAYOUT_NEXT"
    , 0x249: "KEY_EMOJI_PICKER"
    , 0x24a: "KEY_DICTATE"
    , 0x24b: "KEY_CAMERA_ACCESS_ENABLE"
    , 0x24c: "KEY_CAMERA_ACCESS_DISABLE"
    , 0x24d: "KEY_CAMERA_ACCESS_TOGGLE"
    , 0x24e: "KEY_ACCESSIBILITY"
    , 0x24f: "KEY_DO_NOT_DISTURB"
    , 0x250: "KEY_BRIGHTNESS_MIN"
    , 0x251: "KEY_BRIGHTNESS_MAX"
    , 0x260: "KEY_KBDINPUTASSIST_PREV"
    , 0x261: "KEY_KBDINPUTASSIST_NEXT"
    , 0x262: "KEY_KBDINPUTASSIST_PREVGROUP"
    , 0x263: "KEY_KBDINPUTASSIST_NEXTGROUP"
    , 0x264: "KEY_KBDINPUTASSIST_ACCEPT"
    , 0x265: "KEY_KBDINPUTASSIST_CANCEL"
    , 0x266: "KEY_RIGHT_UP"
    , 0x267: "KEY_RIGHT_DOWN"
    , 0x268: "KEY_LEFT_UP"
    , 0x269: "KEY_LEFT_DOWN"
    , 0x26a: "KEY_ROOT_MENU"
    , 0x26b: "KEY_MEDIA_TOP_MENU"
    , 0x26c: "KEY_NUMERIC_11"
    , 0x26d: "KEY_NUMERIC_12"
    , 0x26e: "KEY_AUDIO_DESC"
    , 0x26f: "KEY_3D_MODE"
    , 0x270: "KEY_NEXT_FAVORITE"
    , 0x271: "KEY_STOP_RECORD"
    , 0x272: "KEY_PAUSE_RECORD"
    , 0x273: "KEY_VOD"
    , 0x274: "KEY_UNMUTE"
    , 0x275: "KEY_FASTREVERSE"
    , 0x276: "KEY_SLOWREVERSE"
    , 0x277: "KEY_DATA"
    , 0x278: "KEY_ONSCREEN_KEYBOARD"
    , 0x279: "KEY_PRIVACY_SCREEN_TOGGLE"
    , 0x27a: "KEY_SELECTIVE_SCREENSHOT"
    , 0x27b: "KEY_NEXT_ELEMENT"
    , 0x27c: "KEY_PREVIOUS_ELEMENT"
    , 0x27d: "KEY_AUTOPILOT_ENGAGE_TOGGLE"
    , 0x27e: "KEY_MARK_WAYPOINT"
    , 0x27f: "KEY_SOS"
    , 0x280: "KEY_NAV_CHART"
    , 0x281: "KEY_FISHING_CHART"
    , 0x282: "KEY_SINGLE_RANGE_RADAR"
    , 0x283: "KEY_DUAL_RANGE_RADAR"
    , 0x284: "KEY_RADAR_OVERLAY"
    , 0x285: "KEY_TRADITIONAL_SONAR"
    , 0x286: "KEY_CLEARVU_SONAR"
    , 0x287: "KEY_SIDEVU_SONAR"
    , 0x288: "KEY_NAV_INFO"
    , 0x289: "KEY_BRIGHTNESS_MENU"
    , 0x290: "KEY_MACRO1"
    , 0x291: "KEY_MACRO2"
    , 0x292: "KEY_MACRO3"
    , 0x293: "KEY_MACRO4"
    , 0x294: "KEY_MACRO5"
    , 0x295: "KEY_MACRO6"
    , 0x296: "KEY_MACRO7"
    , 0x297: "KEY_MACRO8"
    , 0x298: "KEY_MACRO9"
    , 0x299: "KEY_MACRO10"
    , 0x29a: "KEY_MACRO11"
    , 0x29b: "KEY_MACRO12"
    , 0x29c: "KEY_MACRO13"
    , 0x29d: "KEY_MACRO14"
    , 0x29e: "KEY_MACRO15"
    , 0x29f: "KEY_MACRO16"
    , 0x2a0: "KEY_MACRO17"
    , 0x2a1: "KEY_MACRO18"
    , 0x2a2: "KEY_MACRO19"
    , 0x2a3: "KEY_MACRO20"
    , 0x2a4: "KEY_MACRO21"
    , 0x2a5: "KEY_MACRO22"
    , 0x2a6: "KEY_MACRO23"
    , 0x2a7: "KEY_MACRO24"
    , 0x2a8: "KEY_MACRO25"
    , 0x2a9: "KEY_MACRO26"
    , 0x2aa: "KEY_MACRO27"
    , 0x2ab: "KEY_MACRO28"
    , 0x2ac: "KEY_MACRO29"
    , 0x2ad: "KEY_MACRO30"
    , 0x2b0: "KEY_MACRO_RECORD_START"
    , 0x2b1: "KEY_MACRO_RECORD_STOP"
    , 0x2b2: "KEY_MACRO_PRESET_CYCLE"
    , 0x2b3: "KEY_MACRO_PRESET1"
    , 0x2b4: "KEY_MACRO_PRESET2"
    , 0x2b5: "KEY_MACRO_PRESET3"
    , 0x2b8: "KEY_KBD_LCD_MENU1"
    , 0x2b9: "KEY_KBD_LCD_MENU2"
    , 0x2ba: "KEY_KBD_LCD_MENU3"
    , 0x2bb: "KEY_KBD_LCD_MENU4"
    , 0x2bc: "KEY_KBD_LCD_MENU5"
    , 0x2ff: "KEY_MAX"
}
btn_to_str = {
    0x100: "BTN_MISC"
    , 0x100: "BTN_0"
    , 0x101: "BTN_1"
    , 0x102: "BTN_2"
    , 0x103: "BTN_3"
    , 0x104: "BTN_4"
    , 0x105: "BTN_5"
    , 0x106: "BTN_6"
    , 0x107: "BTN_7"
    , 0x108: "BTN_8"
    , 0x109: "BTN_9"
    , 0x110: "BTN_MOUSE"
    , 0x110: "BTN_LEFT"
    , 0x111: "BTN_RIGHT"
    , 0x112: "BTN_MIDDLE"
    , 0x113: "BTN_SIDE"
    , 0x114: "BTN_EXTRA"
    , 0x115: "BTN_FORWARD"
    , 0x116: "BTN_BACK"
    , 0x117: "BTN_TASK"
    , 0x120: "BTN_JOYSTICK"
    , 0x120: "BTN_TRIGGER"
    , 0x121: "BTN_THUMB"
    , 0x122: "BTN_THUMB2"
    , 0x123: "BTN_TOP"
    , 0x124: "BTN_TOP2"
    , 0x125: "BTN_PINKIE"
    , 0x126: "BTN_BASE"
    , 0x127: "BTN_BASE2"
    , 0x128: "BTN_BASE3"
    , 0x129: "BTN_BASE4"
    , 0x12a: "BTN_BASE5"
    , 0x12b: "BTN_BASE6"
    , 0x12f: "BTN_DEAD"
    , 0x130: "BTN_GAMEPAD"
    , 0x130: "BTN_SOUTH"
    , 0x131: "BTN_EAST"
    , 0x132: "BTN_C"
    , 0x133: "BTN_NORTH"
    , 0x134: "BTN_WEST"
    , 0x135: "BTN_Z"
    , 0x136: "BTN_TL"
    , 0x137: "BTN_TR"
    , 0x138: "BTN_TL2"
    , 0x139: "BTN_TR2"
    , 0x13a: "BTN_SELECT"
    , 0x13b: "BTN_START"
    , 0x13c: "BTN_MODE"
    , 0x13d: "BTN_THUMBL"
    , 0x13e: "BTN_THUMBR"
    , 0x140: "BTN_DIGI"
    , 0x140: "BTN_TOOL_PEN"
    , 0x141: "BTN_TOOL_RUBBER"
    , 0x142: "BTN_TOOL_BRUSH"
    , 0x143: "BTN_TOOL_PENCIL"
    , 0x144: "BTN_TOOL_AIRBRUSH"
    , 0x145: "BTN_TOOL_FINGER"
    , 0x146: "BTN_TOOL_MOUSE"
    , 0x147: "BTN_TOOL_LENS"
    , 0x148: "BTN_TOOL_QUINTTAP"
    , 0x149: "BTN_STYLUS3"
    , 0x14a: "BTN_TOUCH"
    , 0x14b: "BTN_STYLUS"
    , 0x14c: "BTN_STYLUS2"
    , 0x14d: "BTN_TOOL_DOUBLETAP"
    , 0x14e: "BTN_TOOL_TRIPLETAP"
    , 0x14f: "BTN_TOOL_QUADTAP"
    , 0x150: "BTN_WHEEL"
    , 0x150: "BTN_GEAR_DOWN"
    , 0x151: "BTN_GEAR_UP"
    , 0x220: "BTN_DPAD_UP"
    , 0x221: "BTN_DPAD_DOWN"
    , 0x222: "BTN_DPAD_LEFT"
    , 0x223: "BTN_DPAD_RIGHT"
    , 0x2c0: "BTN_TRIGGER_HAPPY"
    , 0x2c0: "BTN_TRIGGER_HAPPY1"
    , 0x2c1: "BTN_TRIGGER_HAPPY2"
    , 0x2c2: "BTN_TRIGGER_HAPPY3"
    , 0x2c3: "BTN_TRIGGER_HAPPY4"
    , 0x2c4: "BTN_TRIGGER_HAPPY5"
    , 0x2c5: "BTN_TRIGGER_HAPPY6"
    , 0x2c6: "BTN_TRIGGER_HAPPY7"
    , 0x2c7: "BTN_TRIGGER_HAPPY8"
    , 0x2c8: "BTN_TRIGGER_HAPPY9"
    , 0x2c9: "BTN_TRIGGER_HAPPY10"
    , 0x2ca: "BTN_TRIGGER_HAPPY11"
    , 0x2cb: "BTN_TRIGGER_HAPPY12"
    , 0x2cc: "BTN_TRIGGER_HAPPY13"
    , 0x2cd: "BTN_TRIGGER_HAPPY14"
    , 0x2ce: "BTN_TRIGGER_HAPPY15"
    , 0x2cf: "BTN_TRIGGER_HAPPY16"
    , 0x2d0: "BTN_TRIGGER_HAPPY17"
    , 0x2d1: "BTN_TRIGGER_HAPPY18"
    , 0x2d2: "BTN_TRIGGER_HAPPY19"
    , 0x2d3: "BTN_TRIGGER_HAPPY20"
    , 0x2d4: "BTN_TRIGGER_HAPPY21"
    , 0x2d5: "BTN_TRIGGER_HAPPY22"
    , 0x2d6: "BTN_TRIGGER_HAPPY23"
    , 0x2d7: "BTN_TRIGGER_HAPPY24"
    , 0x2d8: "BTN_TRIGGER_HAPPY25"
    , 0x2d9: "BTN_TRIGGER_HAPPY26"
    , 0x2da: "BTN_TRIGGER_HAPPY27"
    , 0x2db: "BTN_TRIGGER_HAPPY28"
    , 0x2dc: "BTN_TRIGGER_HAPPY29"
    , 0x2dd: "BTN_TRIGGER_HAPPY30"
    , 0x2de: "BTN_TRIGGER_HAPPY31"
    , 0x2df: "BTN_TRIGGER_HAPPY32"
    , 0x2e0: "BTN_TRIGGER_HAPPY33"
    , 0x2e1: "BTN_TRIGGER_HAPPY34"
    , 0x2e2: "BTN_TRIGGER_HAPPY35"
    , 0x2e3: "BTN_TRIGGER_HAPPY36"
    , 0x2e4: "BTN_TRIGGER_HAPPY37"
    , 0x2e5: "BTN_TRIGGER_HAPPY38"
    , 0x2e6: "BTN_TRIGGER_HAPPY39"
    , 0x2e7: "BTN_TRIGGER_HAPPY40"
}
ev_key_no_to_str ={
0: 'KEY_RESERVED'
, 1: 'KEY_ESC'
, 2: 'KEY_1'
, 3: 'KEY_2'
, 4: 'KEY_3'
, 5: 'KEY_4'
, 6: 'KEY_5'
, 7: 'KEY_6'
, 8: 'KEY_7'
, 9: 'KEY_8'
, 10: 'KEY_9'
, 11: 'KEY_0'
, 12: 'KEY_MINUS'
, 13: 'KEY_EQUAL'
, 14: 'KEY_BACKSPACE'
, 15: 'KEY_TAB'
, 16: 'KEY_Q'
, 17: 'KEY_W'
, 18: 'KEY_E'
, 19: 'KEY_R'
, 20: 'KEY_T'
, 21: 'KEY_Y'
, 22: 'KEY_U'
, 23: 'KEY_I'
, 24: 'KEY_O'
, 25: 'KEY_P'
, 26: 'KEY_LEFTBRACE'
, 27: 'KEY_RIGHTBRACE'
, 28: 'KEY_ENTER'
, 29: 'KEY_LEFTCTRL'
, 30: 'KEY_A'
, 31: 'KEY_S'
, 32: 'KEY_D'
, 33: 'KEY_F'
, 34: 'KEY_G'
, 35: 'KEY_H'
, 36: 'KEY_J'
, 37: 'KEY_K'
, 38: 'KEY_L'
, 39: 'KEY_SEMICOLON'
, 40: 'KEY_APOSTROPHE'
, 41: 'KEY_GRAVE'
, 42: 'KEY_LEFTSHIFT'
, 43: 'KEY_BACKSLASH'
, 44: 'KEY_Z'
, 45: 'KEY_X'
, 46: 'KEY_C'
, 47: 'KEY_V'
, 48: 'KEY_B'
, 49: 'KEY_N'
, 50: 'KEY_M'
, 51: 'KEY_COMMA'
, 52: 'KEY_DOT'
, 53: 'KEY_SLASH'
, 54: 'KEY_RIGHTSHIFT'
, 55: 'KEY_KPASTERISK'
, 56: 'KEY_LEFTALT'
, 57: 'KEY_SPACE'
, 58: 'KEY_CAPSLOCK'
, 59: 'KEY_F1'
, 60: 'KEY_F2'
, 61: 'KEY_F3'
, 62: 'KEY_F4'
, 63: 'KEY_F5'
, 64: 'KEY_F6'
, 65: 'KEY_F7'
, 66: 'KEY_F8'
, 67: 'KEY_F9'
, 68: 'KEY_F10'
, 69: 'KEY_NUMLOCK'
, 70: 'KEY_SCROLLLOCK'
, 71: 'KEY_KP7'
, 72: 'KEY_KP8'
, 73: 'KEY_KP9'
, 74: 'KEY_KPMINUS'
, 75: 'KEY_KP4'
, 76: 'KEY_KP5'
, 77: 'KEY_KP6'
, 78: 'KEY_KPPLUS'
, 79: 'KEY_KP1'
, 80: 'KEY_KP2'
, 81: 'KEY_KP3'
, 82: 'KEY_KP0'
, 83: 'KEY_KPDOT'
, 85: 'KEY_ZENKAKUHANKAKU'
, 86: 'KEY_102ND'
, 87: 'KEY_F11'
, 88: 'KEY_F12'
, 89: 'KEY_RO'
, 90: 'KEY_KATAKANA'
, 91: 'KEY_HIRAGANA'
, 92: 'KEY_HENKAN'
, 93: 'KEY_KATAKANAHIRAGANA'
, 94: 'KEY_MUHENKAN'
, 95: 'KEY_KPJPCOMMA'
, 96: 'KEY_KPENTER'
, 97: 'KEY_RIGHTCTRL'
, 98: 'KEY_KPSLASH'
, 99: 'KEY_SYSRQ'
, 100: 'KEY_RIGHTALT'
, 101: 'KEY_LINEFEED'
, 102: 'KEY_HOME'
, 103: 'KEY_UP'
, 104: 'KEY_PAGEUP'
, 105: 'KEY_LEFT'
, 106: 'KEY_RIGHT'
, 107: 'KEY_END'
, 108: 'KEY_DOWN'
, 109: 'KEY_PAGEDOWN'
, 110: 'KEY_INSERT'
, 111: 'KEY_DELETE'
, 112: 'KEY_MACRO'
, 113: 'KEY_MUTE'
, 114: 'KEY_VOLUMEDOWN'
, 115: 'KEY_VOLUMEUP'
, 116: 'KEY_POWER'
, 117: 'KEY_KPEQUAL'
, 118: 'KEY_KPPLUSMINUS'
, 119: 'KEY_PAUSE'
, 120: 'KEY_SCALE'
, 121: 'KEY_KPCOMMA'
, 122: 'KEY_HANGEUL'
, 123: 'KEY_HANJA'
, 124: 'KEY_YEN'
, 125: 'KEY_LEFTMETA'
, 126: 'KEY_RIGHTMETA'
, 127: 'KEY_COMPOSE'
, 128: 'KEY_STOP'
, 129: 'KEY_AGAIN'
, 130: 'KEY_PROPS'
, 131: 'KEY_UNDO'
, 132: 'KEY_FRONT'
, 133: 'KEY_COPY'
, 134: 'KEY_OPEN'
, 135: 'KEY_PASTE'
, 136: 'KEY_FIND'
, 137: 'KEY_CUT'
, 138: 'KEY_HELP'
, 139: 'KEY_MENU'
, 140: 'KEY_CALC'
, 141: 'KEY_SETUP'
, 142: 'KEY_SLEEP'
, 143: 'KEY_WAKEUP'
, 144: 'KEY_FILE'
, 145: 'KEY_SENDFILE'
, 146: 'KEY_DELETEFILE'
, 147: 'KEY_XFER'
, 148: 'KEY_PROG1'
, 149: 'KEY_PROG2'
, 150: 'KEY_WWW'
, 151: 'KEY_MSDOS'
, 152: 'KEY_COFFEE'
, 153: 'KEY_ROTATE_DISPLAY'
, 154: 'KEY_CYCLEWINDOWS'
, 155: 'KEY_MAIL'
, 156: 'KEY_BOOKMARKS'
, 157: 'KEY_COMPUTER'
, 158: 'KEY_BACK'
, 159: 'KEY_FORWARD'
, 160: 'KEY_CLOSECD'
, 161: 'KEY_EJECTCD'
, 162: 'KEY_EJECTCLOSECD'
, 163: 'KEY_NEXTSONG'
, 164: 'KEY_PLAYPAUSE'
, 165: 'KEY_PREVIOUSSONG'
, 166: 'KEY_STOPCD'
, 167: 'KEY_RECORD'
, 168: 'KEY_REWIND'
, 169: 'KEY_PHONE'
, 170: 'KEY_ISO'
, 171: 'KEY_CONFIG'
, 172: 'KEY_HOMEPAGE'
, 173: 'KEY_REFRESH'
, 174: 'KEY_EXIT'
, 175: 'KEY_MOVE'
, 176: 'KEY_EDIT'
, 177: 'KEY_SCROLLUP'
, 178: 'KEY_SCROLLDOWN'
, 179: 'KEY_KPLEFTPAREN'
, 180: 'KEY_KPRIGHTPAREN'
, 181: 'KEY_NEW'
, 182: 'KEY_REDO'
, 183: 'KEY_F13'
, 184: 'KEY_F14'
, 185: 'KEY_F15'
, 186: 'KEY_F16'
, 187: 'KEY_F17'
, 188: 'KEY_F18'
, 189: 'KEY_F19'
, 190: 'KEY_F20'
, 191: 'KEY_F21'
, 192: 'KEY_F22'
, 193: 'KEY_F23'
, 194: 'KEY_F24'
, 200: 'KEY_PLAYCD'
, 201: 'KEY_PAUSECD'
, 202: 'KEY_PROG3'
, 203: 'KEY_PROG4'
, 204: 'KEY_ALL_APPLICATIONS'
, 205: 'KEY_SUSPEND'
, 206: 'KEY_CLOSE'
, 207: 'KEY_PLAY'
, 208: 'KEY_FASTFORWARD'
, 209: 'KEY_BASSBOOST'
, 210: 'KEY_PRINT'
, 211: 'KEY_HP'
, 212: 'KEY_CAMERA'
, 213: 'KEY_SOUND'
, 214: 'KEY_QUESTION'
, 215: 'KEY_EMAIL'
, 216: 'KEY_CHAT'
, 217: 'KEY_SEARCH'
, 218: 'KEY_CONNECT'
, 219: 'KEY_FINANCE'
, 220: 'KEY_SPORT'
, 221: 'KEY_SHOP'
, 222: 'KEY_ALTERASE'
, 223: 'KEY_CANCEL'
, 224: 'KEY_BRIGHTNESSDOWN'
, 225: 'KEY_BRIGHTNESSUP'
, 226: 'KEY_MEDIA'
, 227: 'KEY_SWITCHVIDEOMODE'
, 228: 'KEY_KBDILLUMTOGGLE'
, 229: 'KEY_KBDILLUMDOWN'
, 230: 'KEY_KBDILLUMUP'
, 231: 'KEY_SEND'
, 232: 'KEY_REPLY'
, 233: 'KEY_FORWARDMAIL'
, 234: 'KEY_SAVE'
, 235: 'KEY_DOCUMENTS'
, 236: 'KEY_BATTERY'
, 237: 'KEY_BLUETOOTH'
, 238: 'KEY_WLAN'
, 239: 'KEY_UWB'
, 240: 'KEY_UNKNOWN'
, 241: 'KEY_VIDEO_NEXT'
, 242: 'KEY_VIDEO_PREV'
, 243: 'KEY_BRIGHTNESS_CYCLE'
, 244: 'KEY_BRIGHTNESS_AUTO'
, 245: 'KEY_DISPLAY_OFF'
, 246: 'KEY_WWAN'
, 247: 'KEY_RFKILL'
, 248: 'KEY_MICMUTE'
, 352: 'KEY_OK'
, 353: 'KEY_SELECT'
, 354: 'KEY_GOTO'
, 355: 'KEY_CLEAR'
, 356: 'KEY_POWER2'
, 357: 'KEY_OPTION'
, 358: 'KEY_INFO'
, 359: 'KEY_TIME'
, 360: 'KEY_VENDOR'
, 361: 'KEY_ARCHIVE'
, 362: 'KEY_PROGRAM'
, 363: 'KEY_CHANNEL'
, 364: 'KEY_FAVORITES'
, 365: 'KEY_EPG'
, 366: 'KEY_PVR'
, 367: 'KEY_MHP'
, 368: 'KEY_LANGUAGE'
, 369: 'KEY_TITLE'
, 370: 'KEY_SUBTITLE'
, 371: 'KEY_ANGLE'
, 372: 'KEY_FULL_SCREEN'
, 373: 'KEY_MODE'
, 374: 'KEY_KEYBOARD'
, 375: 'KEY_ASPECT_RATIO'
, 376: 'KEY_PC'
, 377: 'KEY_TV'
, 378: 'KEY_TV2'
, 379: 'KEY_VCR'
, 380: 'KEY_VCR2'
, 381: 'KEY_SAT'
, 382: 'KEY_SAT2'
, 383: 'KEY_CD'
, 384: 'KEY_TAPE'
, 385: 'KEY_RADIO'
, 386: 'KEY_TUNER'
, 387: 'KEY_PLAYER'
, 388: 'KEY_TEXT'
, 389: 'KEY_DVD'
, 390: 'KEY_AUX'
, 391: 'KEY_MP3'
, 392: 'KEY_AUDIO'
, 393: 'KEY_VIDEO'
, 394: 'KEY_DIRECTORY'
, 395: 'KEY_LIST'
, 396: 'KEY_MEMO'
, 397: 'KEY_CALENDAR'
, 398: 'KEY_RED'
, 399: 'KEY_GREEN'
, 400: 'KEY_YELLOW'
, 401: 'KEY_BLUE'
, 402: 'KEY_CHANNELUP'
, 403: 'KEY_CHANNELDOWN'
, 404: 'KEY_FIRST'
, 405: 'KEY_LAST'
, 406: 'KEY_AB'
, 407: 'KEY_NEXT'
, 408: 'KEY_RESTART'
, 409: 'KEY_SLOW'
, 410: 'KEY_SHUFFLE'
, 411: 'KEY_BREAK'
, 412: 'KEY_PREVIOUS'
, 413: 'KEY_DIGITS'
, 414: 'KEY_TEEN'
, 415: 'KEY_TWEN'
, 416: 'KEY_VIDEOPHONE'
, 417: 'KEY_GAMES'
, 418: 'KEY_ZOOMIN'
, 419: 'KEY_ZOOMOUT'
, 420: 'KEY_ZOOMRESET'
, 421: 'KEY_WORDPROCESSOR'
, 422: 'KEY_EDITOR'
, 423: 'KEY_SPREADSHEET'
, 424: 'KEY_GRAPHICSEDITOR'
, 425: 'KEY_PRESENTATION'
, 426: 'KEY_DATABASE'
, 427: 'KEY_NEWS'
, 428: 'KEY_VOICEMAIL'
, 429: 'KEY_ADDRESSBOOK'
, 430: 'KEY_MESSENGER'
, 431: 'KEY_DISPLAYTOGGLE'
, 432: 'KEY_SPELLCHECK'
, 433: 'KEY_LOGOFF'
, 434: 'KEY_DOLLAR'
, 435: 'KEY_EURO'
, 436: 'KEY_FRAMEBACK'
, 437: 'KEY_FRAMEFORWARD'
, 438: 'KEY_CONTEXT_MENU'
, 439: 'KEY_MEDIA_REPEAT'
, 440: 'KEY_10CHANNELSUP'
, 441: 'KEY_10CHANNELSDOWN'
, 442: 'KEY_IMAGES'
, 444: 'KEY_NOTIFICATION_CENTER'
, 445: 'KEY_PICKUP_PHONE'
, 446: 'KEY_HANGUP_PHONE'
, 447: 'KEY_LINK_PHONE'
, 448: 'KEY_DEL_EOL'
, 449: 'KEY_DEL_EOS'
, 450: 'KEY_INS_LINE'
, 451: 'KEY_DEL_LINE'
, 464: 'KEY_FN'
, 465: 'KEY_FN_ESC'
, 466: 'KEY_FN_F1'
, 467: 'KEY_FN_F2'
, 468: 'KEY_FN_F3'
, 469: 'KEY_FN_F4'
, 470: 'KEY_FN_F5'
, 471: 'KEY_FN_F6'
, 472: 'KEY_FN_F7'
, 473: 'KEY_FN_F8'
, 474: 'KEY_FN_F9'
, 475: 'KEY_FN_F10'
, 476: 'KEY_FN_F11'
, 477: 'KEY_FN_F12'
, 478: 'KEY_FN_1'
, 479: 'KEY_FN_2'
, 480: 'KEY_FN_D'
, 481: 'KEY_FN_E'
, 482: 'KEY_FN_F'
, 483: 'KEY_FN_S'
, 484: 'KEY_FN_B'
, 485: 'KEY_FN_RIGHT_SHIFT'
, 497: 'KEY_BRL_DOT1'
, 498: 'KEY_BRL_DOT2'
, 499: 'KEY_BRL_DOT3'
, 500: 'KEY_BRL_DOT4'
, 501: 'KEY_BRL_DOT5'
, 502: 'KEY_BRL_DOT6'
, 503: 'KEY_BRL_DOT7'
, 504: 'KEY_BRL_DOT8'
, 505: 'KEY_BRL_DOT9'
, 506: 'KEY_BRL_DOT10'
, 512: 'KEY_NUMERIC_0'
, 513: 'KEY_NUMERIC_1'
, 514: 'KEY_NUMERIC_2'
, 515: 'KEY_NUMERIC_3'
, 516: 'KEY_NUMERIC_4'
, 517: 'KEY_NUMERIC_5'
, 518: 'KEY_NUMERIC_6'
, 519: 'KEY_NUMERIC_7'
, 520: 'KEY_NUMERIC_8'
, 521: 'KEY_NUMERIC_9'
, 522: 'KEY_NUMERIC_STAR'
, 523: 'KEY_NUMERIC_POUND'
, 524: 'KEY_NUMERIC_A'
, 525: 'KEY_NUMERIC_B'
, 526: 'KEY_NUMERIC_C'
, 527: 'KEY_NUMERIC_D'
, 528: 'KEY_CAMERA_FOCUS'
, 529: 'KEY_WPS_BUTTON'
, 530: 'KEY_TOUCHPAD_TOGGLE'
, 531: 'KEY_TOUCHPAD_ON'
, 532: 'KEY_TOUCHPAD_OFF'
, 533: 'KEY_CAMERA_ZOOMIN'
, 534: 'KEY_CAMERA_ZOOMOUT'
, 535: 'KEY_CAMERA_UP'
, 536: 'KEY_CAMERA_DOWN'
, 537: 'KEY_CAMERA_LEFT'
, 538: 'KEY_CAMERA_RIGHT'
, 539: 'KEY_ATTENDANT_ON'
, 540: 'KEY_ATTENDANT_OFF'
, 541: 'KEY_ATTENDANT_TOGGLE'
, 542: 'KEY_LIGHTS_TOGGLE'
, 560: 'KEY_ALS_TOGGLE'
, 561: 'KEY_ROTATE_LOCK_TOGGLE'
, 562: 'KEY_REFRESH_RATE_TOGGLE'
, 576: 'KEY_BUTTONCONFIG'
, 577: 'KEY_TASKMANAGER'
, 578: 'KEY_JOURNAL'
, 579: 'KEY_CONTROLPANEL'
, 580: 'KEY_APPSELECT'
, 581: 'KEY_SCREENSAVER'
, 582: 'KEY_VOICECOMMAND'
, 583: 'KEY_ASSISTANT'
, 584: 'KEY_KBD_LAYOUT_NEXT'
, 585: 'KEY_EMOJI_PICKER'
, 586: 'KEY_DICTATE'
, 587: 'KEY_CAMERA_ACCESS_ENABLE'
, 588: 'KEY_CAMERA_ACCESS_DISABLE'
, 589: 'KEY_CAMERA_ACCESS_TOGGLE'
, 590: 'KEY_ACCESSIBILITY'
, 591: 'KEY_DO_NOT_DISTURB'
, 592: 'KEY_BRIGHTNESS_MIN'
, 593: 'KEY_BRIGHTNESS_MAX'
, 608: 'KEY_KBDINPUTASSIST_PREV'
, 609: 'KEY_KBDINPUTASSIST_NEXT'
, 610: 'KEY_KBDINPUTASSIST_PREVGROUP'
, 611: 'KEY_KBDINPUTASSIST_NEXTGROUP'
, 612: 'KEY_KBDINPUTASSIST_ACCEPT'
, 613: 'KEY_KBDINPUTASSIST_CANCEL'
, 614: 'KEY_RIGHT_UP'
, 615: 'KEY_RIGHT_DOWN'
, 616: 'KEY_LEFT_UP'
, 617: 'KEY_LEFT_DOWN'
, 618: 'KEY_ROOT_MENU'
, 619: 'KEY_MEDIA_TOP_MENU'
, 620: 'KEY_NUMERIC_11'
, 621: 'KEY_NUMERIC_12'
, 622: 'KEY_AUDIO_DESC'
, 623: 'KEY_3D_MODE'
, 624: 'KEY_NEXT_FAVORITE'
, 625: 'KEY_STOP_RECORD'
, 626: 'KEY_PAUSE_RECORD'
, 627: 'KEY_VOD'
, 628: 'KEY_UNMUTE'
, 629: 'KEY_FASTREVERSE'
, 630: 'KEY_SLOWREVERSE'
, 631: 'KEY_DATA'
, 632: 'KEY_ONSCREEN_KEYBOARD'
, 633: 'KEY_PRIVACY_SCREEN_TOGGLE'
, 634: 'KEY_SELECTIVE_SCREENSHOT'
, 635: 'KEY_NEXT_ELEMENT'
, 636: 'KEY_PREVIOUS_ELEMENT'
, 637: 'KEY_AUTOPILOT_ENGAGE_TOGGLE'
, 638: 'KEY_MARK_WAYPOINT'
, 639: 'KEY_SOS'
, 640: 'KEY_NAV_CHART'
, 641: 'KEY_FISHING_CHART'
, 642: 'KEY_SINGLE_RANGE_RADAR'
, 643: 'KEY_DUAL_RANGE_RADAR'
, 644: 'KEY_RADAR_OVERLAY'
, 645: 'KEY_TRADITIONAL_SONAR'
, 646: 'KEY_CLEARVU_SONAR'
, 647: 'KEY_SIDEVU_SONAR'
, 648: 'KEY_NAV_INFO'
, 649: 'KEY_BRIGHTNESS_MENU'
, 656: 'KEY_MACRO1'
, 657: 'KEY_MACRO2'
, 658: 'KEY_MACRO3'
, 659: 'KEY_MACRO4'
, 660: 'KEY_MACRO5'
, 661: 'KEY_MACRO6'
, 662: 'KEY_MACRO7'
, 663: 'KEY_MACRO8'
, 664: 'KEY_MACRO9'
, 665: 'KEY_MACRO10'
, 666: 'KEY_MACRO11'
, 667: 'KEY_MACRO12'
, 668: 'KEY_MACRO13'
, 669: 'KEY_MACRO14'
, 670: 'KEY_MACRO15'
, 671: 'KEY_MACRO16'
, 672: 'KEY_MACRO17'
, 673: 'KEY_MACRO18'
, 674: 'KEY_MACRO19'
, 675: 'KEY_MACRO20'
, 676: 'KEY_MACRO21'
, 677: 'KEY_MACRO22'
, 678: 'KEY_MACRO23'
, 679: 'KEY_MACRO24'
, 680: 'KEY_MACRO25'
, 681: 'KEY_MACRO26'
, 682: 'KEY_MACRO27'
, 683: 'KEY_MACRO28'
, 684: 'KEY_MACRO29'
, 685: 'KEY_MACRO30'
, 688: 'KEY_MACRO_RECORD_START'
, 689: 'KEY_MACRO_RECORD_STOP'
, 690: 'KEY_MACRO_PRESET_CYCLE'
, 691: 'KEY_MACRO_PRESET1'
, 692: 'KEY_MACRO_PRESET2'
, 693: 'KEY_MACRO_PRESET3'
, 696: 'KEY_KBD_LCD_MENU1'
, 697: 'KEY_KBD_LCD_MENU2'
, 698: 'KEY_KBD_LCD_MENU3'
, 699: 'KEY_KBD_LCD_MENU4'
, 700: 'KEY_KBD_LCD_MENU5'
, 767: 'KEY_MAX'
, 256: 'BTN_0'
, 257: 'BTN_1'
, 258: 'BTN_2'
, 259: 'BTN_3'
, 260: 'BTN_4'
, 261: 'BTN_5'
, 262: 'BTN_6'
, 263: 'BTN_7'
, 264: 'BTN_8'
, 265: 'BTN_9'
, 272: 'BTN_LEFT'
, 273: 'BTN_RIGHT'
, 274: 'BTN_MIDDLE'
, 275: 'BTN_SIDE'
, 276: 'BTN_EXTRA'
, 277: 'BTN_FORWARD'
, 278: 'BTN_BACK'
, 279: 'BTN_TASK'
, 288: 'BTN_TRIGGER'
, 289: 'BTN_THUMB'
, 290: 'BTN_THUMB2'
, 291: 'BTN_TOP'
, 292: 'BTN_TOP2'
, 293: 'BTN_PINKIE'
, 294: 'BTN_BASE'
, 295: 'BTN_BASE2'
, 296: 'BTN_BASE3'
, 297: 'BTN_BASE4'
, 298: 'BTN_BASE5'
, 299: 'BTN_BASE6'
, 303: 'BTN_DEAD'
, 304: 'BTN_SOUTH'
, 305: 'BTN_EAST'
, 306: 'BTN_C'
, 307: 'BTN_NORTH'
, 308: 'BTN_WEST'
, 309: 'BTN_Z'
, 310: 'BTN_TL'
, 311: 'BTN_TR'
, 312: 'BTN_TL2'
, 313: 'BTN_TR2'
, 314: 'BTN_SELECT'
, 315: 'BTN_START'
, 316: 'BTN_MODE'
, 317: 'BTN_THUMBL'
, 318: 'BTN_THUMBR'
, 320: 'BTN_TOOL_PEN'
, 321: 'BTN_TOOL_RUBBER'
, 322: 'BTN_TOOL_BRUSH'
, 323: 'BTN_TOOL_PENCIL'
, 324: 'BTN_TOOL_AIRBRUSH'
, 325: 'BTN_TOOL_FINGER'
, 326: 'BTN_TOOL_MOUSE'
, 327: 'BTN_TOOL_LENS'
, 328: 'BTN_TOOL_QUINTTAP'
, 329: 'BTN_STYLUS3'
, 330: 'BTN_TOUCH'
, 331: 'BTN_STYLUS'
, 332: 'BTN_STYLUS2'
, 333: 'BTN_TOOL_DOUBLETAP'
, 334: 'BTN_TOOL_TRIPLETAP'
, 335: 'BTN_TOOL_QUADTAP'
, 336: 'BTN_GEAR_DOWN'
, 337: 'BTN_GEAR_UP'
, 544: 'BTN_DPAD_UP'
, 545: 'BTN_DPAD_DOWN'
, 546: 'BTN_DPAD_LEFT'
, 547: 'BTN_DPAD_RIGHT'
, 704: 'BTN_TRIGGER_HAPPY1'
, 705: 'BTN_TRIGGER_HAPPY2'
, 706: 'BTN_TRIGGER_HAPPY3'
, 707: 'BTN_TRIGGER_HAPPY4'
, 708: 'BTN_TRIGGER_HAPPY5'
, 709: 'BTN_TRIGGER_HAPPY6'
, 710: 'BTN_TRIGGER_HAPPY7'
, 711: 'BTN_TRIGGER_HAPPY8'
, 712: 'BTN_TRIGGER_HAPPY9'
, 713: 'BTN_TRIGGER_HAPPY10'
, 714: 'BTN_TRIGGER_HAPPY11'
, 715: 'BTN_TRIGGER_HAPPY12'
, 716: 'BTN_TRIGGER_HAPPY13'
, 717: 'BTN_TRIGGER_HAPPY14'
, 718: 'BTN_TRIGGER_HAPPY15'
, 719: 'BTN_TRIGGER_HAPPY16'
, 720: 'BTN_TRIGGER_HAPPY17'
, 721: 'BTN_TRIGGER_HAPPY18'
, 722: 'BTN_TRIGGER_HAPPY19'
, 723: 'BTN_TRIGGER_HAPPY20'
, 724: 'BTN_TRIGGER_HAPPY21'
, 725: 'BTN_TRIGGER_HAPPY22'
, 726: 'BTN_TRIGGER_HAPPY23'
, 727: 'BTN_TRIGGER_HAPPY24'
, 728: 'BTN_TRIGGER_HAPPY25'
, 729: 'BTN_TRIGGER_HAPPY26'
, 730: 'BTN_TRIGGER_HAPPY27'
, 731: 'BTN_TRIGGER_HAPPY28'
, 732: 'BTN_TRIGGER_HAPPY29'
, 733: 'BTN_TRIGGER_HAPPY30'
, 734: 'BTN_TRIGGER_HAPPY31'
, 735: 'BTN_TRIGGER_HAPPY32'
, 736: 'BTN_TRIGGER_HAPPY33'
, 737: 'BTN_TRIGGER_HAPPY34'
, 738: 'BTN_TRIGGER_HAPPY35'
, 739: 'BTN_TRIGGER_HAPPY36'
, 740: 'BTN_TRIGGER_HAPPY37'
, 741: 'BTN_TRIGGER_HAPPY38'
, 742: 'BTN_TRIGGER_HAPPY39'
, 743: 'BTN_TRIGGER_HAPPY40'
}

ev_rel_no_to_str      ={
     0x00:"REL_X"
    ,0x01:"REL_Y"
    ,0x02:"REL_Z"
    ,0x03:"REL_RX"
    ,0x04:"REL_RY"
    ,0x05:"REL_RZ"
    ,0x06:"REL_HWHEEL"
    ,0x07:"REL_DIAL"
    ,0x08:"REL_WHEEL"
    ,0x09:"REL_MISC"
    #"0x0a is reserved and should not be used in input drivers."
    ,0x0a:"REL_RESERVED"
    ,0x0b:"REL_WHEEL_HI_RES"
    ,0x0c:"REL_HWHEEL_HI_RES"
    ,0x0f:"REL_MAX"
    #(REL_MAX+1):"REL_CNT"
}
ev_abs_no_to_str    ={
     0x00:"ABS_X"
    ,0x01:"ABS_Y"
    ,0x02:"ABS_Z"
    ,0x03:"ABS_RX"
    ,0x04:"ABS_RY"
    ,0x05:"ABS_RZ"
    ,0x06:"ABS_THROTTLE"
    ,0x07:"ABS_RUDDER"
    ,0x08:"ABS_WHEEL"
    ,0x09:"ABS_GAS"
    ,0x0a:"ABS_BRAKE"
    ,0x10:"ABS_HAT0X"
    ,0x11:"ABS_HAT0Y"
    ,0x12:"ABS_HAT1X"
    ,0x13:"ABS_HAT1Y"
    ,0x14:"ABS_HAT2X"
    ,0x15:"ABS_HAT2Y"
    ,0x16:"ABS_HAT3X"
    ,0x17:"ABS_HAT3Y"
    ,0x18:"ABS_PRESSURE"
    ,0x19:"ABS_DISTANCE"
    ,0x1a:"ABS_TILT_X"
    ,0x1b:"ABS_TILT_Y"
    ,0x1c:"ABS_TOOL_WIDTH"
    ,0x20:"ABS_VOLUME"
    ,0x21:"ABS_PROFILE"
    ,0x28:"ABS_MISC"
    #"0x2e is reserved and should not be used in input drivers."{
    ,0x2e:"ABS_RESERVED"
    #:"ABS_MT_SLOT"
    #:"ABS_MT_TOUCH_MAJOR"
    #:"ABS_MT_TOUCH_MINOR"
    #:"ABS_MT_WIDTH_MAJOR"
    #:"ABS_MT_WIDTH_MINOR"
    #:"ABS_MT_ORIENTATION"
    #:"ABS_MT_POSITION_X"
    #:"ABS_MT_POSITION_Y"
    #:"ABS_MT_TOOL_TYPE"
    #:"ABS_MT_BLOB_ID"
    #:"ABS_MT_TRACKING_ID"
    #:"ABS_MT_PRESSURE"
    #:"ABS_MT_DISTANCE"
    #:"ABS_MT_TOOL_X"
    #:"ABS_MT_TOOL_Y"
    ,0x3f:"ABS_MAX"
    #(ABS_MAX+1):"ABS_CNT"
}
ev_sw_no_to_str     ={
     0x00  :"SW_LID"
    ,0x01  :"SW_TABLET_MODE"
    ,0x02  :"SW_HEADPHONE_INSERT"
    ,0x03  :"SW_RFKILL_ALL"
    #:"SW_RADIO"
    ,0x04  :"SW_MICROPHONE_INSERT"
    ,0x05  :"SW_DOCK"
    #,0x06  :"SW_LINEOUT_INSERT"
    ,0x06  :"SW_JACK_PHYSICAL_INSERT"
    ,0x08  :"SW_VIDEOOUT_INSERT"
    ,0x09  :"SW_CAMERA_LENS_COVER"
    ,0x0a  :"SW_KEYPAD_SLIDE"
    ,0x0b  :"SW_FRONT_PROXIMITY"
    ,0x0c  :"SW_ROTATE_LOCK"
    ,0x0d  :"SW_LINEIN_INSERT"
    ,0x0e  :"SW_MUTE_DEVICE"
    ,0x0f  :"SW_PEN_INSERTED"
    ,0x10  :"SW_MACHINE_COVER"
   # ,0x10:"SW_MAX"
    #(SW_MAX+1):"SW_CNT"
}
ev_msc_no_to_str   ={
     0x00:"MSC_SERIAL"
    ,0x01:"MSC_PULSELED"
    ,0x02:"MSC_GESTURE"
    ,0x03:"MSC_RAW"
    ,0x04:"MSC_SCAN"
    ,0x05:"MSC_TIMESTAMP"
    ,0x07:"MSC_MAX"
    #(MSC_MAX+1):"MSC_CNT"
}
ev_led_no_to_str     ={
     0x00:"LED_NUML"
    ,0x01:"LED_CAPSL"
    ,0x02:"LED_SCROLLL"
    ,0x03:"LED_COMPOSE"
    ,0x04:"LED_KANA"
    ,0x05:"LED_SLEEP"
    ,0x06:"LED_SUSPEND"
    ,0x07:"LED_MUTE"
    ,0x08:"LED_MISC"
    ,0x09:"LED_MAIL"
    ,0x0a:"LED_CHARGING"
    ,0x0f:"LED_MAX"
    #(LED_MAX+1):"LED_CNT"
}
ev_rep_no_to_str     ={
     0x00:"REP_DELAY"
    ,0x01:"REP_PERIOD"
    #,0x01:"REP_MAX"
    ,0x02:"REP_CNT"
}
ev_snd_no_to_str    ={
     0x00:"SND_CLICK"
    ,0x01:"SND_BELL"
    ,0x02:"SND_TONE"
    ,0x07:"SND_MAX"
    #(SND_MAX+1):"SND_CNT"
}

ev_syn_codes=[0,1,2,3,15]
ev_key_codes=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,117,118,119,121,122,123,124,125,126,127,129,132,141,145,146,147,148,149,151,154,155,157,160,161,162,163,164,165,166,167,168,170,175,176,177,178,179,180,183,184,185,186,187,188,189,190,191,192,193,194,200,201,202,203,205,207,208,209,211,212,213,214,215,216,217,218,220,221,222,224,225,226,228,229,230,235,236,237,238,239,240,256,257,258,259,260,261,262,263,264,265,272,273,274,275,276,277,278,279,288,289,290,291,292,293,294,295,296,297,298,299,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,320,321,322,323,324,325,326,327,329,330,331,332,333,334,336,337,352,353,354,355,356,357,359,360,361,363,364,365,367,368,369,370,371,373,374,382,385,387,388,390,391,394,395,397,398,399,400,401,404,406,407,408,409,410,411,412,413,414,415,432,433,434,435,437,447,448,449,450,451,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,497,498,499,500,501,502,503,504,505,506,514,515,516,517,518,519,520,521,522,523,525,526,527,528,531,532,533,534,535,536,537,538,539,540,544,545,546,547,608,609,610,611,612,613,614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,629,630,631,632,633,634,635,636,637,638,639,640,641,642,643,644,645,646,647,648,649,656,657,658,659,660,661,662,663,664,665,666,667,668,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,688,689,690,691,692,693,696,697,698,699,700,704,705,706,707,708,709,710,711,712,713,714,715,716,717,718,719,720,721,722,723,724,725,726,727,728,729,730,731,732,733,734,735,736,737,738,739,740,741,742,743,767]
ev_rel_codes=[0,1,2,3,4,5,6,7,8,9,10,11,12,15]
ev_abs_codes=[0,1,2,3,4,5,6,7,8,9,10,16,17,18,19,20,21,22,23,24,25,26,27,28,32,33,40,46,63]
ev_msc_codes=[0,1,2,3,4,5,7]
ev_sw_codes=[0,1,2,4,5,6,8,9,10,11,12,13,14,15,16]
ev_led_codes=[0,1,2,3,4,5,6,7,8,9,10,15]
ev_snd_codes=[0,1,2,7]
ev_rep_codes=[0,1]

#a_lot_of_caps = {
    #  0x00:  ev_syn_codes #EV_SYN"
    # ,0x01: ev_key_codes #"EV_KEY"
    # ,0x02: ev_rel_codes #"EV_REL"
    # ,0x03: ev_abs_codes #"EV_ABS"
    # ,0x04: ev_msc_codes #"EV_MSC"
    # ,0x05: ev_sw_codes #"EV_SW"
    # ,0x11: ev_led_codes #"EV_LED"
    # ,0x12: ev_snd_codes #"EV_SND"
    # ,0x14: ev_rep_codes #"EV_REP"
    # ,0x15: {}#"EV_FF"
    # ,0x16: {}#"EV_PWR"
    # ,0x17:() #"EV_FF_STATUS"
    # ,0x1f: {}#:"EV_MAX"
    #(EV_MAX+1):"EV_CNT"
#}

ev_type_code_no_to_str={
     0x00:  ev_syn_no_to_str #EV_SYN"
    ,0x01: ev_key_no_to_str #"EV_KEY"
    ,0x02: ev_rel_no_to_str #"EV_REL"
    ,0x03: ev_abs_no_to_str #"EV_ABS"
    ,0x04: ev_msc_no_to_str #"EV_MSC"
    ,0x05: ev_sw_no_to_str #"EV_SW"
    ,0x11: ev_led_no_to_str #"EV_LED"
    ,0x12: ev_snd_no_to_str #"EV_SND"
    ,0x14: ev_rep_no_to_str #"EV_REP"
    ,0x15: {}#"EV_FF"
    ,0x16: {}#"EV_PWR"
    ,0x17:() #"EV_FF_STATUS"
    ,0x1f: {}#:"EV_MAX"
    #(EV_MAX+1):"EV_CNT"
}

def dict_to_list(name,d):
    l=[str(key) for key in d.keys()]
    #ic(l)
    l=','.join(l)
    print(f'{name}=[{l}]')

def list_maker():
    # "EV_SYN": 0
    dict_to_list("ev_syn_codes", ev_syn_no_to_str)
    # , "EV_KEY": 1
    dict_to_list("ev_key_codes", ev_key_no_to_str)
    # , "EV_REL": 2
    dict_to_list("ev_rel_codes", ev_rel_no_to_str)
    # , "EV_ABS": 3
    dict_to_list("ev_abs_codes", ev_abs_no_to_str)
    # , "EV_MSC": 4
    dict_to_list("ev_msc_codes",ev_msc_no_to_str)
    # , "EV_SW": 5
    dict_to_list("ev_sw_codes", ev_sw_no_to_str)
    # , "EV_LED": 17
    dict_to_list('ev_led_codes',ev_led_no_to_str)
    # , "EV_SND": 18
    dict_to_list('ev_snd_codes', ev_snd_no_to_str)
    # , "EV_REP": 20
    dict_to_list("ev_rep_codes", ev_rep_no_to_str)
    # , "EV_FF": 21
    #dict_to_list("ev_ff_codes", ev_ff_no_to_str)
    # , "EV_PWR": 22
    #dict_to_list("ev_pwr_codes", ev_pwr_no_to_str)
    # , "EV_FF_STATUS": 23
    #dict_to_list("ev_ff_status_codes", ev_ff_status_no_to_str)
    # , "EV_MAX": 31
    #dict_to_list("ev_max_codes", ev_max_no_to_str)
    # , "EV_CNT": 32
    #dict_to_list("ev_cnt_codes", ev_cnt_no_to_str)

def main():
    print(ev_type_code_no_to_str[1][272])
    dict_to_list("ev_types", ev_type_no_to_str)

if __name__ == '__main__':
    # newd={}
    # komma=''
    # for key,item in event_types_by_name.items():
    #     if not key in newd:
    #         newd[key]=item
    #         print(f'    {komma}"{key}":{item}')
    #         komma=','
    main()