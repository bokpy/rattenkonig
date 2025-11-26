#!/usr/bin/python3
import ctypes
import os
xqp_path=os.path.abspath('.')+'/xqp_wrapper.so'
print(f'{xqp_path=}')
libObject = ctypes.CDLL(xqp_path)
# libObject.xqp_init()
# libObject.xqp_show()
# libObject.xqp_find_mouse_window()
# libObject.xqp_get_name_and_class()
# libObject.xqp_close()
window =  libObject.xqp_init()
print(f'Opened {window=}')

show = libObject.xqp_show(window)
print (f'xqp_show({window=}) -> {show}')

mouse_window=libObject.xqp_find_mouse_window()
print(f'{mouse_window=}')

c_string_name=ctypes.c_char_p(b'win_name win_name win_name win_name')
c_string_class_name=ctypes.c_char_p(b'class_name  class_name  class_name  ')
c_string_class_class=ctypes.c_char_p(b'class_class class_class class_class ')

result = libObject.xqp_get_name_and_class(
    mouse_window
    ,c_string_name
    ,c_string_class_name
    ,c_string_class_class
    )
print (f'"{c_string_name.value=}"')
print (f'"{c_string_class_name.value =}"')
print (f'"{c_string_class_class.value=}"')
print (f'{result=}\n')

active_window = libObject.find_active_window()
print(f'{active_window=}')

closed = libObject.xqp_close()
print (f'xqp_close() -> {closed}')
closed = libObject.xqp_close()
print (f'xqp_close() -> {closed}')
