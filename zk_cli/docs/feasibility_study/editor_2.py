#!env python3
#-*- coding: utf-8 -*-
"""
feasibility research No.2 for 'editor'
1. run vim with auto_reload.vimrc which set autoread
2. if any editing saved, reload still works
"""

import logging
import os

def main():
    """main function"""
    # make a new vimrc for testing
    reload_vimrc = "./reload.vimrc"
    # start vim, and reboot vim when user quit
    file_name = 'test.tmp'
    while True:
        os.system('vim -u '+reload_vimrc+' '+file_name)
        answer = input('pricess x to exit, any other key to restart vim: ')
        if answer == 'x':
            break
    return 0

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    exit(main())
exit(-1)
