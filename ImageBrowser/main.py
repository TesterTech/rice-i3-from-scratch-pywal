"""
# Simple GUI experiment. This is just an image browser atm.
# Expects images to be there ar $HOME/Pictures/Wallpapers
# This is a WIP! Tested on openSUSE 15.4 with Python 3.10
# uses tkinter to render the gui.
"""
import os
import subprocess
from tkinter import Button, Label, Tk, Checkbutton, IntVar
from PIL import ImageTk, Image
from helpers.TooltipHelper import Tooltip

TEXT_LABEL_FORWARD = " >> "
TEXT_LABEL_BACK = " << "

HOME = os.path.expanduser("~")
WALLPAPERS_DIR = f"{HOME}/Pictures/Wallpapers/"


def set_current_image_nr(image_nmbr: int):
    """The current image index"""
    global img_no
    img_no = image_nmbr


def prep_move(img_no: int):
    """
    Preparations for moving back or forward an image.
    Set the current image nr.
    Rebuild the grid for displaying the gui elements.
    """
    global image_on_grid
    global button_forward
    global button_back
    global button_exit
    global button_colors
    global checkbox_16_colors
    global button_info

    set_current_image_nr(img_no - 1)
    image_on_grid.grid_forget()
    image_on_grid = Label(
        image=List_of_images[img_no - 1]
    )  # this puts the image on the grid.
    text_label_image_index = Label(text=f"Image {img_no} of {len(List_of_images)}")
    text_label_image_index.grid(row=2, column=0)
    get_grid_configuration(image_on_grid)


def get_grid_configuration(image_on_grid):
    image_on_grid.grid(row=3, column=0, columnspan=6, rowspan=3, padx=20, pady=20)


def forward(image_number: int):
    """
    Code that is executed when the next button is pressed.
    The current image nr is passed into this function.
    Prep move is always prior to doing anything else.
    """
    prep_move(image_number)
    if image_number == 1:
        button_back = Button(root, text=TEXT_LABEL_BACK, state="disabled")
    else:
        button_back = Button(
            root, text=TEXT_LABEL_BACK, command=lambda: back(image_number - 1)
        )
    if image_number == len(List_of_images):
        button_forward = Button(root, text=TEXT_LABEL_FORWARD, state="disabled")
    else:
        button_forward = Button(
            root, text=TEXT_LABEL_FORWARD, command=lambda: forward(image_number + 1)
        )
    place_buttons_in_grid_function(button_back, button_forward)


def back(img_number: int):
    """
    Code that is executed when the Back button is pressed.
    The current image nr is passed into this function.
    Prep move is always prior to doing anything else.
    """
    prep_move(img_number)
    button_forward = Button(
        root, text=TEXT_LABEL_FORWARD, command=lambda: forward(img_number + 1)
    )
    if img_number == 1:
        button_back = Button(root, text=TEXT_LABEL_BACK, state="disabled")
    else:
        button_back = Button(
            root, text=TEXT_LABEL_BACK, command=lambda: back(img_number - 1)
        )
    place_buttons_in_grid_function(button_back, button_forward)


def place_buttons_in_grid_function(button_back, button_forward):
    place_buttons_in_grid(
        button_back, button_exit, button_forward, button_pywal, button_colors, checkbox_16_colors,
        button_info
    )


def run_wal_on_image(img_no: int):
    """
    Run the image through the wal command with some arguments.
    To support 16 colors, a different version is needed, check:
    https://github.com/eylles/pywal16.git
    This version supports the  --cols16 argument.
    A toggle has been built into the GUI to toggle this.
    """
    filename = List_of_original_images[img_no].filename
    print(f'>> Run pywal on {filename} >> {sixteen_colors.get()}')
    if sixteen_colors.get():
        subprocess.run(["../scripts/pywal.sh", f"{filename}", "--cols16"])
    else:
        subprocess.run(["../scripts/pywal.sh", f"{filename}", "-q"])


def place_buttons_in_grid(
        btn_back: Button,
        btn_exit: Button,
        btn_forward: Button,
        btn_pywal: Button,
        btn_colors: Button,
        chk_16_colors: Checkbutton,
        btn_info: Button,
):
    btn_forward.grid(row=1, column=0)
    btn_back.grid(row=1, column=1)
    btn_pywal.grid(row=1, column=2)
    chk_16_colors.grid(row=1, column=3)
    btn_colors.grid(row=1, column=4)
    btn_info.grid(row=1, column=5)
    btn_exit.grid(row=1, column=6)


def add_images_to_list():
    global List_of_images
    global List_of_original_images
    res = []
    for path in os.listdir(WALLPAPERS_DIR):
        if os.path.isfile(os.path.join(WALLPAPERS_DIR, path)):
            if not check_if_svg(path):
                res.append(path)
    List_of_images = []
    List_of_original_images = []
    scale_and_crop_images(List_of_images, List_of_original_images, res)


def check_if_svg(file_name: str) -> bool:
    if file_name.lower().endswith('.svg'):
        return True
    else:
        return False


def scale_and_crop_images(
        list_of_images: list, list_of_original_images: list, res: list
):
    """
    the list of images and list of original images are passed here.
    The loi will contain the scaled and cropped ones.
    The looi will contain as stated.
    """
    for image_name in res:
        image_1 = Image.open(WALLPAPERS_DIR + image_name)
        reduce_factor = determine_scale_factor(image_1)
        low_res_image = ImageTk.PhotoImage(image_1.reduce(reduce_factor))
        low_res_image_1 = ImageTk.getimage(low_res_image)
        low_res_image = low_res_image_1.crop((0, 0, 800, 500))
        list_of_images.append(ImageTk.PhotoImage(low_res_image))
        list_of_original_images.append(image_1)


def determine_scale_factor(image_1: ImageTk) -> int:
    """
    There are various images sizes, the image preview is fixed.
    Dependent on the image size an image is resized by a given amount
    (reduce factor).
    Could probably be solved more elegantly tbh.
    """
    reduce_factor = 2  # default
    if image_1.width <= 1024:
        reduce_factor = 1
    if 1999 < image_1.width < 4080:
        reduce_factor = 4
    if image_1.width >= 4080 or image_1.height > 2999:
        reduce_factor = 6
    return reduce_factor


def create_color_dict(color_string: str) -> dict:
    """A dictionary for the current colors to be stored in"""
    color_dict = {}
    for line in color_string.split("\n"):
        if line.strip() != "":
            key, value = line.split(":")
            color_dict[key.strip()] = value.strip()
    return color_dict


def color_button_grid():
    """This function will place the color buttons in a grid."""
    colors = get_colors_from_xrdb()
    color_blob = colors[1]
    color_dict = create_color_dict(color_blob)
    print(f'>> colordict {color_dict}')

    label_row = 8
    item_num = 1
    column_num = 0
    col_span = 1
    for key, value in color_dict.items():
        if item_num == 7:
            column_num = 1
            label_row = 8
        if item_num == 13:
            column_num = 2
            label_row = 8
        button = Button(root, text=f"{key}", background=f"{value}", pady=10, padx=10)
        button.grid(row=label_row, column=column_num, columnspan=col_span)
        label_row = label_row + 1
        item_num = item_num + 1


def get_colors_from_xrdb() -> tuple:
    """Get the colors values from xrdb"""
    colors = subprocess.getstatusoutput("xrdb -q | grep *.color")
    return colors


def show_windowing_system() -> str:
    """Wayland or X11?"""
    xdg_session_type = subprocess.getoutput("echo $XDG_SESSION_TYPE")
    return xdg_session_type


def show_wallpaper_changer() -> str:
    """
    There are a lot of wallpaper changers.
    This will scan of some known ones.
    Can be useful to check if at least one is installed.
    Also, wallpaper changers depend on a certain display server.
    F.e. on X11 feh can be used and on Wayland swwww can be.
    """
    wall_change_progs = subprocess.getoutput("../scripts/wallpaper_changers.sh")
    return wall_change_progs


def show_sys_info():
    """
    Used for the text hint (Hover) to show some general info like
    the windowing_system and wallpaper_changer.
    """
    sysinfo = (
            f"Display Server: {show_windowing_system()}\n\n"
            f"Wallpaper changers: \n{show_wallpaper_changer()}"
            )
    return sysinfo


if __name__ == "__main__":
    global sixteen_colors
    root = Tk()
    root.tk.call(
        "tk", "scaling", 1.0
    )  # https://www.tcl.tk/man/tcl8.6/TkCmd/tk.html#M10
    root.title("Pywal Image Browser")
    root.geometry("1200x700")
    root.config(bg="lightgrey", pady=20, padx=20)
    sixteen_colors = IntVar()

    add_images_to_list()
    image_on_grid = Label(text="Pywal Image Browser", height=15, width=50)
    get_grid_configuration(image_on_grid)
    button_back = Button(root, text=TEXT_LABEL_BACK, command=back, state="disabled")
    button_exit = Button(root, text="Exit", command=root.quit)
    button_info = Button(root, text="Info")
    Tooltip(button_info, text=show_sys_info(), wraplength=200)
    button_forward = Button(root, text=TEXT_LABEL_FORWARD, command=lambda: forward(1))
    button_pywal = Button(root, text="Pywal", command=lambda: run_wal_on_image(img_no))
    checkbox_16_colors = Checkbutton(root, text='16 colors', variable=sixteen_colors)
    Tooltip(checkbox_16_colors,
            text='*Important*\nOnly works with Pywal (fork) supporting 16 colors!',
            wraplength=200)
    button_colors = Button(root, text="get colors", command=lambda: color_button_grid())
    place_buttons_in_grid(
        button_back, button_exit, button_forward, button_pywal, button_colors, checkbox_16_colors,
        button_info
    )
    root.mainloop()
