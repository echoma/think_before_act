#-*- coding: utf-8 -*-
"""
Merge configurations from argument string into configure file.
"""

import logging
import argparse
import os.path
import configparser
import conf.CnfZkSvr
import conf.CnfCommSvr

MODE_MAIN = 'MAIN'
MODE_NAV_BAR = 'NAV_BAR'
MODE_NODE_TREE = 'NODE_TREE'
MODE_NODE_INFO = 'NODE_INFO'
MODE_EDITOR = 'EDITOR'

class Conf(object):
    """
    Conf things
    """
    ini = ''
    mode = MODE_MAIN
    zk_svr = None
    comm_svr = None
    tmux = None

def merge_arg(cmd_arg, ini_arg):
    """
    Merge command line argument and configure file argument.
        The cmd_args has higher priority than ini_arg.
        Only none-empty argument will be considered.
    """
    if isinstance(cmd_arg, (list, tuple)):
        cmd = cmd_arg[0]
        return cmd if cmd else ini_arg
    else:
        return cmd_arg if cmd_arg else ini_arg

def init(args=None):
    """
    Simplest way to initialize the global configuration.
    1. Parse argument string
    2. Load from configure file
    3. Merge
    """
    # parse argument string
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', nargs='?', default='MAIN', \
        choices=['MAIN', 'NAV_BAR', 'NODE_TREE', 'NODE_INFO', 'EDITOR'])
    parser.add_argument('--ini', nargs='+', default=os.getcwd()+'/conf/sample.ini')
    parser.add_argument('--comm-working-dir', nargs='+')
    parser.add_argument('--comm-socket', nargs='+')
    parser.add_argument('--comm-node-data-file', nargs='+')
    parser.add_argument('--zk-server', nargs='+')
    parser.add_argument('--zk-digest', nargs='?')
    parser.add_argument('--tmux-session', nargs='+')
    parser.add_argument('--tmux-window', nargs='+')
    parser.add_argument('--tmux-kill-session', nargs='+', default=[1])
    parser.add_argument('--tmux-zk-cli-cmd', nargs='+')
    obj = parser.parse_args(args)
    Conf.ini = obj.ini
    Conf.mode = obj.mode
    logging.debug('mode = '+mode())
    # load from configure file and merge with argument
    config = configparser.ConfigParser()
    good_ini_list = config.read(obj.ini)
    if len(good_ini_list) == 0:
        logging.error("read %s failed", obj.ini)
        return False
    # zk server config
    zk_server = merge_arg(obj.zk_server, config['zookeeper-server']['server'])
    zk_digest = merge_arg(obj.zk_digest, config['zookeeper-server']['digest'])
    Conf.zk_svr = conf.CnfZkSvr(zk_server, zk_digest)
    # comm server config
    comm_working_dir = merge_arg(obj.comm_working_dir, config['communicate-server']['working_dir'])
    comm_working_dir = os.path.expanduser(comm_working_dir)
    comm_socket = merge_arg(obj.comm_socket, config['communicate-server']['socket'])
    comm_node_data_file = merge_arg(obj.comm_node_data_file, \
        config['communicate-server']['node_data_file'])
    Conf.comm_svr = conf.CnfCommSvr(comm_working_dir, comm_socket, comm_node_data_file)
    # tmux config
    tmux_session = merge_arg(obj.tmux_session, config['tmux']['session_name'])
    tmux_window = merge_arg(obj.tmux_window, config['tmux']['window_name'])
    tmux_kill_session = merge_arg(obj.tmux_kill_session, config['tmux']['kill_session'])
    tmux_kill_session = int(tmux_kill_session)
    tmux_zk_cli_cmd = merge_arg(obj.tmux_zk_cli_cmd, config['tmux']['zk_cli_cmd'])
    Conf.tmux = conf.CnfTmux(tmux_session, tmux_window, tmux_kill_session, tmux_zk_cli_cmd)
    return True

def mode():
    """Return current mode"""
    return Conf.mode

def mode_cmd(mode_str):
    """Return the command for specified mode"""
    return tmux().zk_cli_cmd + ' --mode ' + mode_str + ' --ini ' + Conf.ini\
        + ' --comm-working-dir ' + comm_svr().working_dir + ' --comm-socket ' + comm_svr().socket \
        + ' --comm-node-data-file ' + comm_svr().node_data_file \
        + ' --zk-server ' + zk_svr().server + ' --zk-digest ' + zk_svr().digest \
        + ' --tmux-session ' + tmux().session_name + ' --tmux-window ' + tmux().window_name \
        + ' --tmux-kill-session ' + str(tmux().kill_session) \
        + ' --tmux-zk-cli-cmd ' + tmux().zk_cli_cmd

def zk_svr():
    """Return global zk_svr configuration"""
    return Conf.zk_svr

def comm_svr():
    """Return global comm_svr configuration"""
    return Conf.comm_svr

def tmux():
    """Return global tmux configuration"""
    return Conf.tmux
