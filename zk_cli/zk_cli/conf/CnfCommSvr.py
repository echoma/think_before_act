#-*- coding: utf-8 -*-
"""
Configuration for communication server via which all the component process exchange messages.

key arguments:
  working_dir -- all temporary files will put in this directory.
  socket -- the unix socket file name.
  node_data_file -- the file name containing the data of current node when using vim editor.
"""

import collections

CnfCommSvr = collections.namedtuple('CnfCommSvr', ('working_dir', 'socket', 'node_data_file'))
