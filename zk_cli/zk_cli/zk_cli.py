#!env python3
"""
under dev
"""

import logging
import conf
import comm
import ui
import error

def main():
    """The main entry"""
    if not conf.init():
        return -1
    logging.debug(conf.zk_svr())
    logging.debug(conf.comm_svr())
    logging.debug(conf.tmux())

    if conf.mode() == conf.MODE_MAIN:
        proc = comm.Process()
        proc.start()
        try:
            tmux = ui.Tmux()
            tmux.start()
        except error.TmuxError as err:
            logging.error(err.message)
            proc.terminate()
        return 0
    elif conf.mode() == conf.MODE_NODE_TREE:
        node_tree = ui.NodeTree()
        node_tree.run()
    else:
        import os
        os.system('echo '+conf.mode())
    return 0

logging.basicConfig(level=logging.DEBUG, \
    format='[%(asctime)s](%(levelname)s): %(message)s (%(funcName)s()@%(filename)s:%(lineno)d)')

if __name__ == '__main__':
    exit(main())
