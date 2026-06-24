#!/usr/bin/python3
from evdev import UInput, ecodes as ec
import evdev as ev
import time
import atexit
# import ladders as ladder
# import  tracer as trace
#from ladders import ascii_to_evdev as asc2ev
#import toys as toy
from icecream import ic
ic.configureOutput(includeContext=True)

PRINT=print
KEYDELAY=.01
L_SHIFT=SHIFT=42
R_SHIFT=54
help_text="""
ChatGPT:

Allow non-root access to /dev/uinput via udev (recommended)

Description
-----------
Create a persistent udev rule that sets the device node for /dev/uinput to a group
you control (for example 'uinput'), then add your user to that group. This
permits opening the uinput device from a regular user process without running
the script as root.

Steps (one-time, run as root):
  1. Create group and add your user:
	 sudo groupadd --system uinput    # only if group doesn't exist
	 sudo usermod -aG uinput <your-user>

  2. Create udev rule (file: /etc/udev/rules.d/99-uinput.rules):
	 KERNEL=="uinput", SUBSYSTEM=="misc", MODE="0660", GROUP="uinput"

  3. Reload udev rules and trigger:
	 sudo udevadm control --reload-rules
	 sudo udevadm trigger --action=add /dev/uinput

Notes
-----
• This is persistent across reboots and is the safest common approach.
• If /dev/uinput already exists with different attributes on your distro, adapt
  the rule (or use GROUP="input" if preferred).
• After these steps log out and back in (or reboot) so group membership takes effect.

Justness estimate: 92% — typical on most Linux distributions using udev.

"""
asc2ev = {
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


#CAPS = {ec.EV_LED:ladder.ev_led_codes,ec.EV_KEY: ladder.ev_key_codes, ec.EV_REL: ladder.ev_rel_codes}

CAPS={
	#0 : [0, 1, 2, 3, 4, 17, 20]
	ec.EV_KEY : [
	       1,
	       2,
	       3,
	       4,
	       5,
	       6,
	       7,
	       8,
	       9,
	       10,
	       11,
	       12,
	       13,
	       14,
	       15,
	       16,
	       17,
	       18,
	       19,
	       20,
	       21,
	       22,
	       23,
	       24,
	       25,
	       26,
	       27,
	       28,
	       29,
	       30,
	       31,
	       32,
	       33,
	       34,
	       35,
	       36,
	       37,
	       38,
	       39,
	       40,
	       41,
	       42,
	       43,
	       44,
	       45,
	       46,
	       47,
	       48,
	       49,
	       50,
	       51,
	       52,
	       53,
	       54,
	       55,
	       56,
	       57,
	       58,
	       59,
	       60,
	       61,
	       62,
	       63,
	       576,
	       577,
	       578,
	       579,
	       580,
	       581,
	       582,
	       583,
	       584,
	       585,
	       74,
	       586,
	       587,
	       588,
	       78,
	       589,
	       592,
	       593,
	       73,
	       75,
	       76,
	       77,
	       79,
	       80,
	       81,
	       82,
	       83,
	       85,
	       86,
	       87,
	       88,
	       89,
	       608,
	       609,
	       610,
	       611,
	       612,
	       613,
	       93,
	       103,
	       95,
	       105,
	       106,
	       98,
	       108,
	       100,
	       110,
	       111,
	       104,
	       113,
	       114,
	       115,
	       116,
	       109,
	       117,
	       119,
	       120,
	       121,
	       122,
	       123,
	       124,
	       125,
	       126,
	       127,
	       128,
	       129,
	       130,
	       131,
	       132,
	       133,
	       134,
	       135,
	       136,
	       137,
	       138,
	       139,
	       140,
	       107,
	       142,
	       143,
	       144,
	       150,
	       152,
	       155,
	       156,
	       158,
	       159,
	       161,
	       163,
	       164,
	       165,
	       166,
	       167,
	       168,
	       169,
	       171,
	       172,
	       173,
	       174,
	       176,
	       177,
	       178,
	       179,
	       180,
	       181,
	       182,
	       183,
	       184,
	       185,
	       186,
	       187,
	       188,
	       189,
	       190,
	       191,
	       192,
	       193,
	       194,
	       204,
	       206,
	       207,
	       208,
	       209,
	       210,
	       212,
	       216,
	       217,
	       219,
	       223,
	       224,
	       225,
	       228,
	       229,
	       230,
	       231,
	       232,
	       233,
	       234,
	       235,
	       240,
	       241,
	       244,
	       256,
	       272,
	       273,
	       274,
	       275,
	       276,
	       277,
	       278,
	       279,
	       102,
	       320,
	       64,
	       65,
	       330,
	       331,
	       332,
	       66,
	       67,
	       68,
	       69,
	       353,
	       354,
	       70,
	       358,
	       71,
	       362,
	       72,
	       366,
	       370,
	       372,
	       374,
	       375,
	       376,
	       377,
	       378,
	       379,
	       380,
	       381,
	       383,
	       384,
	       386,
	       387,
	       389,
	       392,
	       393,
	       396,
	       397,
	       398,
	       399,
	       400,
	       401,
	       402,
	       403,
	       405,
	       407,
	       408,
	       409,
	       410,
	       412,
	       416,
	       417,
	       418,
	       419,
	       420,
	       421,
	       422,
	       423,
	       424,
	       425,
	       426,
	       427,
	       428,
	       429,
	       430,
	       431,
	       432,
	       433,
	       439,
	       442,
	       90,
	       91,
	       92,
	       94,
	       96,
	       97,
	       99
       ]
	,ec.EV_REL : [0, 1, 6, 8, 11, 12]
       #, ec.EV_ABS : [
	   #     (32, AbsInfo(value=0, min=0, max=572, fuzz=0, flat=0, resolution=0)),
	   #     (32, AbsInfo(value=0, min=1, max=1023, fuzz=0, flat=0, resolution=0)),
	   #     (32, AbsInfo(value=0, min=0, max=668, fuzz=0, flat=0, resolution=0)),
	   #     (1, AbsInfo(value=0, min=0, max=15240, fuzz=0, flat=0, resolution=200)),
	   #     (0, AbsInfo(value=0, min=0, max=20320, fuzz=0, flat=0, resolution=200)),
	   #     (32, AbsInfo(value=0, min=0, max=896, fuzz=0, flat=0, resolution=0)),
	   #     (24, AbsInfo(value=0, min=0, max=8191, fuzz=0, flat=0, resolution=0))
       # ],
       #4 : [4],
    ,ec.EV_LED: [0, 1, 2, 3, 4]
}

# def is_iterable(obj):
# 	try:
# 		iter(obj)
# 		return True
# 	except TypeError:
# 		return False

def name_key_button(code):
	if code in ec.KEY:
		return ec.KEY[code]
	return ec.BTN.get(code,'No Key or Button')

class PiedPiper(UInput):
	"""class writing the mouse and keyboard events"""
	piper=None

	def __init__(S):
		if PiedPiper.piper:
			print(f'There should only bee one Pied Piper.')
			exit(666)
		try:
			#super().__init__(name="Pied Piper of Hamelin")
			super().__init__(CAPS,name="Pied Piper of Hamelin")
		except PermissionError as e:
			print(help_text)
			exit (e.errno)
		PiedPiper.piper=S
		#S.pressed_keys=None
		#trace.open_window()
		atexit.register(S.leave_hamelin)

	def leave_hamelin(S):
		#trace.close_window()
		S.close()
		print(f'Pied Piper left Hamelin.')

	def rel_move(S,ev_code,ev_value):
		"""
		send a relative move event to the UInput device
		:param ev_code: a code for the move event
		:param ev_value: the value for the move event
		:return:  S
		"""
		PRINT(f'Move {ev_value}')
		S.write(ec.EV_REL,ev_code,ev_value)
		S.syn()
		S.syn_report()
		return S

	def syn_report(S):
		S.write(ec.EV_SYN,ec.SYN_REPORT,0)

	def passthrough(S,event):
		"""
		send an event to the UInput device.
		use to pass trough un altered events
		:param event: an evdev event
		:return: S
		"""
		PRINT(f'passthrough({ev.categorize(event)})')
	
		S.write_event(event)
		S.syn()
		return S

	def passthrough_code(S,ev_type,ev_code,ev_value):
		"""
		send an event to the UInput device.
		:param ev_type:
		:param ev_code:
		:param ev_value:
		:return: S
		"""
		S.write(ev_type,ev_code,ev_value)
		S.syn()
		return S

	def default(S,event):
		"""
		print an event for debuging
		:param event: event to print
		:return: S
		"""
		print(f'PiedPiper.default({ev.categorize(event)})')
		return S

	def simultaneous_keys(S,*args):
		"""
		press  keys together and also release.
		:param args: button and or keycodes
		:return: S
		"""
		S.hold(*args)
		time.sleep(KEYDELAY)
		S.release(*args)
		return S

	def type_key(S,key:int):
		'''
		simulate a single key or button press
		:param key: evdev.ecode.code of a key or button
		:type key: int
		:return: S
		:rtype: PiedPiper
		'''
		S.write(ec.EV_KEY,key,1)
		S.syn()
		time.sleep(KEYDELAY)
		S.write(ec.EV_KEY,key,0)
		S.syn()
		return S
	
	def  type_keys(S,*args):
		"""
		type the keys in args like typed from a keyboard
		:param args: key codes
		:return: S
		"""
		for key in args:
			#print(f'[{ec.KEY[key]}] ',end='')
			S.type_key(key)
		#print()
		return S

	def hold(S,*args):
		'''
		press and hold a number of keys and/or buttons simultaneous.
		:param args: evdev.ecode.code of keys and/or buttons
		:type args: int
		:return: S
		:rtype: PiedPiper
		'''
		for key in args:
			PRINT(f'hold({name_key_button(key)})')
			S.write(ec.EV_KEY,key,1)
		time.sleep(KEYDELAY)
		S.syn()
		return S

	def release(S,*args):
		'''
		release keys/buttons previous pressed and holded
		:param args: keys/buttons to release
		:type args: int
		:return: S
		:rtype: PiedPiper
		'''
		
		for key in args:
			PRINT(f'release({name_key_button(key)})')
			S.write(ec.EV_KEY,key,0)
		time.sleep(KEYDELAY)
		S.syn()
		return S

	def message(S,s):
		'''
		print a string as typed from a keyboard without capslock on.
		:param s: Ascii string to type
		:type s: str
		:return: S
		:rtype: PiedPiper
		'''
		for c in s:
			code,shift = asc2ev[ord(c)]
			if shift:
				S.simultaneous_keys(SHIFT,code)
				continue
			S.type_key(code)
		return S

	def nap(S,snooze=KEYDELAY):
		"""
		do sleep
		:param snooze: seconds to sleep
		:return: S
		"""
		time.sleep(snooze)
		return S

	# def id_active_window(S):
	# 	return trace.active_window_name_and_classes()
	#
	# def match_active_window(S,name=None,class_name=None,class_class=None,show=False):
	# 	n,cn,cc=trace.active_window_name_and_classes()
	# 	#n,cn,cc=trace.mouse_over_window_name_and_classes()
	# 	if (not n) or (n == "Bad Window"):
	# 		return False
	# 	if show:
	# 		print(f'"{n}","{cn}","{cc}"')
	# 	if name and (not name in n ):
	# 		return False
	# 	if class_name and (not class_name in cn ):
	# 		return False
	# 	if class_class and (not class_class in cc):
	# 		return False
	# 	return True

	# def id_mouse_window(S):
	# 	return trace.mouse_over_window_name_and_classes()

def test_piper():
	piper=PiedPiper()
	#print(piper.capabilities())
	for i in range(1,20):
		piper.passthrough_code(ec.EV_KEY, ec.KEY_1+i, 1)
		piper.passthrough_code(ec.EV_KEY, ec.KEY_1+i, 0)
		time.sleep(.3)

	dirx=10
	diry=16
	for i in range(20):
		if i % 30 == 0:
			dirx=-dirx
		if i % 80 == 0:
			diry=-diry
		piper.rel_move( ec.REL_X, dirx)
		piper.rel_move( ec.REL_Y, diry)
		time.sleep(.3)
	#second_ratter=PiedPiper()
		#
def test_message():
	ratter=PiedPiper()
	time.sleep(3)
	print('Message Start:')
	ratter.message('Hello World!')
	print('Message End:')

# def test_trace():
# 	piper=PiedPiper()
# 	count = 5
# 	last=''
# 	while count>0:
# 		n,cn,cc=piper.id_active_window()
# 		if n != last:
# 			count-=1
# 			last=n
# 			print(f'{n},{cn},{cc}')

def test_hold_keys():
	time.sleep(3)
	piper=PiedPiper()
	ic(piper)
	piper.press_and_hold((ec.BTN_LEFT,ec.BTN_RIGHT))
	print(piper.device.active_keys(verbose=True))
	piper.message('<Buttons Pressed Message.>')
	piper.release((ec.BTN_RIGHT,ec.BTN_LEFT))
	print(piper.device.active_keys(verbose=True))
	time.sleep(3)

def main():
	#test_piper()
	test_message()
	#test_trace()
	#test_hold_keys()

if __name__=='__main__':
	main()
