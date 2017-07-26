#-*- coding: utf-8 -*-
"""
Error defination
"""

class Error(Exception):
    """Base class for exception in this module"""
    pass

class TmuxError(Error):
    """Raised when tmux operation failed"""
    def __init__(self, msg):
        super(TmuxError, self).__init__()
        self.message = msg
