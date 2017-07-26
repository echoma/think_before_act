#-*- coding: utf-8 -*-
"""
Configuration for the zookeeper server which we will connect to.

key arguments:
  server -- the ip:port of zookeeper server
  digest -- user and password digest for logon to the server
"""

import collections

CnfZkSvr = collections.namedtuple('CnfZkSvr', ('server', 'digest'))
