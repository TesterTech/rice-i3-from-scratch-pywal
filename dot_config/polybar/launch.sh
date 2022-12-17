#!/usr/bin/env bash

dir="$HOME/.config/polybar"
themes=(`ls --hide="launch.sh" $dir`)

killall -q polybar
while pgrep -u $UID -x polybar >/dev/null; do sleep 1; done

echo launch polybar with theme $1

if [[ "$1" == "--hack" ]]; then
    echo go into HACK as theme
    polybar -r -q top -c "$dir/hack/config.ini" &
    polybar -r -q bottom -c "$dir/hack/config.ini" &

else
	cat <<- EOF
	Usage : launch.sh --theme
		
	Available Themes :
	--hack    
	EOF
fi
