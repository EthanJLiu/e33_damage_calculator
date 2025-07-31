import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()

# Get the TkDefaultFont object
default_font = tkFont.nametofont("TkDefaultFont")

# Get the actual properties of the font
font_details = default_font.actual()

print(f"Default Font Details: {font_details}")

root.destroy()