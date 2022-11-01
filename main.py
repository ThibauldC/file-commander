import tkinter as tk
from tkinter import ttk

def print_current_option():
    selection = msgbox.curselection()
    print(msgbox.get(selection[0]))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Filr")
    root.geometry("500x200")
    mainframe = ttk.Frame(root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky='nsew')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    msgbox = tk.Listbox(mainframe, background="white")
    msgbox.insert(1, "option1")
    msgbox.insert(2, "option2")
    msgbox2 = tk.Listbox(mainframe, background="white")
    msgbox2.insert(1, "option1")
    msgbox2.insert(2, "option2")
    msgbox.focus()

    msgbox.grid(row=0,column=0, padx=10)
    tk.ttk.Separator(mainframe, orient="vertical").grid(column=1, row=0, rowspan=3, sticky='ns')
    move_button = tk.ttk.Button(mainframe, text="->", command=print_current_option, width=2)
    move_button.grid(row=0, column=2, padx=10, pady=10)
    tk.ttk.Separator(mainframe, orient="vertical").grid(column=3, row=0, rowspan=3, sticky='ns')
    msgbox2.grid(row=0,column=4, padx=10)
    root.mainloop()
