//#include <X11/Xlib.h>
#include <stdio.h>
#include <string.h>
#include <X11/Xlib.h>
#include <X11/Xatom.h>
#include "xqp_wrapper.h"

//#define PRINTF(...) printf(__VA_ARGS__)
#define PRINTF(...)
#define MAX_STRING_LENGTH 254
#define TRUE 1
#define FALSE 0
//#define __MAIN__

//gcc  -fPIC -o xqp_wrapper xqp_wrapper.c -lX11
//gcc -shared -fPIC -o xqp_wrapper xqp_wrapper.c -lX11 SEGMENTATION FAULT
/*
Badwindow testing
*/
volatile int had_badwindow = 0;

int temp_xerr_handler(Display *dpy, XErrorEvent *e) {
    if (e->error_code == BadWindow) {
        had_badwindow = 1;
        return 0;
    }
    return 0;
}
/*
the global variables initialized by Window xqp_init()
*/
Display *display = NULL;
Window root_window = 0;
XClassHint *x_class_hint_ptr = NULL;
XWindowAttributes win_atr;
XTextProperty xtext_prop;
/*
initialize the globals return's the root_window by success else FALSE
*/
Window xqp_init() {
    //PRINTF("xqp_init\n");
    if (display != NULL) {return root_window;}
    display = XOpenDisplay(NULL);
    if (display == NULL) {
        fprintf(stderr, "XOpenDisplay(NULL) failed,in init_display_window()\n");
        return FALSE;
    }
    int screen = DefaultScreen(display);
    root_window = RootWindow(display, screen);
    x_class_hint_ptr = XAllocClassHint();
    return root_window;
}
/*
return's the window id of the window where the mouse pointer is over,
         or 0 by no success
*/
Window xqp_find_mouse_window() {
    //Window root_win;
    XWindowAttributes attrs;     // used for XGetWindowAttributes(display, win, &attrs)
    Window dummy_parent_win;     // not used
    Window* xqp_kid_windows;     // list of windows to inspect
    unsigned int xqp_kid_count;  // number of children to inspect
    Window dummy_root_win;       // not used
    Window xqp_wanted_kid_win;   // the Window under the mouse pointer when found
    int    dummy_root_x;         // not used
    int    dummy_root_y;         // not used
    int    dummy_win_x;          // not used
    int    dummy_win_y;          // not used
    unsigned int dummy_mask;     // not used
    Window xqp_kid;              // window being tested

    if ( xqp_init() == 0 ) {return FALSE;} // are global variables initalized?
    XQueryTree(display,root_window,&dummy_root_win,&dummy_parent_win,
    &xqp_kid_windows,&xqp_kid_count); // get the chidren of the root window
    PRINTF("xqp_kid_count %i\n",xqp_kid_count);
    if ( xqp_kid_windows == NULL )  {return FALSE;} // no luck return 0
    for (unsigned int i = 0; i < xqp_kid_count;i++) {
        xqp_kid = xqp_kid_windows[i];
	// check if the xqp_kid is ok.
	// to prevent:
	// X Error of failed request:
	// BadWindow (invalid Window parameter)
	//   Major opcode of failed request:  38 (X_QueryPointer)
	had_badwindow = 0; // ChatGpt solution
    int (*old_handler)(Display*, XErrorEvent*) = XSetErrorHandler(temp_xerr_handler);
	XGetWindowAttributes(display,xqp_kid, &attrs);
	XSync(display, False);
    XSetErrorHandler(old_handler);
    if (had_badwindow) {
    return FALSE;
    // window is invalid
    //continue;   // skip this child
    }
        PRINTF("inspect [%i] %lu ",i,xqp_kid);
        if (XQueryPointer(display,xqp_kid,
            &dummy_root_win,&xqp_wanted_kid_win,
            &dummy_root_x,&dummy_root_y,
            &dummy_win_x,&dummy_win_y,
            &dummy_mask)) {
                PRINTF( "XQueryPointer True ");
                if (xqp_wanted_kid_win) { // found and delivered
                     PRINTF( "Found %lu \n",xqp_wanted_kid_win);
                     return xqp_wanted_kid_win;
                     }
            }
         PRINTF("\n");
        }
     return FALSE;
     }
/*
print what XQueryPointer return's for the given window
*/
int xqp_show(Window win) {
    Window root_win;
    Window kid_win;
    int    root_x;
    int    root_y;
    int    win_x;
    int    win_y;
    unsigned int mask;
    int result;
    char s_True[] = "True";
    char s_False[] = "False";
    if ( xqp_init() == 0 ) {return FALSE;} // are global variables initialized?
    result = XQueryPointer(display,win,&root_win,&kid_win,&root_x,&root_y,&win_x,&win_y,&mask);
    printf(
    "%s = XQueryPointer(display,\nwindow=%lu,\nroot_window=%lu,\nchild_window=%lu\nroot_x=%i,\nroot_y=%i,\nwin_x=%i,\nwin_y=%i.\nmask=%u",
    (result)?s_True:s_False,win,root_win,kid_win,root_x,root_y,win_x,win_y,mask);

    return result;
    }

/*
extract: name , res_name, res_class

from X11 struct's
the parameters should point to sufficient memory MAX_STRING_LENGTH
to hold the results
return TRUE on success, FALSE on fail

typedef struct {
	unsigned char *value;	// property data
	Atom encoding;		    // type of property
	int format;		        // 8, 16, or 32
	unsigned long nitems;	// number of items in value

} XTextProperty;
typedef struct {
	char *res_name;
	char *res_class;
} XClassHint;

*/
int xqp_get_name_and_class(
   Window win,char *name,char *class_name, char* class_class) {
   if ( xqp_init() == 0 ) {return FALSE;}
   //XTextProperty xtext_prop;
   name[0]=0;
   class_name[0]=0;
   class_class[0]=0;

   if (XGetWMName(display, win, &xtext_prop)) {
       //_copy_string(name,xtext_prop.value,xtext_prop.nitems);
       _clean_copy_string(name,xtext_prop.value);
      }
   if (XGetClassHint(display, win, x_class_hint_ptr)) {
//      _copy_string(class_name,  x_class_hint_ptr->res_name,sizeof(x_class_hint_ptr->res_name));
//      _copy_string(class_class,x_class_hint_ptr->res_class,sizeof(x_class_hint_ptr->res_class));
      _clean_copy_string(class_name,  x_class_hint_ptr->res_name);
      _clean_copy_string(class_class,x_class_hint_ptr->res_class);

      PRINTF ("       name \"%s\"\n",name);
      PRINTF (" class_name \"%s\"\n",class_name);
      PRINTF ("class_class \"%s\"\n",class_class);
      return TRUE;
      }
   return FALSE;
}

void _copy_string(void* dest,void *source, int length ) {
   if (length >= MAX_STRING_LENGTH ) {
      length = MAX_STRING_LENGTH-1;
      char *d;
      d = (char *) dest;
      d[length]=0;
      }
   memcpy(dest,source,length);
   }

void _clean_copy_string(void* output,void* input) {
    char* out=(char*)output;
    char* inp=(char*)input;
    while (*inp) {
        if (*inp < 0) {
            // Skip the output escape sequence
              inp ++; // Skip non ascii
        } else {
           *(out++) =*(inp++);
        }
    }
   *out = '\0'; // Null-terminate the output string
}

int find_active_window() {
  Window root;
  Atom active_window_atom;
  Window active_window;
    // Get the root window
    root = DefaultRootWindow(display);
    // Get the _NET_ACTIVE_WINDOW atom
    active_window_atom = XInternAtom(display, "_NET_ACTIVE_WINDOW", True);
    // Get the active window
    Atom actual_type;
    int actual_format;
    unsigned long nitems, bytes_after;
    unsigned char *prop = NULL;

    if (XGetWindowProperty(display, root, active_window_atom, 0, 1, False, AnyPropertyType,
                           &actual_type, &actual_format, &nitems, &bytes_after, &prop) == Success) {
        if (nitems != 0) {
            active_window = *(Window *)prop;
            PRINTF("Active window ID: %lu\n", active_window);
	     XFree(prop);
	     return active_window;
        } else {
            PRINTF("No active window found.\n");
	    XFree(prop);
	    return 0;
        }
       
    }

    // Close the display
    //XCloseDisplay(display);
    return 0;
}

/*
close and cleanup
*/
int xqp_close() {
    if (display == 0) {
    return FALSE;
    }
    XFree(x_class_hint_ptr);
    XCloseDisplay(display);
    display = 0 ;
    return TRUE;
}

#ifdef __MAIN__
int main(void) {
      Window win;
      Window  root;
	  Window child;
	  int root_x;
	  int root_y;
	  int win_x;
	  int win_y;
	  unsigned int mask;
	  char name[100];
	  char class_name[100];
      char class_class[100];
win = xqp_find_mouse_window();
if (win) {
    printf ("found (%lu) :\n",win);
    xqp_get_name_and_class(win,name,class_name,class_class);
    printf ("       name \"%s\"\n",name);
    printf (" class_name \"%s\"\n",class_name);
    printf ("class_class \"%s\"\n",class_class);
    }
xqp_close();
};
#endif
