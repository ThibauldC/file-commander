import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter.simpledialog import askstring
from typing import List


# TODO: add make directory functionality -> add move folder functionality -> add VS code open button -> button for sorting on file/dir name or timestamp created
# TODO: nice to have: make combobox flash red if path does not exist
# TODO: refactor GUI into class

def populate_combo(path: str) -> List[str]:
    all_dirs_up = []
    start = path
    for _ in range(4):
        dir_up = os.path.dirname(start)
        if dir_up == "/":
            break
        all_dirs_up.append(dir_up)
        start = dir_up
    return all_dirs_up


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
    return sorted([attach_icon(path, f) for f in os.listdir(path)])


def rename_file() -> None:
    files, path = tk.StringVar(), tk.StringVar()
    list_box = [box for box in [msgbox, msgbox2] if len(box.curselection()) > 0][0]
    if list_box == msgbox:
       files, path = l_files, first_path_combo
    elif list_box == msgbox2:
       files, path = r_files, second_path_combo
    old_path = path.get() + "/" + list_box.get(list_box.curselection()[0])[2:]
    new_name = askstring("Rename", "New file/directory name?")
    new_path = path.get() + "/" + new_name
    os.rename(old_path, new_path)
    files.set(get_directory_with_icons(path))


def create_file() -> None:
    list_box = [box for box in [msgbox, msgbox2] if len(box.curselection()) > 0][0]
    if list_box == msgbox:
       files, path = l_files, first_path_combo
    else:
       files, path = r_files, second_path_combo
    file_name = askstring("New file", "Enter file name")
    new_file_path = path.get() + "/" + file_name
    if not os.path.exists(new_file_path):
        with open(new_file_path, "w"):
            pass
    files.set(get_directory_with_icons(path))


def remove_file() -> None:
    files, path = tk.StringVar(), tk.StringVar()
    list_box = [box for box in [msgbox, msgbox2] if len(box.curselection()) > 0][0]
    if list_box == msgbox:
       files, path = l_files, first_path_combo
    elif list_box == msgbox2:
       files, path = r_files, second_path_combo
    path_to_remove = path.get() + "/" + list_box.get(list_box.curselection()[0])[2:]
    if os.path.isdir(path_to_remove):
        os.rmdir(path_to_remove)
    else:
        os.remove(path_to_remove)
    files.set(get_directory_with_icons(path))


def set_path_if_dir(e: tk.Event) -> None:
    files, path, list_box = tk.StringVar(), tk.StringVar(), e.widget
    if list_box == msgbox:
        files, path = l_files, first_path_combo
    elif list_box == msgbox2:
        files, path = r_files, second_path_combo

    selection = list_box.curselection()
    new_path = path.get() + '/' + list_box.get(selection[0])[2:]
    if os.path.isdir(new_path):
        path.set(new_path)
        files.set(get_directory_with_icons(path))
        path["values"] = populate_combo(path.get())


def set_path_entry(e: tk.Event) -> None:
    files = tk.StringVar()
    if e.widget == first_path_combo:
        files = l_files
    elif e.widget == second_path_combo:
        files = r_files
    files.set(get_directory_with_icons(e.widget))
    e.widget["values"] = populate_combo(e.widget.get())


def move_file(direction: str) -> None:
    source_folder, destination_folder, list_box = "", "", None
    if direction == "forward":
        source_folder, destination_folder, list_box = first_path_combo.get(), second_path_combo.get(), msgbox
    elif direction == "backward":
        source_folder, destination_folder, list_box = second_path_combo.get(), first_path_combo.get(), msgbox2
    selection = list_box.curselection()
    source_path = source_folder + '/' + list_box.get(selection[0])[2:]
    if not os.path.exists(destination_folder + "/" + list_box.get(selection[0])[2:]):
        shutil.move(source_path, destination_folder)
        l_files.set(get_directory_with_icons(first_path_combo))
        r_files.set(get_directory_with_icons(second_path_combo))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("file-commander")
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    first_path = tk.StringVar(value="/Users/thibauld.croonenborghs/Desktop/test")
    second_path = tk.StringVar(value="/Users/thibauld.croonenborghs/Desktop/test2")

    l_files = tk.StringVar(value=get_directory_with_icons(first_path))
    r_files = tk.StringVar(value=get_directory_with_icons(second_path))

    msgbox = tk.Listbox(mainframe, listvariable=l_files, background="white", width=30, height=40)
    msgbox2 = tk.Listbox(mainframe, listvariable=r_files, background="white", width=30, height=40)
    msgbox.focus()

    rename_button = tk.ttk.Button(mainframe, text="Rename", command=lambda: rename_file(), width=6)
    rename_button.grid(row=0, column=0, padx=5, pady=5)
    make_file_button = tk.ttk.Button(mainframe, text="touch", command=lambda: create_file(), width=6)
    make_file_button.grid(row=0, column=1, padx=5, pady=5)
    remove_button = tk.ttk.Button(mainframe, text="X", command=lambda: remove_file(), width=2)
    remove_button.grid(row=0, column=2, padx=5, pady=5)
    make_dir_button = tk.ttk.Button(mainframe, text="mkdir", command=lambda: print("make dir"), width=6)
    make_dir_button.grid(row=0, column=3, padx=5, pady=5)
    vs_code_button = tk.ttk.Button(mainframe, text="VS code", command=lambda: print("Open in VS code"), width=8)
    vs_code_button.grid(row=0, column=4, padx=5, pady=5)

    move_backward_button = tk.ttk.Button(mainframe, text="<-", command=lambda: move_file("backward"), width=2)
    move_backward_button.grid(row=1, column=1, padx=5, pady=5)
    move_forward_button = tk.ttk.Button(mainframe, text="->", command=lambda: move_file("forward"), width=2)
    move_forward_button.grid(row=1, column=3, padx=5, pady=5)

    first_path_combo = ttk.Combobox(mainframe, textvariable=first_path, width=30)
    first_path_combo["values"] = populate_combo(str(first_path))
    first_path_combo.grid(row=2, column=0, columnspan=2, pady=10)
    first_path_combo.bind('<Return>', lambda e: set_path_entry(e))
    first_path_combo.bind('<<ComboboxSelected>>', lambda e: set_path_entry(e))

    second_path_combo = ttk.Combobox(mainframe, textvariable=second_path, width=30)
    second_path_combo["values"] = populate_combo(str(second_path))
    second_path_combo.grid(row=2, column=3, columnspan=2, pady=10)
    second_path_combo.bind('<Return>', lambda e: set_path_entry(e))
    second_path_combo.bind('<<ComboboxSelected>>', lambda e: set_path_entry(e))


    msgbox.grid(row=3, column=0, rowspan=2, columnspan=2, padx=10)
    msgbox.bind('<Double-1>', lambda e: set_path_if_dir(e))

    tk.ttk.Separator(mainframe, orient="vertical").grid(column=2, row=3, rowspan=3, sticky='ns')

    msgbox2.grid(row=3, column=3, rowspan=2, columnspan=2, padx=10)
    msgbox2.bind('<Double-1>', lambda e: set_path_if_dir(e))
    msgbox.selection_set(0)

    root.mainloop()
