#-*- coding: utf-8 -*-
"""
The communication client.

Each UI component will has its own comm-client to communicate with the comm-server.
"""

import logging
import socket
import conf

class CommClt(object):
    """Process entry of communication server"""
    def __init__(self):
        self.socket_path_name = conf.comm_svr().working_dir + '/' + conf.comm_svr().socket
        logging.debug("CommClient object created, socket_path_name="+self.socket_path_name)
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    def send(self, data):
        """Send data to server"""
        self.socket.sendto(data, self.socket_path_name)
