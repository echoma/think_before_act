#-*- coding: utf-8 -*-
"""
A zookeeper client using kazoo
"""

import logging
from kazoo.client import KazooClient
import conf

class ZkClient(object):
    """The client"""
    def __init__(self):
        self._clt = KazooClient(hosts=conf.zk_svr().server)
        self._clt.start()
        logging.debug("ZkClient started")
