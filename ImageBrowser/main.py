# Simple GUI experiment. This is just an image browser atm.
# Expects images to be there ar $HOME/Pictures/Wallpapers
# This is a WIP! Tested on openSUSE 15.4 with Python 3.10
# uses tkinter to render the gui.
import os
from tkinter import *
import subprocess

import PIL.ImageTk
from PIL import ImageTk, Image
from tkinter import filedialog as fd

TEXT_LABEL_FORWARD = " >> "
TEXT_LABEL_BACK = " << "

HOME = os.path.expanduser('~')
WALLPAPERS_DIR = f'{HOME}/Pictures/Wallpapers/'


def select_file() -> str:
    filetypes = (
        ('All files', '*.*'),
    )
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir=WALLPAPERS_DIR,
        filetypes=filetypes)
    return filename


def set_current_image_nr(image_nmbr):
    global img_no
    img_no = image_nmbr
    print(f'set the image no {img_no}')


def prep_move(img_no):
    global image_on_grid
    global button_forward
    global button_back
    global button_exit
    set_current_image_nr(img_no - 1)

    image_on_grid.grid_forget()
    image_on_grid = Label(image=List_of_images[img_no - 1])  # this puts the image on the grid.
    text_label = Label(text=f"Image {img_no} of {len(List_of_images)}")
    text_label.grid(row=2, column=0, columnspan=3)
    image_on_grid.grid(row=3, column=0, columnspan=5, rowspan=3, padx=20, pady=20)


def forward(image_number):
    prep_move(image_number)
    if image_number == 1:
        button_back = Button(root, text=TEXT_LABEL_BACK, state=DISABLED)
    else:
        button_back = Button(root, text=TEXT_LABEL_BACK, command=lambda: back(image_number - 1))
    if image_number == len(List_of_images):
        button_forward = Button(root, text=TEXT_LABEL_FORWARD, state=DISABLED)
    else:
        button_forward = Button(root, text=TEXT_LABEL_FORWARD,
                                command=lambda: forward(image_number + 1))
    place_buttons_in_grid(button_back, button_exit, button_forward, button_pywal)


def back(img_number):
    prep_move(img_number)
    button_forward = Button(root, text=TEXT_LABEL_FORWARD,
                            command=lambda: forward(img_number + 1))
    if img_number == 1:
        button_back = Button(root, text=TEXT_LABEL_BACK, state=DISABLED)
    else:
        button_back = Button(root, text=TEXT_LABEL_BACK, command=lambda: back(img_number - 1))
    place_buttons_in_grid(button_back, button_exit, button_forward, button_pywal)


def run_wal_on_image(img_no):
    filename=List_of_original_images[img_no].filename
    print(f'run pywal on image: {filename}')
    subprocess.run([f'{HOME}/scripts/pywal.sh', f'{filename}'])


def place_buttons_in_grid(btn_back, btn_exit, btn_forward, btn_pywal):
    button_browse_files.grid(row=1, column=0, padx=20, pady=20)
    btn_forward.grid(row=1, column=1)
    btn_back.grid(row=1, column=2)
    btn_pywal.grid(row=1, column=3)
    btn_exit.grid(row=1, column=4)


def add_images_to_list():
    global List_of_images
    global List_of_original_images
    res = []
    for path in os.listdir(WALLPAPERS_DIR):
        if os.path.isfile(os.path.join(WALLPAPERS_DIR, path)):
            res.append(path)
    List_of_images = []
    List_of_original_images = []
    for image_name in res:
        reduce_factor = 4  # default
        # image_1 = PIL.ImageTk.getimage(
        #     ImageTk.PhotoImage(Image.open(WALLPAPERS_DIR + image_name)))
        image_1 = Image.open(WALLPAPERS_DIR + image_name)
        if image_1.width > 3999 or image_1.height > 2999:
            reduce_factor = 8
        low_res_image = ImageTk.PhotoImage(image_1.reduce(reduce_factor))
        List_of_original_images.append(image_1)
        List_of_images.append(low_res_image)


if __name__ == "__main__":
    root = Tk()
    root.tk.call('tk', 'scaling', 1.0)
    root.title("Pywal Image Browser")
    root.geometry("1200x700")
    root.config(bg='lightgrey', pady=20, padx=20)

    add_images_to_list()
    image_on_grid = Label(text='Image Browser Bruh', height=15, width=50)
    image_on_grid.grid(row=3, column=0, columnspan=5, rowspan=3, padx=20, pady=20)
    button_back = Button(root, text=TEXT_LABEL_BACK, command=back, state=DISABLED)
    button_exit = Button(root, text="Exit", command=root.quit)
    button_forward = Button(root, text=TEXT_LABEL_FORWARD, command=lambda: forward(1))
    button_browse_files = Button(root, text='Open a File', command=select_file)
    button_pywal = Button(root, text="Pywal", command=lambda: run_wal_on_image(img_no))
    place_buttons_in_grid(button_back, button_exit, button_forward, button_pywal)

    root.mainloop()
