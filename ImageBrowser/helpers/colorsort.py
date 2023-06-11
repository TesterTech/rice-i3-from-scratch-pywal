import colorsys


def get_hsv(hexrgb):
    hexrgb = hexrgb.lstrip("#")  # in case you have Web color specs
    r, g, b = (int(hexrgb[i:i + 2], 16) / 255.0 for i in range(0, 5, 2))
    return colorsys.rgb_to_hsv(r, g, b)


color_list = ["#010203",
       "#0c71b4",
       "#4b83b5",
       "#737578",
       "#999089",
       "#7286a1",
       "#8199b2",
       "#808081",
       "#404142",
       "#1097F0",
        "#64AFF2",
        "#9A9CA0",
        "#CDC0B7",
        "#99B3D7",
        "#ACCDEE",
        "#bfbfc0"]  # GBR
color_list.sort(key=get_hsv)
print(color_list)