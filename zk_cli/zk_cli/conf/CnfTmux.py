#-*- coding: utf-8 -*-
"""
Configuration for the tmux.

key arguments:
  session_name -- name when we create new tmux session or attach to old session
  window_name -- name of the tmux window
"""

import collections

CnfTmux = collections.namedtuple('CnfTmux', \
  ('session_name', 'window_name', 'kill_session', 'zk_cli_cmd'))
