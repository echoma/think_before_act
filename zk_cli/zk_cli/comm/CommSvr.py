#-*- coding: utf-8 -*-
"""
The communication server.

The MAIN mode will fork a subprocess and running this server.
"""

import logging
import os
import os.path
import socket
import conf

class CommSvr(object):
    """Process entry of communication server"""
    def __init__(self):
        self.socket_path_name = conf.comm_svr().working_dir + '/' + conf.comm_svr().socket
        logging.debug("CommSvr object created, socket_path_name="+self.socket_path_name)
        if not os.path.exists(conf.comm_svr().working_dir):
            os.makedirs(conf.comm_svr().working_dir)
        if os.path.exists(self.socket_path_name):
            os.remove(self.socket_path_name)
        self.server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server_socket.bind(self.socket_path_name)
    def run(self):
        """Start message processing"""
        while True:
            barr, addr = self.server_socket.recvfrom(409600)
            logging.debug(str(barr) + ' @ ' + str(addr))
