#-*- coding: utf-8 -*-
"""
The communication message.
"""

class Message(object):
    """Base class for messages"""
    def __init__(self, cmd):
        self.cmd = cmd

class ReqMsgZkNodeChildren(Message):
    """request for a list of children of a zk node"""
    def __init__(self, node_path, limit=200, offset=0):
        super(self.__class__, self).__init__(self.__class__)
        self.node_path = node_path
        self.limit = limit
        self.offset = offset

class RspMsgZkNodeChildren(Message):
    """response for a list of children of a zk node"""
    def __init__(self, children):
        super(self.__class__, self).__init__(self.__class__.__name__)
        self.children = children
