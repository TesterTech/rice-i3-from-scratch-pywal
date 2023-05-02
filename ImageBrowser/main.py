"""
A simple image browser GUI. With the option of running
Pywal on an image and showing the xrdb colors.
Expects images to be there at $HOME/Pictures/Wallpapers
directory. This is a WIP! Tested on openSUSE 15.4,
Fedora 38 with Python 3.10 should work on most distro's.
Uses tkinter to render the GUI. Uses pillow for image parsing.
Subprocess is used to run shell scripts.
source: https://github.com/TesterTech
"""
import os
import subprocess
from tkinter import Button, Label, Tk
from PIL import ImageTk, Image

TEXT_LABEL_FORWARD = " >> "
TEXT_LABEL_BACK = " << "
HOME = os.path.expanduser("~")
WALLPAPERS_DIR = f"{HOME}/Pictures/Wallpapers/"
PYWAL_SCRIPT_LOCATION = f"{HOME}/scripts/pywal.sh"
THUMB_CROP_SIZE = (0, 0, 200, 125)
PREVIEW_CROP_SIZE = (0, 0, 800, 500)
img_no = 0
List_of_images = []
List_of_thumbnail_images = []
List_of_original_images = []


def set_current_image_nr(image_nmbr: int):
    global img_no
    img_no = image_nmbr


def prep_move(img_no: int):
    """
    This function is run before move to next or previous image.
    It puts puts some elements on the grid like buttons and image labels.
    """
    global selected_image
    global button_forward
    global button_back
    global button_exit
    global button_colors

    set_current_image_nr(img_no - 1)
    image_x_of_y_label = Label(text=f"Image {img_no} of {len(List_of_images)}")
    selected_image.grid_forget()
    selected_image = Label(
        image=List_of_images[img_no - 1]
    )  # this puts the image on the grid.
    next_image = Label(image=List_of_thumbnail_images[img_no])
    previous_image = Label(image=List_of_thumbnail_images[img_no - 2])
    image_x_of_y_label.grid(row=2, column=0)
    previous_image.grid(row=3, column=0, columnspan=4, rowspan=1, padx=20, pady=20)
    selected_image.grid(row=4, column=0, columnspan=4, rowspan=1, padx=20, pady=20)
    next_image.grid(row=5, column=0, columnspan=4, rowspan=1, padx=20, pady=20)


def forward(image_number: int):
    """forward button, pass the image number as argument"""
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
    """back button, pass the image number as argument"""
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
    """run the pywal script on the image
    :parameter img_no will get the image at index from the List of images
    """
    filename = List_of_original_images[img_no].filename
    subprocess.run([PYWAL_SCRIPT_LOCATION, f"{filename}"])


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
    btn_colors.grid(row=1, column=3)
    btn_exit.grid(row=1, column=5)


def add_images_to_list():
    global List_of_images
    global List_of_thumbnail_images
    global List_of_original_images
    res = []
    for path in os.listdir(WALLPAPERS_DIR):
        if os.path.isfile(os.path.join(WALLPAPERS_DIR, path)):
            if not check_if_svg(path):
                res.append(path)
    scale_and_crop_images(
        List_of_images, List_of_original_images, List_of_thumbnail_images, res
    )


def check_if_svg(file_name: str) -> bool:
    return bool(file_name.lower().endswith((".svg")))


def scale_and_crop_images(
    list_of_preview_images: list,
    list_of_original_images: list,
    list_of_thumbnail_images: list,
    res: list,
):
    for image_name in res:
        # print(f'found {image_name} in wall dir. ')
        image_from_disk = Image.open(WALLPAPERS_DIR + image_name)
        reduce_factor = determine_scale_factor(image_from_disk)
        preview_image = reduce_photoimage(image_from_disk, reduce_factor)
        thumbnail_image = reduce_photoimage(image_from_disk, reduce_factor * 4)

        preview_image = crop_image(preview_image, PREVIEW_CROP_SIZE)
        thumbnail_image = crop_image(thumbnail_image, THUMB_CROP_SIZE)

        list_of_original_images.append(image_from_disk)
        list_of_preview_images.append(ImageTk.PhotoImage(preview_image))
        list_of_thumbnail_images.append(ImageTk.PhotoImage(thumbnail_image))


def crop_image(_preview_image, preview_crop_size: tuple) -> ImageTk.PhotoImage:
    tmp_image_1 = ImageTk.getimage(_preview_image)
    return tmp_image_1.crop(preview_crop_size)


def reduce_photoimage(image_from_disk, reduce_factor):
    preview_image = ImageTk.PhotoImage(image_from_disk.reduce(reduce_factor))
    return preview_image


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
    selected_image = Label(text="Pywal Image Browser", height=15, width=50)
    selected_image.grid(row=3, column=0, columnspan=5, rowspan=3, padx=20, pady=20)
    button_forward = Button(root, text=TEXT_LABEL_FORWARD, command=lambda: forward(1))
    button_back = Button(root, text=TEXT_LABEL_BACK, command=back, state="disabled")
    button_pywal = Button(root, text="Pywal", command=lambda: run_wal_on_image(img_no))
    button_colors = Button(root, text="get colors", command=lambda: color_button_grid())
    button_exit = Button(root, text="Exit", command=root.quit)
    place_buttons_in_grid(
        button_back, button_exit, button_forward, button_pywal, button_colors
    )

    root.mainloop()
