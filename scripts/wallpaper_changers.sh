#!/usr/bin/env bash
set -e
# some apps to change wallpapers, there may be more, feel free to add.
APPS=(
  'feh' 'nitrogen' 'pacwall' 'swww' 'hydrapaper' 'wpgtk' 'chwall' 'pacwall' 'azote' 'swaybg' 'xwallpaper'
  )
function checker() {
  which "$app"> /dev/null 2>&1 &&  return 0 || return 1
}
for app in "${APPS[@]}"
do
  if checker "$app" == 0 ; then echo "Found: $app"; else echo "$app [not Installed]"; fi
done

