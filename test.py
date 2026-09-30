import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.withdraw()  # Hide the main window
messagebox.showinfo("Success", "The file worked!")
root.destroy()
