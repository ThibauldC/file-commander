import os
import tkinter as tk
from tkinter import ttk


def print_current_option():
    selection = msgbox.curselection()
    print(msgbox.get(selection[0]))


def insert_files_directories(box: tk.Listbox, path: tk.StringVar):
    for i, file in enumerate(os.listdir(path.get())):
        box.insert(i, file)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("File-commander")
    #root.geometry("500x250")
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    msgbox = tk.Listbox(mainframe, background="white", width=30, height=40)
    msgbox2 = tk.Listbox(mainframe, background="white", width=30, height=40)
    msgbox.focus()

    first_path = tk.StringVar()
    first_path_entry = ttk.Entry(mainframe, textvariable=first_path, width=30)

    second_path = tk.StringVar()
    second_path_entry = ttk.Entry(mainframe, textvariable=second_path, width=30)

    first_path_entry.insert(0, "/Users/thibauld.croonenborghs/git")
    second_path_entry.insert(0, "/Users/thibauld.croonenborghs/Downloads")
    insert_files_directories(msgbox, first_path)
    insert_files_directories(msgbox2, second_path)

    first_path_entry.grid(row=0, column=0)
    second_path_entry.grid(row=0, column=4)
    msgbox.grid(row=1,column=0, padx=10)
    tk.ttk.Separator(mainframe, orient="vertical").grid(column=1, row=0, rowspan=3, sticky='ns')
    move_button = tk.ttk.Button(mainframe, text="->", command=print_current_option, width=2)
    move_button.grid(row=1, column=2, padx=10, pady=10)
    tk.ttk.Separator(mainframe, orient="vertical").grid(column=3, row=0, rowspan=3, sticky='ns')
    msgbox2.grid(row=1,column=4, padx=10)
    root.mainloop()
