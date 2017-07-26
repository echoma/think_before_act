#!env python3
#-*- coding: utf-8 -*-
"""
feasibility research No.3 for 'editor'
1. polling the modify time of file
"""

import logging
import os.path
import time

def main():
    """main function"""
    # polling modified time of a file
    file_name = 'test.tmp'
    last_change = os.path.getmtime(file_name)
    while True:
        new_last_change = os.path.getmtime(file_name)
        if new_last_change != last_change:
            last_change = new_last_change
            logging.info('file changed')
        time.sleep(1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    exit(main())
exit(-1)
