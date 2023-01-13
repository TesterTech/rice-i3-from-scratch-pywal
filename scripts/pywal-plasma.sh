#!/usr/bin/env bash
# ##
# This piece of code uses a script provided by user fehawen (1) and also the program plasma-theme-switcher (2)
# (1) https://github.com/dylanaraps/pywal/issues/264
#     https://github.com/fehawen
# (2) https://github.com/maldoinc/plasma-theme-switcher
#
# Also was having these issues when opening Dolphin (it was using older version of toolkit not plasma)
# https://www.reddit.com/r/i3wm/comments/ijzb12/dolphin_looks_different_between_kde_and_i3_how_to/

COLOR_SCHEME_DIR="$HOME/.local/share/color-schemes/"
COLOR_SCHEME_NAME="pywal"

[[ -d "$COLOR_SCHEME_DIR" ]] || mkdir -pv "$COLOR_SCHEME_DIR"

query_xresources_rgb_value() {
	hex=$(xrdb -query | grep "$1" | awk '{print $2}' | cut -d# -f2)
	printf "%d,%d,%d\n" "0x${hex:0:2}" "0x${hex:2:2}" "0x${hex:4:2}"
}

output="$(cat << THEME
[ColorEffects:Disabled]
Color=$(query_xresources_rgb_value color9:)

[ColorEffects:Inactive]
Color=$(query_xresources_rgb_value color9:)

[Colors:Button]
BackgroundNormal=$(query_xresources_rgb_value color8:)
ForegroundNormal=$(query_xresources_rgb_value background:)

[Colors:Complementary]

[Colors:Selection]
BackgroundAlternate=
BackgroundNormal=$(query_xresources_rgb_value color2:)
DecorationFocus=
DecorationHover=
ForegroundActive=
ForegroundInactive=
ForegroundLink=
ForegroundNegative=
ForegroundNeutral=
ForegroundNormal=$(query_xresources_rgb_value foreground:)
ForegroundPositive=
ForegroundVisited=

[Colors:Tooltip]
BackgroundAlternate=
BackgroundNormal=$(query_xresources_rgb_value color2:)
DecorationFocus=
DecorationHover=
ForegroundActive=
ForegroundInactive=
ForegroundLink=
ForegroundNegative=
ForegroundNeutral=
ForegroundNormal=$(query_xresources_rgb_value foreground:)
ForegroundPositive=
ForegroundVisited=

[Colors:View]
# BackgroundAlternate=
BackgroundNormal=$(query_xresources_rgb_value color0:)
# DecorationFocus=
# DecorationHover=
# ForegroundActive=
# ForegroundInactive=
# ForegroundLink=
# ForegroundNegative=
# ForegroundNeutral=
ForegroundNormal=$(query_xresources_rgb_value foreground:)
# ForegroundPositive=
# ForegroundVisited=

[Colors:Window]
# BackgroundAlternate=
BackgroundNormal=$(query_xresources_rgb_value color0:)
# DecorationFocus=
# DecorationHover=
# ForegroundActive=
# ForegroundInactive=
# ForegroundLink=
# ForegroundNegative=
# ForegroundNeutral=
ForegroundNormal=$(query_xresources_rgb_value foreground:)
# ForegroundPositive=
# ForegroundVisited=

[General]
ColorScheme=${COLOR_SCHEME_NAME}
Name=${COLOR_SCHEME_NAME}
shadeSortColumn=true

[KDE]
contrast=0

[WM]
activeBackground=$(query_xresources_rgb_value background:)
activeForeground=$(query_xresources_rgb_value foreground:)
inactiveBackground=$(query_xresources_rgb_value background:)
inactiveForeground=$(query_xresources_rgb_value color15:)
THEME
)"

echo "Generated KDE colorscheme ${COLOR_SCHEME_NAME} in folder ${COLOR_SCHEME_DIR}"
printf '%s' "$output" > "${COLOR_SCHEME_DIR}${COLOR_SCHEME_NAME}.colors"

echo Apply the new theme to plasma using plasma-theme script
plasma-theme -c "${COLOR_SCHEME_DIR}${COLOR_SCHEME_NAME}.colors"
