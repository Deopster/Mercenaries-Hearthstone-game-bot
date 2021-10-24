import tkinter as tk
from tkinter import *
import threading
import keyboard
from tkinter.ttk import *
def main():
    window = tk.Tk()

    label = tk.Label(
        text="HsBot v1.0",
        fg="white",
        bg="black",
        width=20,
        height=2
    )

    label.grid(column=0, row=0)
    combo = Combobox(window)
    window.title("HsBot v1.0")
    combo['values'] = ("1920x1080", "2560x1440", "not ready")
    combo.current(1)  # set the selected item
    combo.grid(column=0, row=1)
    window.mainloop()

if __name__ == '__main__':
    main()