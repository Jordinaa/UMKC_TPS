#!/bin/bash
# this runs tmux and opens up all programs for running the PX4 SITL
# set the session name
SESSION_NAME="PFC"


# start a new tmux session
tmux new-session -d -s $SESSION_NAME

# split the window into panes
tmux split-window -h -t $SESSION_NAME 
tmux split-window -v -t $SESSION_NAME
tmux select-pane -L
tmux split-window -v -t $SESSION_NAME

# run commands in each pane
tmux send-keys -t $SESSION_NAME:0.0 'cd; cd /home/taranto/catkin_ws/src/afrl_ros/afrl_ros/src/; code .' Enter
tmux send-keys -t $SESSION_NAME:0.1 'cd; cd /home/taranto/afrl_waypoint/js/; code .' Enter
tmux send-keys -t $SESSION_NAME:0.2 'cd; cd /home/taranto/catkin_ws/src/afrl_ros/afrl_ros/scripts/flight_card/; code .' Enter 
tmux send-keys -t $SESSION_NAME:0.3 'cd ~' Enter

# open terminal tabs
# Attach to the tmux session
tmux attach-session -t $SESSION_NAME

export SESSION_NAME="PFC"
