#!env python3
#-*- coding: utf-8 -*-
"""
feasibility research No.0 for 'editor'
1. get current tty device path and write this path to a file.
2. execute vim to editor this file, restart if user exit vim
"""

import logging
import os
import sys

def main():
    """main function"""
    # get tty path name, write to a file
    file_name = 'test.tmp'
    file_obj = open(file_name, 'w')
    tty_name = os.ttyname(sys.stdout.fileno())
    file_obj.write(tty_name)
    file_obj.close()
    logging.info("tty name is %s", tty_name)
    # start vim, and reboot vim when user quit
    while True:
        os.system('vim '+file_name)
        answer = input('pricess x to exit, any other key to restart vim: ')
        if answer == 'x':
            break
    return 0

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    exit(main())
exit(-1)
