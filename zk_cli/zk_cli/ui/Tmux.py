#-*- coding: utf-8 -*-
"""
Use tmux as the multiplexer.

It has two utilities:

1. As a terminal multiplexer, start all the ui component process and do the UI-layout work.
2. Send key stroke to ui component when IPC needed.
"""

import logging
import os
import time
import sys
import conf
import error

class Tmux(object):
    """The tmux controller"""

    __ERR_EXIT = 256

    def __init__(self):
        self.pane_name_nave_bar = None
        self.pane_name_node_tree = None
        self.pane_name_node_info = None
        self.pane_name_editor = None
    def run_tmux_cmd(self, cmd):
        """call tmux command"""
        logging.debug(cmd)
        return os.system('tmux ' + cmd)
    def run_shell_cmd_in_pane(self, pane, cmd):
        """input command into pane, and press Enter"""
        return self.run_tmux_cmd('send-keys -t ' + pane + ' \'' + cmd + '\' ENTER')
    def start(self):
        """Startup"""
        logging.debug('ui.Tmux starting')
        ses_name = conf.tmux().session_name
        win_name = conf.tmux().window_name
        ses_win_name = ses_name + ':' + win_name
        self.pane_name_nave_bar = ses_name + ':0.0'
        self.pane_name_node_tree = ses_name + ':0.1'
        self.pane_name_node_info = ses_name + ':0.2'
        self.pane_name_editor = ses_name + ':0.3'
        # ensure the existance of tmux session
        session_is_new = False
        if conf.tmux().kill_session:
            self.run_tmux_cmd('kill-session -t ' + ses_name)
        has_session = self.run_tmux_cmd('has -t ' + ses_name)
        if has_session == Tmux.__ERR_EXIT:
            logging.debug('creating tmux session')
            session_is_new = True
            self.run_tmux_cmd('new -d -s ' + ses_name)
        has_session = self.run_tmux_cmd('has -t ' + ses_name)
        if has_session == Tmux.__ERR_EXIT:
            raise error.TmuxError("tmux session create failed, name="+ses_name)
        time.sleep(1) # wait for tmux booting up
        # ensure the existance of tmux window
        if not session_is_new:
            logging.debug('active tmux window')
            self.run_tmux_cmd('selectw -t ' + ses_win_name)
            return
        else:
            logging.debug('initialize the tmux window panes')
        # split the current window, generate win.1 as node tree component
        time.sleep(0.1)
        pane0_name = ses_name + ':0.0'
        self.run_tmux_cmd('splitw -t ' + pane0_name + ' -v -p 80 ')
        # split the win.1, generate win.2 as node info component
        time.sleep(0.1)
        pane1_name = ses_name + ':0.1'
        self.run_tmux_cmd('splitw -t ' + pane1_name + ' -h -p 70 ')
        # split the win.2, generate win.3 as editor component
        time.sleep(0.1)
        pane2_name = ses_name + ':0.2'
        self.run_tmux_cmd('splitw -t ' + pane2_name + ' -v -p 80 ')
        # start UI component process in corresponding pane
        time.sleep(0.1)
        cmd = conf.mode_cmd(conf.MODE_NAV_BAR)
        self.run_shell_cmd_in_pane(self.pane_name_nave_bar, cmd)
        cmd = conf.mode_cmd(conf.MODE_NODE_TREE)
        self.run_shell_cmd_in_pane(self.pane_name_node_tree, cmd)
        cmd = conf.mode_cmd(conf.MODE_NODE_INFO)
        self.run_shell_cmd_in_pane(self.pane_name_node_info, cmd)
        cmd = conf.mode_cmd(conf.MODE_EDITOR)
        self.run_shell_cmd_in_pane(self.pane_name_editor, cmd)
        # if session is new created, name the window
        time.sleep(0.1)
        logging.debug('rename tmux window of the new session: '+ses_name)
        self.run_tmux_cmd('renamew -t ' + ses_name + ':0 ' + win_name)
