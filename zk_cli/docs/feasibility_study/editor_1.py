#!env python3
#-*- coding: utf-8 -*-
"""
feasibility research No.1 for 'editor'
1. read tty name from file, and open tty device
2. simulate key stroke via tty device to exit vim
"""

import logging
import fcntl
import termios

def main():
    """main function"""
    # read tty name from file and open the tty device
    file_name = 'test.tmp'
    file_obj = open(file_name, 'r')
    tty_name = file_obj.readline()
    if len(tty_name) <= 0:
        logging.error("empty tty name")
        return -1
    file_obj.close()
    logging.info('tty name is %s', tty_name)
    device = open(tty_name, 'w')
    # write vim command to tty device
    device_fd = device.fileno()
    cmd = ':q!\n'
    for char in cmd:
        fcntl.ioctl(device_fd, termios.TIOCSTI, char)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    exit(main())
exit(-1)
