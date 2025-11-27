/*
xqp_wrapper.h
*/

#ifndef XQP_WRAPPER_H
#define XQP_WRAPPER_H

#include <X11/Xlib.h>
#include <X11/Xutil.h>
typedef unsigned long Window;

void _copy_string(void* dest,void* source, int length );
void _clean_copy_string(void* output,void* input) ;
//int xqp_is_this_the_mouse_window(Window);
Window xqp_init();
int xqp_show(Window win);
Window xqp_find_mouse_window();
int xqp_get_name_and_class(Window,char *name,char *class_name, char* class_class);
int xqp_close();

#endif
