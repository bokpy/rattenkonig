#!/usr/bin/env python3
import argparse

from pygments.lexer import default

parser = argparse.ArgumentParser(
prog="pied_piper.py",
description=f'Catches mouse and keyboard input events and then outputs events via an uinput device. '
            f'What output an event sends to the system can be programmed in a configuration file '
            f'per physical mouse device.',

epilog='Peep peep'
	)


parser.add_argument('-l', '--list',
                    help='List mouse devices and other input devices with simular names',
                    action='store_true',
                    )

parser.add_argument('-v', '--verbose',
                    help='Verbose output.',
                    action='store_true'
                    )

parser.add_argument('-c','--configdir',
                    help='directory where the configuration files are.',
                    default='./configs/',
                    nargs='?',
                    action='store'
)
parser.add_argument('-t', '--template',
                    help='create template files in "--configdir" existing files are left alone.',
                    action='store_true'
                    )

parser.add_argument('-w', '--windows',
                    help='Print the window_name, class_name, class_class of the '
                         'windows hovered bij the mouse'
                    ,action='store_true'
                    )
def main():
    args = parser.parse_args()
    print(args)
    pass

if __name__ == '__main__':
    main()