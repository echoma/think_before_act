# feasibility study

## text ui

* [x] python urwid.
* [x] Treeview support of urwid.

## content editor

* [x] embed a `vim` via python script in a tmux pane.
* [x] (editor_0.py) get the tty device for `ioctl` in python.
* [x] (editor_0.py) if the user quit vim, restart the vim.
* [ ] (**DENIED**, editor_1.py) sending key stroke to `vim` via the `ioctl` syscall in python: need root to do this, bad expierence.
* [x] (editor_2.py, reload.vimrc, auto_autoreload.vim) vim auto reload a changed file. after editing, reload can still work.
* [x] if the user saved content in the vim, notified by this change, and update it to zookeeper.

## multiplexer

* [x] tmux, one component process in each pane.
* [x] (tmux_layout_control.sh) using script to create tmux window and panes, startup each component process, then adjust the panes layout.
* [x] (tmux_layout_control.sh) send key stroke via tmux to vim


## general UI

```text
+------------------------------------------------------------------+
|                                                                  |
|    Navigator Bar: node path, quick jump..etc.                    |
|                                                                  |
+-------------------+----------------------------------------------+
|                   |                                              |
|                   |                                              |
|                   |                                              |
|                   |                                              |
|                   |                                              |
|   Tree view       |          Editor of node content              |
|    of nodes       |                                              |
|                   |                                              |
|                   |                                              |
|                   |                                              |
+-------------------+----------------------------------------------+
|                                                                  |
|     Status Bar: connection, data exchange, node infomation       |
|                                                                  |
+------------------------------------------------------------------+
```