# Simple GUI experiment. This is just an image browser atm.
# Expects images to be there ar $HOME/Pictures/Wallpapers
# This is a WIP! Tested on openSUSE 15.4 with Python 3.10
import os
from tkinter import *

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


def prep_move(img_no):
    global image_on_grid
    global button_forward
    global button_back
    global button_exit
    image_on_grid.grid_forget()
    image_on_grid = Label(image=List_images[img_no - 1])
    text_label = Label(text=f"Image {img_no} of {len(List_images)}")
    image_on_grid.grid(row=3, column=0, columnspan=3, rowspan=3)
    text_label.grid(row=2, column=0, columnspan=3)


def forward(img_no):
    prep_move(img_no)
    if img_no == 1:
        button_back = Button(root, text=TEXT_LABEL_BACK, state=DISABLED)
    else:
        button_back = Button(root, text=TEXT_LABEL_BACK, command=lambda: back(img_no - 1))
    if img_no == len(List_images):
        button_forward = Button(root, text=TEXT_LABEL_FORWARD, state=DISABLED)
    else:
        button_forward = Button(root, text=TEXT_LABEL_FORWARD,
                                command=lambda: forward(img_no + 1))

    place_buttons_in_grid(button_back, button_exit, button_forward)

def back(img_no):
    prep_move(img_no)
    button_forward = Button(root, text=TEXT_LABEL_FORWARD,
                            command=lambda: forward(img_no + 1))
    if img_no == 1:
        button_back = Button(root, text=TEXT_LABEL_BACK, state=DISABLED)
    else:
        button_back = Button(root, text=TEXT_LABEL_BACK, command=lambda: back(img_no - 1))
    place_buttons_in_grid(button_back, button_exit, button_forward)


def place_buttons_in_grid(button_back, button_exit, button_forward):
    button_browse_files.grid(row=1, column=0, padx=20, pady=20)
    button_forward.grid(row=1, column=1)
    button_back.grid(row=1, column=2)
    button_exit.grid(row=1, column=3, columnspan=2)


root = Tk()
root.tk.call('tk', 'scaling', 1.0)
root.title("Image Viewer")
root.geometry("1000x700")
root.config(bg='lightgrey')

res = []
for path in os.listdir(WALLPAPERS_DIR):
    if os.path.isfile(os.path.join(WALLPAPERS_DIR, path)):
        res.append(path)


List_images = []
for image_name in res:
    image_1 = PIL.ImageTk.getimage(
        ImageTk.PhotoImage(Image.open(WALLPAPERS_DIR + image_name)))
    low_res_img_1 = ImageTk.PhotoImage(image_1.resize((image_1.width // 8, image_1.height // 8)))
    List_images.append(low_res_img_1)

image_on_grid = Label(text='Image Browser Bruh')
image_on_grid.grid(row=3, column=0, columnspan=3, rowspan=3, padx=20, pady=20)

button_back = Button(root, text=TEXT_LABEL_BACK, command=back, state=DISABLED)
button_exit = Button(root, text="Exit", command=root.quit)
button_forward = Button(root, text=TEXT_LABEL_FORWARD, command=lambda: forward(1))
button_browse_files = Button(root, text='Open a File', command=select_file)
place_buttons_in_grid(button_back, button_exit, button_forward)


root.mainloop()
