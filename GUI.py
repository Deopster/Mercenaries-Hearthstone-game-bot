import tkinter as tk
from tkinter import *
import threading
import keyboard
from tkinter.ttk import *
from tkinter.messagebox import showinfo
def main():
    window = tk.Tk()
    window.overrideredirect(True)
    window.attributes("-topmost",True)
    window.resizable(width=False, height=False)
    label = tk.Label(
        text="HsBot v1.0",
        bg="white",
        fg="black",
        width=20,
        height=1
    ).grid(column=0, row=0)
    st = Style()
    st.configure('W.TButton', background='#555', foreground='#ccc',padx="2",pady="8", font=('Arial', 16))
    Button(window, text='>', style='W.TButton', command=None).grid(column=0, row=3)
    combo = Combobox(
        state="readonly"
    )
    window.title("HsBot v1.0")
    combo['values'] = ("1920x1080", "2560x1440", "not ready")
    combo.current(1)  # set the selected item
    combo.grid(column=0, row=2)

    def download_clicked():
        showinfo(
            title='Information',
            message='The bot has started'
        )

    download_icon = tk.PhotoImage(file='./files/play.png')
    Button(window,image=download_icon,command=download_clicked).grid(column=0, row=1)
    window.mainloop()

if __name__ == '__main__':
    main()