#!/bin/bash

# Ensure other individual backup scripts run correctly
bash "$(dirname "$0")/ensure_bashrc_backuped.sh"
bash "$(dirname "$0")/ensure_zshrc_backuped.sh"
bash "$(dirname "$0")/ensure_tmux_config_backuped.sh"
