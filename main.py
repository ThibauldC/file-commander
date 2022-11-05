import os
import shutil
import tkinter as tk
from tkinter import ttk


def print_current_option():
    selection = msgbox.curselection()
    print(msgbox.get(selection[0]))

# TODO: implement move_file_backward
def move_file_forward():
    selection = msgbox.curselection()
    source_path = first_path.get() + '/' + msgbox.get(selection[0])
    destination_path = second_path.get()
    shutil.move(source_path, destination_path)
    l_files.set(os.listdir(first_path.get()))
    r_files.set(os.listdir(second_path.get()))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("File-commander")
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    first_path = tk.StringVar()
    first_path_entry = ttk.Entry(mainframe, textvariable=first_path, width=30)

    second_path = tk.StringVar()
    second_path_entry = ttk.Entry(mainframe, textvariable=second_path, width=30)

    first_path_entry.insert(0, "/Users/thibauld.croonenborghs/Desktop/test")
    second_path_entry.insert(0, "/Users/thibauld.croonenborghs/Desktop/test2")
    l_files = tk.StringVar(value=os.listdir(first_path.get()))
    r_files = tk.StringVar(value=os.listdir(second_path.get()))

    msgbox = tk.Listbox(mainframe, listvariable=l_files, background="white", width=30, height=40)
    msgbox2 = tk.Listbox(mainframe, listvariable=r_files, background="white", width=30, height=40)
    msgbox.focus()

    first_path_entry.grid(row=0, column=0)
    second_path_entry.grid(row=0, column=4)
    msgbox.grid(row=1,column=0, padx=10)
    tk.ttk.Separator(mainframe, orient="vertical").grid(column=1, row=0, rowspan=3, sticky='ns')
    move_button = tk.ttk.Button(mainframe, text="->", command=move_file_forward, width=2)
    move_button.grid(row=1, column=2, padx=10, pady=10)
    tk.ttk.Separator(mainframe, orient="vertical").grid(column=3, row=0, rowspan=3, sticky='ns')
    msgbox2.grid(row=1,column=4, padx=10)
    msgbox.selection_set(0)
    root.mainloop()
