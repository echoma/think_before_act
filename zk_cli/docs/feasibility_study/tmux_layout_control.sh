#!/bin/sh
#-*- coding: utf-8 -*-

tmux new -d -s STUDY

# tmux new-window -t STUDY:0 -n 'try_layout'

tmux split-window -h -p 70 ./editor_0.py

tmux send-keys -t STUDY:0.1 ':w' ENTER

tmux attach -t STUDY