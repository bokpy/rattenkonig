#!/usr/bin/python3
import ctypes
import time
import re
import atexit
from icecream import ic
ic.configureOutput(includeContext=True)

#clean_ascii=re.compile(r'[\w\d\. -]+')
clean_ascii=re.compile(r'\x1b%.')
# xqp_path=os.path.abspath('.')+'/xqp_wrapper.so'
# print(f'{xqp_path=}')
#libObject = ctypes.CDLL(xqp_path)
libObject = ctypes.CDLL('./xqp_wrapper.so')
# libObject.xqp_init()
# libObject.xqp_show()
# libObject.xqp_find_mouse_window()
# libObject.xqp_get_name_and_class()
# libObject.xqp_close()

window = None
def open_window():
    global window
    window =  libObject.xqp_init()
    print(f'Opened {window=}')

def show_window_info(window):
    show = libObject.xqp_show(window)
    #print (f'xqp_show({window=}) -> {show}')

def get_mouse_over_window():
    mouse_window=libObject.xqp_find_mouse_window()
    return mouse_window

#Allocate a buffers
buffer_size = 256
result_buffers= [
    ctypes.create_string_buffer(buffer_size)
    , ctypes.create_string_buffer(buffer_size)
    , ctypes.create_string_buffer(buffer_size)
   ]

libObject.xqp_get_name_and_class.restype = ctypes.c_int
libObject.xqp_get_name_and_class.argtypes = \
    [ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]

def get_window_id(mouse_window):
    if not mouse_window:
        return 'Bad Window', 'Bad Window', 'Bad Window'
    result = libObject.xqp_get_name_and_class(mouse_window,*result_buffers)
    result_strings=[ res.value.decode('ascii') for res in result_buffers]
    result_strings[0]=clean_ascii.sub('*',result_strings[0])
    return result_strings

def get_active_window():
    active_window= libObject.find_active_window()
    #print(f'{active_window} <- get_active_window()')
    return active_window

def close_window():
    global window
    if not window:
        ic()
        print("No window to close.")
        return
    if libObject.xqp_close():
        print(f"\nwindow {window} closed.")
        window=None
        return
    ic()
    print(f"window {window} failed to close.")

def mouse_over_window_name_and_classes():
    mouse_window=get_mouse_over_window()
    return get_window_id(mouse_window)

def active_window_name_and_classes():
    mouse_window=get_active_window()
    return get_window_id(mouse_window)

atexit.register(close_window)

def show_pointed_windows():
    win=open_window()
    print('\nMove the mouse pointer over the windows to indentify it.')
    timeout=5
    stop_time=time.time()
    time_limit=stop_time + timeout
    print(f'Stay {timeout}sec over the same window to stop.')
    prev=None
    visited=[]
    field = lambda x:x[0]
    while stop_time < time_limit:
        mouse_window=get_mouse_over_window()
        #mouse_window=get_active_window()
        wn,wcn,wcc=get_window_id(mouse_window)
        stop_time=time.time()
        if prev != wn:
            if (wn,wcn,wcc) not in visited:
                visited.append((wn,wcn,wcc))
            time_limit=stop_time + timeout
            print(f'"{wn}","{wcn}","{wcc}"')
            prev=wn
    #ic(visited.sort(key=field ))
    print(f'\nSorted Result: \n')
    for t in visited:
        print(t)


def test_show_window_info():
    win=open_window()
    print(f'{win=} {window=}')
    mouse_window=get_mouse_over_window()
    print(f'{mouse_window=}')
    show_window_info(mouse_window)
    prev=None
    while True:
        #mouse_window=get_mouse_over_window()
        mouse_window=get_active_window()
        wn,wcn,wcc=get_window_id(mouse_window)
        if prev != wn:
            print(f'\n"{wn=}","{wcn=}","{wcc=}"')
            prev=wn

def main():
    show_pointed_windows()
    #test_show_window_info()

if __name__=='__main__':
    main()
