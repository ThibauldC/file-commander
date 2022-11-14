import os
import shutil
import tkinter as tk
from tkinter import ttk
from typing import List


# TODO: sort by file/dir name -> add combobox -> redesign of grid -> add remove and rename button -> add VS code open button -> button for sorting on file/dir name or timestamp created
# TODO: nice to have: make entry/combobox flash red if path does not exist

def set_path_if_dir(e: tk.Event) -> None:
    files, path, list_box = tk.StringVar(), tk.StringVar(), e.widget
    if list_box == msgbox:
        files, path = l_files, first_path
    elif list_box == msgbox2:
        files, path = r_files, second_path

    selection = list_box.curselection()
    new_path = path.get() + '/' + list_box.get(selection[0])[2:]
    if os.path.isdir(new_path):
        path.set(new_path)
        files.set(get_directory_with_icons(path))


def set_path_entry(e: tk.Event) -> None:
    files, path = tk.StringVar(), tk.StringVar()
    if e.widget == first_path_entry:
        files, path = l_files, first_path
    elif e.widget == second_path_entry:
        files, path = r_files, second_path
    files.set(get_directory_with_icons(path))


def attach_icon(path: str, file_or_dir_name: str) -> str:
    full_path = path + "/" + file_or_dir_name
    icon = ""
    if os.path.isdir(full_path):
        icon = u"\U0001F4C2"
    elif os.path.isfile(full_path):
        icon = u"\U0001F4C4"
    return icon + " " + file_or_dir_name


def get_directory_with_icons(path_entered: ttk.Entry) -> List[str]:
    path = path_entered.get()
    return [attach_icon(path, f) for f in os.listdir(path)]


def move_file(direction: str) -> None:
    source_folder, destination_folder, list_box = "", "", None
    if direction == "forward":
        source_folder, destination_folder, list_box = first_path.get(), second_path.get(), msgbox
    elif direction == "backward":
        source_folder, destination_folder, list_box = second_path.get(), first_path.get(), msgbox2
    selection = list_box.curselection()
    source_path = source_folder + '/' + list_box.get(selection[0])[2:]
    shutil.move(source_path, destination_folder)
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
    first_path_entry.bind('<Return>', lambda e: set_path_entry(e))
    second_path_entry.grid(row=0, column=4)
    second_path_entry.bind('<Return>', lambda e: set_path_entry(e))
    msgbox.grid(row=1, column=0, rowspan=2, padx=10)
    msgbox.bind('<Double-1>', lambda e: set_path_if_dir(e))
    tk.ttk.Separator(mainframe, orient="vertical").grid(column=1, row=0, rowspan=3, sticky='ns')
    move_forward_button = tk.ttk.Button(mainframe, text="->", command=lambda: move_file("forward"), width=2)
    move_forward_button.grid(row=1, column=2, padx=10, pady=10)
    move_backward_button = tk.ttk.Button(mainframe, text="<-", command=lambda: move_file("backward"), width=2)
    move_backward_button.grid(row=2, column=2, padx=10, pady=10)
    tk.ttk.Separator(mainframe, orient="vertical").grid(column=3, row=0, rowspan=3, sticky='ns')
    msgbox2.grid(row=1,column=4, rowspan=2, padx=10)
    msgbox2.bind('<Double-1>', lambda e: set_path_if_dir(e))
    msgbox.selection_set(0)
    root.mainloop()
