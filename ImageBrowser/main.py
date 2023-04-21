# Simple GUI experiment. This is just an image browser atm.
# Expects images to be there ar $HOME/Pictures/Wallpapers
# This is a WIP! Tested on openSUSE 15.4 with Python 3.10
# uses tkinter to render the gui.
import os
import subprocess
from tkinter import Button, Label, Tk

from PIL import ImageTk, Image

TEXT_LABEL_FORWARD = " >> "
TEXT_LABEL_BACK = " << "

HOME = os.path.expanduser("~")
WALLPAPERS_DIR = f"{HOME}/Pictures/Wallpapers/"


def set_current_image_nr(image_nmbr: int):
    global img_no
    img_no = image_nmbr


def prep_move(img_no: int):
    global image_on_grid
    global button_forward
    global button_back
    global button_exit
    global button_colors

    set_current_image_nr(img_no - 1)
    image_on_grid.grid_forget()
    image_on_grid = Label(
        image=List_of_images[img_no - 1]
    )  # this puts the image on the grid.
    text_label = Label(text=f"Image {img_no} of {len(List_of_images)}")
    text_label.grid(row=2, column=0)
    image_on_grid.grid(row=3, column=0, columnspan=5, rowspan=3, padx=20, pady=20)


def forward(image_number: int):
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
    place_buttons_in_grid(
        button_back, button_exit, button_forward, button_pywal, button_colors
    )


def back(img_number: int):
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
    place_buttons_in_grid(
        button_back, button_exit, button_forward, button_pywal, button_colors
    )


def run_wal_on_image(img_no: int):
    filename = List_of_original_images[img_no].filename
    subprocess.run([f"{HOME}/scripts/pywal.sh", f"{filename}"])


def place_buttons_in_grid(
    btn_back: Button,
    btn_exit: Button,
    btn_forward: Button,
    btn_pywal: Button,
    btn_colors: Button,
):
    btn_forward.grid(row=1, column=0)
    btn_back.grid(row=1, column=1)
    btn_pywal.grid(row=1, column=2)
    btn_exit.grid(row=1, column=3)
    btn_colors.grid(row=1, column=4)


def add_images_to_list():
    global List_of_images
    global List_of_original_images
    res = []
    for path in os.listdir(WALLPAPERS_DIR):
        if os.path.isfile(os.path.join(WALLPAPERS_DIR, path)):
            res.append(path)
    List_of_images = []
    List_of_original_images = []
    scale_and_crop_images(List_of_images, List_of_original_images, res)


def scale_and_crop_images(
    List_of_images: list, List_of_original_images: list, res: list
):
    for image_name in res:
        # print(f'found {image_name} in wall dir. ')
        image_1 = Image.open(WALLPAPERS_DIR + image_name)
        reduce_factor = determine_scale_factor(image_1)
        low_res_image = ImageTk.PhotoImage(image_1.reduce(reduce_factor))
        low_res_image_1 = ImageTk.getimage(low_res_image)
        low_res_image = low_res_image_1.crop((0, 0, 800, 500))
        List_of_images.append(ImageTk.PhotoImage(low_res_image))
        List_of_original_images.append(image_1)


def determine_scale_factor(image_1: ImageTk) -> int:
    reduce_factor = 2  # default
    if image_1.width <= 1024:
        reduce_factor = 1
    if 1999 < image_1.width < 4080:
        reduce_factor = 4
    if image_1.width >= 4080 or image_1.height > 2999:
        reduce_factor = 6
    return reduce_factor


def create_color_dict(color_string: str) -> dict:
    color_dict = {}
    for line in color_string.split("\n"):
        if line.strip() != "":
            key, value = line.split(":")
            color_dict[key.strip()] = value.strip()
    return color_dict


def color_button_grid():
    colors = get_colors_from_xrdb()
    color_blob = colors[1]
    color_dict = create_color_dict(color_blob)
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
    colors = subprocess.getstatusoutput("xrdb -q | grep *.color")
    return colors


if __name__ == "__main__":
    root = Tk()
    root.tk.call(
        "tk", "scaling", 2.0
    )  # https://www.tcl.tk/man/tcl8.6/TkCmd/tk.html#M10
    root.title("Pywal Image Browser")
    root.geometry("1200x700")
    root.config(bg="lightgrey", pady=20, padx=20)

    add_images_to_list()
    image_on_grid = Label(text="Pywal Image Browser", height=15, width=50)
    image_on_grid.grid(row=3, column=0, columnspan=5, rowspan=3, padx=20, pady=20)
    button_back = Button(root, text=TEXT_LABEL_BACK, command=back, state="disabled")
    button_exit = Button(root, text="Exit", command=root.quit)
    button_forward = Button(root, text=TEXT_LABEL_FORWARD, command=lambda: forward(1))
    button_pywal = Button(root, text="Pywal", command=lambda: run_wal_on_image(img_no))
    button_colors = Button(root, text="get colors", command=lambda: color_button_grid())
    place_buttons_in_grid(
        button_back, button_exit, button_forward, button_pywal, button_colors
    )

    root.mainloop()
