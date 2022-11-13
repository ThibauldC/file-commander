import os
import shutil
import tkinter as tk
from tkinter import ttk
from typing import List

# TODO:add combobox -> redesign of grid -> add remove button -> add VS code open button


def set_left_path_if_dir():
    selection = msgbox.curselection()
    source_path = first_path.get() + '/' + msgbox.get(selection[0])[2:]
    if os.path.isdir(source_path):
        first_path.set(source_path)
        l_files.set(get_directory_with_icons(first_path))


def set_right_path_if_dir():
    selection = msgbox2.curselection()
    destination_path = second_path.get() + '/' + msgbox2.get(selection[0])[2:]
    if os.path.isdir(destination_path):
        second_path.set(destination_path)
        r_files.set(get_directory_with_icons(second_path))


# TODO: generalize functions on widgets
def set_left_path() -> None:
    l_files.set(get_directory_with_icons(first_path))


def set_right_path() -> None:
    r_files.set(get_directory_with_icons(second_path))


def attach_icon(path: str, file_or_dir_name: str) -> str:
    full_path = path + "/" + file_or_dir_name
    icon = ""
    if os.path.isdir(full_path):
        icon = u"\U0001F4C2"
    elif os.path.isfile(full_path):
        icon = u"\U0001F4C4"
    return icon + " " + file_or_dir_name


# TODO: create dropdown for path -> Combobox
def get_directory_with_icons(path_entered: ttk.Entry) -> List[str]:
    path = path_entered.get()
    return [attach_icon(path, f) for f in os.listdir(path)]


def move_file_backward():
    selection = msgbox2.curselection()
    source_path = second_path.get() + '/' + msgbox2.get(selection[0])[2:]
    destination_path = first_path.get()
    shutil.move(source_path, destination_path)
    l_files.set(get_directory_with_icons(first_path))
    r_files.set(get_directory_with_icons(second_path))


# TODO: merge 2 move methods
def move_file_forward():
    selection = msgbox.curselection()
    source_path = first_path.get() + '/' + msgbox.get(selection[0])[2:]
    destination_path = second_path.get()
    shutil.move(source_path, destination_path)
    l_files.set(get_directory_with_icons(first_path))
    r_files.set(get_directory_with_icons(second_path))


# TODO: add double click event for directories
if __name__ == "__main__":
    root = tk.Tk()
    root.title("file-commander")
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    first_path = tk.StringVar(value="/Users/thibauld.croonenborghs/Desktop/test")
    first_path_entry = ttk.Entry(mainframe, textvariable=first_path, width=30)

    second_path = tk.StringVar(value="/Users/thibauld.croonenborghs/Desktop/test2")
    second_path_entry = ttk.Entry(mainframe, textvariable=second_path, width=30)

    l_files = tk.StringVar(value=get_directory_with_icons(first_path))
    r_files = tk.StringVar(value=get_directory_with_icons(second_path))

    msgbox = tk.Listbox(mainframe, listvariable=l_files, background="white", width=30, height=40)
    msgbox2 = tk.Listbox(mainframe, listvariable=r_files, background="white", width=30, height=40)
    msgbox.focus()

    first_path_entry.grid(row=0, column=0)
    first_path_entry.bind('<Return>', lambda e: set_left_path())
    second_path_entry.grid(row=0, column=4)
    second_path_entry.bind('<Return>', lambda e: set_right_path())
    msgbox.grid(row=1, column=0, rowspan=2, padx=10)
    msgbox.bind('<Double-1>', lambda e: set_left_path_if_dir())
    tk.ttk.Separator(mainframe, orient="vertical").grid(column=1, row=0, rowspan=3, sticky='ns')
    move_forward_button = tk.ttk.Button(mainframe, text="->", command=move_file_forward, width=2)
    move_forward_button.grid(row=1, column=2, padx=10, pady=10)
    move_backward_button = tk.ttk.Button(mainframe, text="<-", command=move_file_backward, width=2)
    move_backward_button.grid(row=2, column=2, padx=10, pady=10)
    tk.ttk.Separator(mainframe, orient="vertical").grid(column=3, row=0, rowspan=3, sticky='ns')
    msgbox2.grid(row=1,column=4, rowspan=2, padx=10)
    msgbox2.bind('<Double-1>', lambda e: set_right_path_if_dir())
    msgbox.selection_set(0)
    root.mainloop()
