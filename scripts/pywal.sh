#!/usr/bin/env bash
# This is a Pywal wrapper script that is shown in TesterTech's YT video's
# Free to use it for your own workflow. No guarantees given on proper operation.
# ~ Script source ~
# https://github.com/TesterTech/rice-i3-from-scratch-pywal
#
# YT: https://www.youtube.com/@testertech
# GH: https://github.com/testertech


# Color files
ROFI_FILE="$HOME/.config/rofi/colors.rasi"
WAL_FILE="$HOME/.cache/wal/colors.sh"
KONSOLE_FILE="$HOME/.local/share/konsole/pywal.colorscheme"
PLASMA_COLORS_DIR="$HOME/.local/share/color-schemes/"
PLASMA_COLORS_FILE="PywalColorScheme.colors"
PLASMA_SHELL_EXECUTABLE="plasmashell"

# Get colors
# standard command for getting pywal
#    -i is path to image
#    -q is quiet mode
#    -t skip changing colors in tty (not sure why this is needed)
#    -n skip setting wallpaper (kde workaropund)
#    --saturate 0.5 fe. would desaturate
#
#    -- other fork of pywal --
#    https://github.com/eylles/pywal16.git
#    This version has  --cols16
#
pywal_get() {
    echo "[func: pywal_get] >> wal -i ${1} ${2}"
	wal -i "$1" "$2" -n -e
    echo "[func: pywal_get] >> still here"
	return 1
}
# Change colors
change_color() {

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
	  foreground-alt3: ${AC6};
	}
	EOF

	#polybar-msg cmd restart
}

set_wallpaper_using_feh() {
	if [ $XDG_SESSION_TYPE == "wayland" ]; then
		echo ">> Set the wallpaper "$1" using swww"
		swww img "$1"
	else
		echo ">> Set the wallpaper "$1" using feh"
		feh --bg-fill "$1"
	fi
}

copy_konsole_colorscheme() {
    echo ">> Copy Konsole colorscheme to 'home local share'"
    cp -f $HOME/.cache/wal/colors-konsole.colorscheme $KONSOLE_FILE
    echo ">> and set transparency to 20%"
    sed -i -e "s/Opacity=.*/Opacity=0.8/g" $KONSOLE_FILE
}
merge_xresources_color() {
    xrdb -merge $HOME/.cache/wal/colors.Xresources
}
get_xres_rgb() {
	hex=$(xrdb -query | grep "$1" | awk '{print $2}' | cut -d# -f2)
	printf "%d,%d,%d\n" "0x${hex:0:2}" "0x${hex:2:2}" "0x${hex:4:2}"
}
plasma_color_scheme() {

	[[ -d "$PLASMA_COLORS_DIR" ]] || mkdir -pv "$PLASMA_COLORS_DIR"

	output="$(cat << THEME
[ColorEffects:Disabled]
Color=$(get_xres_rgb color8:)
ColorAmount=0.15
ColorEffect=0
ContrastAmount=0.250
ContrastEffect=1
IntensityAmount=0
IntensityEffect=1

[ColorEffects:Inactive]
ChangeSelectionColor=false
Color=$(get_xres_rgb color8:)
ColorAmount=0.25
ColorEffect=0
ContrastAmount=0.15
ContrastEffect=1
Enable=false
IntensityAmount=0.20

[Colors:Button]
BackgroundNormal=$(get_xres_rgb background:)
ForegroundNormal=$(get_xres_rgb foreground:)
BackgroundAlternate=80,80,80
DecorationFocus=$(get_xres_rgb color13:)
DecorationHover=$(get_xres_rgb color5:)
ForegroundActive=148,190,201
ForegroundInactive=116,136,174
ForegroundLink=$(get_xres_rgb color5:)
ForegroundNegative=191,8,11
ForegroundNeutral=192,144,0
ForegroundPositive=0,137,43
ForegroundVisited=100,74,155

[Colors:Selection]
BackgroundAlternate=$(get_xres_rgb color6:)
BackgroundNormal=$(get_xres_rgb color6:)
DecorationFocus=180,113,31
DecorationHover=180,113,31
ForegroundActive=132,67,101
ForegroundInactive=255,232,115
ForegroundLink=44,27,0
ForegroundNegative=200,62,76
ForegroundNeutral=$(get_xres_rgb foreground:)
ForegroundNormal=$(get_xres_rgb foreground:)
ForegroundPositive=255,162,0
ForegroundVisited=144,112,140

[Colors:Tooltip]
BackgroundAlternate=186,200,216
BackgroundNormal=192,206,224
DecorationFocus=$(get_xres_rgb color5:)
DecorationHover=$(get_xres_rgb color5:)
ForegroundActive=148,190,201
ForegroundInactive=116,136,174
ForegroundLink=$(get_xres_rgb color5:)
ForegroundNegative=191,3,3
ForegroundNeutral=192,144,0
ForegroundNormal=52,56,61
ForegroundPositive=0,137,43
ForegroundVisited=100,74,155

[Colors:View]
BackgroundAlternate=$(get_xres_rgb color1:)
BackgroundNormal=$(get_xres_rgb color1:)
DecorationFocus=$(get_xres_rgb color5:)
DecorationHover=$(get_xres_rgb color5:)
ForegroundActive=$(get_xres_rgb color14:)
ForegroundInactive=$(get_xres_rgb color12:)
ForegroundLink=$(get_xres_rgb color13:)
ForegroundNegative=$(get_xres_rgb color8:)
ForegroundNeutral=$(get_xres_rgb color15:)
ForegroundNormal=$(get_xres_rgb color15:)
ForegroundPositive=0,137,43
ForegroundVisited=100,74,155

[Colors:Window]
BackgroundAlternate=$(get_xres_rgb color1:)
BackgroundNormal=$(get_xres_rgb color1:)
DecorationFocus=$(get_xres_rgb color5:)
DecorationHover=$(get_xres_rgb color5:)
ForegroundActive=$(get_xres_rgb color14:)
ForegroundInactive=$(get_xres_rgb color12:)
ForegroundLink=$(get_xres_rgb color13:)
ForegroundNegative=$(get_xres_rgb color8:)
ForegroundNeutral=$(get_xres_rgb color15:)
ForegroundNormal=$(get_xres_rgb color15:)
ForegroundPositive=0,137,43
ForegroundVisited=100,74,155

[General]
ColorScheme=Pywal Color Scheme
Name=PywalColorScheme
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground=$(get_xres_rgb background:)
activeBlend=255,255,255
activeForeground=$(get_xres_rgb foreground:)
inactiveBackground=$(get_xres_rgb background:)
inactiveBlend=75,71,67
inactiveForeground=$(get_xres_rgb color15:)
THEME
)"

	printf '%s' "$output" > "${PLASMA_COLORS_DIR}${PLASMA_COLORS_FILE}"
	echo ">> Generated KDE theme: ${PLASMA_COLORS_DIR}${PLASMA_COLORS_FILE}"
	echo ">> Apply using Plasma builtin: plasma-apply-colorscheme  ${PLASMA_COLORS_FILE}"
	plasma-apply-colorscheme BreezeDark # needs to be toggled... so first BreezeDark
	sleep 0.2s
	plasma-apply-colorscheme PywalColorScheme # then the updated one
}

# Main
if [[ -x "`which wal`" ]]; then
	if [[ "$1" ]]; then
		pywal_get "$1" "$2"

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
		AC6=`printf "%s\n" "$color6"`
		AC7=`printf "%s\n" "$color7"`
		AC8=`printf "%s\n" "$color8"`
		AC9=`printf "%s\n" "$color9"`
		AC10=`printf "%s\n" "$color10"`
		AC11=`printf "%s\n" "$color11"`
		AC12=`printf "%s\n" "$color12"`
		AC13=`printf "%s\n" "$color13"`
		AC14=`printf "%s\n" "$color14"`
		AC15=`printf "%s\n" "$color15"`
		AC66=`printf "%s\n" "$color66"`

		change_color
		set_wallpaper_using_feh "$1"
		merge_xresources_color
		if [ -x "`which ${PLASMA_SHELL_EXECUTABLE}`" ];
		then
			echo ">> Plasmashell executable found. "
			plasma_color_scheme
			copy_konsole_colorscheme
		else
			echo "ERROR plasmashell: cannot is NOT installed! Cannot set plasma's (kde) color scheme"
		fi
		sleep 0.1s
		pywalfox update
		$HOME/scripts/waybarstart

	else
		echo -e "[!] Please enter the path to wallpaper. \n"
		echo "Usage : ./pywal.sh path/to/image"
	fi
else
	echo "[!] 'pywal' is not installed. https://pypi.org/project/pywal/"
fi

