#!/usr/bin/env sh
DIR=$HOME/.screenlayout
list=$(ls $DIR)

chosen=$(printf '%s\n' "$list" \
    | rofi -theme-str '@import "~/.config/rofi/screenlayout.rasi"' -dmenu)
# execute the screenlayout script
bash $DIR/$chosen
bash $HOME/scripts/polybarstart
bash $HOME/scripts/setwall.sh
