#!/usr/bin/env bash

# Color files
POLYBAR_FILE="$HOME/.config/polybar/hack/colors.ini"
ROFI_FILE="$HOME/.config/rofi/colors.rasi"
WAL_FILE="$HOME/.cache/wal/colors.sh"

# Get colors
pywal_get() {
	wal -i "$1" -q -t
}

# Change colors
change_color() {
	# polybar
	sed -i -e "s/foreground = #.*/foreground = $FG/g" $POLYBAR_FILE
	sed -i -e "s/background = #.*/background = $BG/g" $POLYBAR_FILE
	sed -i -e "s/primary = #.*/primary = $AC1/g" $POLYBAR_FILE
	sed -i -e "s/secondary = #.*/secondary = $AC2/g" $POLYBAR_FILE
	sed -i -e "s/background-alt = #.*/background-alt = $AC3/g" $POLYBAR_FILE
	sed -i -e "s/foreground-alt = #.*/foreground-alt = $AC4/g" $POLYBAR_FILE
	sed -i -e "s/foreground-alt2 = #.*/foreground-alt2 = $AC5/g" $POLYBAR_FILE

	# rofi
	cat > $ROFI_FILE <<- EOF
	/* colors */

	* {
	  foreground: ${FG};
	  background: ${BG};
	  primary: ${AC1};
	  secondary: ${AC2};
	  background-alt: ${AC3};
	  foreground-alt: ${AC4};
	  foreground-alt2: ${AC5};
	}
	EOF

	polybar-msg cmd restart
}

set_wallpaper_using_feh() {
    echo Set the wallpaper "$1" using feh
    feh --bg-fill "$1"
}

copy_konsole_colorscheme() {
    echo Copy Konsole colorscheme to 'home local share'
    cp -f $HOME/.cache/wal/colors-konsole.colorscheme $HOME/.local/share/konsole/pywal.colorscheme
}

# Main
if [[ -x "`which wal`" ]]; then
	if [[ "$1" ]]; then
		pywal_get "$1"

		# Source the pywal color file
		if [[ -e "$WAL_FILE" ]]; then
			. "$WAL_FILE"
		else
			echo 'Color file does not exist, exiting...'
            echo '1) Is ImageMagick installed?'
            echo '2) Try to run wal --> f.e. wal -i ~/Pictures/<yourimage>.jpg'
            echo 'should result in ~/.cache/wal dir being filled with files (also the color.sh file)'
			exit 1
		fi

		BG=`printf "%s\n" "$background"`
		FG=`printf "%s\n" "$foreground"`
		AC1=`printf "%s\n" "$color1"`
		AC2=`printf "%s\n" "$color2"`
		AC3=`printf "%s\n" "$color3"`
		AC4=`printf "%s\n" "$color4"`
		AC5=`printf "%s\n" "$color5"`

		change_color
		set_wallpaper_using_feh "$1"
		copy_konsole_colorscheme
	else
		echo -e "[!] Please enter the path to wallpaper. \n"
		echo "Usage : ./pywal.sh path/to/image"
	fi
else
	echo "[!] 'pywal' is not installed. https://pypi.org/project/pywal/"
fi
