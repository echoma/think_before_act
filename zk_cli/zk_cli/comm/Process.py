#-*- coding: utf-8 -*-
"""
The process runing the communication server.

It has two utilities:

1. listening on a unix socket, communicate with other components
2. maintaining a zookeeper client, working as a bridge between other components and zookeeper server
"""

import logging
import multiprocessing
import gevent
import comm.ZkClient
import comm.CommSvr

def comm_gevent_procedure(proc):
    """The procedure entry of comm gevent greenlet."""
    proc.comm.run()

class Process(multiprocessing.Process):
    """Process entry of communication server"""
    def __init__(self):
        multiprocessing.Process.__init__(self)
        logging.debug("CommSvr.Process object created")
        self.zk_client = comm.ZkClient.ZkClient()
        self.comm = comm.CommSvr.CommSvr()
    def run(self):
        logging.debug("CommSvr.Process start running")
        gevent.joinall([
            gevent.spawn(comm_gevent_procedure, self)
        ])
        logging.debug("CommSvr.Process ended")
