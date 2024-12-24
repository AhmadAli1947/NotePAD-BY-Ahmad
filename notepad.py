from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import simpledialog
import os
import win32api
import win32print

def newFile():
    global file
    root.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0, END)
    update_status_bar()
    update_bottom_bar()

def openFile():
    global file
    file = askopenfilename(defaultextension=".txt",
                           filetypes=[("All Files", "*.*"),
                                      ("Text Documents", "*.txt")])
    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + " - Notepad")
        TextArea.delete(1.0, END)
        with open(file, "r") as f:
            TextArea.insert(1.0, f.read())
    update_status_bar()
    update_bottom_bar()

def saveFile():
    global file
    if file is None:
        file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                  filetypes=[("All Files", "*.*"),
                                             ("Text Documents", "*.txt")])
        if file == "":  # User canceled the save dialog
            file = None
        else:
            with open(file, "w") as f:
                f.write(TextArea.get(1.0, END))
            root.title(os.path.basename(file) + " - Notepad")
    else:
        with open(file, "w") as f:
            f.write(TextArea.get(1.0, END))
    update_status_bar()
    update_bottom_bar()

def saveAsFile():
    global file
    file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                              filetypes=[("All Files", "*.*"),
                                        ("Text Documents", "*.txt")])
    if file != "":  # User canceled the save dialog
        with open(file, "w") as f:
            f.write(TextArea.get(1.0, END))
        root.title(os.path.basename(file) + " - Notepad")
    update_status_bar()
    update_bottom_bar()

def printFile():
    content = TextArea.get(1.0, END)
    temp_file = "temp.txt"
    with open(temp_file, "w") as f:
        f.write(content)
    # Print the file
    try:
        win32api.ShellExecute(0, "print", temp_file, None, ".", 0)
        os.remove(temp_file)  # Delete the temporary file after printing
    except Exception as e:
        showinfo("Error", f"An error occurred while printing: {str(e)}")

def quitApp():
    root.destroy()

def cut():
    TextArea.event_generate("<<Cut>>")
    update_status_bar()
    update_bottom_bar()

def copy():
    TextArea.event_generate("<<Copy>>")

def paste():
    TextArea.event_generate("<<Paste>>")
    update_status_bar()
    update_bottom_bar()

def undo():
    try:
        TextArea.edit_undo()
        update_status_bar()
        update_bottom_bar()
    except Exception:
        pass

def redo():
    try:
        TextArea.edit_redo()
        update_status_bar()
        update_bottom_bar()
    except Exception:
        pass

def about():
    showinfo("Notepad", "Welcome to the Notepad application! This lightweight and user-friendly text editor is designed to help you quickly create, edit, and manage plain text files with ease.\n\nDeveloped with dedication by Muhammad Usama.")

def update_status_bar(event=None):
    line, col = TextArea.index(INSERT).split('.')
    status_var.set(f"Line: {line}, Column: {col}")

def update_bottom_bar():
    if file:
        file_name = os.path.basename(file)
        file_size = os.path.getsize(file) if os.path.exists(file) else 0
        char_count = len(TextArea.get(1.0, END)) - 1
        bottom_var.set(f"File: {file_name} | Size: {file_size} bytes | Characters: {char_count}")
    else:
        bottom_var.set("No file selected")

# Format Menu Functions
def toggle_word_wrap():
    global word_wrap
    word_wrap = not word_wrap
    if word_wrap:
        TextArea.config(wrap=WORD)
    else:
        TextArea.config(wrap=NONE)

def change_font_size_popup():
    def apply_font_size():
        size = font_size_var.get()
        try:
            size = int(size)
            TextArea.config(font=f"lucida {size}")
            font_popup.destroy()
        except ValueError:
            showinfo("Error", "Invalid font size. Please enter a valid number.")

    # Create popup for font size
    font_popup = Toplevel(root)
    font_popup.title("Change Font Size")
    font_popup.geometry("250x100")
    font_popup.resizable(False, False)

    Label(font_popup, text="Enter Font Size:", font="lucida 10").pack(pady=5)
    font_size_var = StringVar()
    Entry(font_popup, textvariable=font_size_var, font="lucida 10").pack(pady=5)
    Button(font_popup, text="Apply", command=apply_font_size).pack(pady=5)

# View Menu Functions
def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    if dark_mode:
        TextArea.config(bg="black", fg="white", insertbackground="white")
        StatusBar.config(bg="black", fg="white")
        BottomBar.config(bg="black", fg="white")
    else:
        TextArea.config(bg="white", fg="black", insertbackground="black")
        StatusBar.config(bg="lightgrey", fg="black")
        BottomBar.config(bg="red", fg="white")

if __name__ == '__main__':
    # Basic tkinter setup
    root = Tk()
    root.title("Untitled - Notepad")
    root.geometry("644x788")

    # Add TextArea
    TextArea = Text(root, font="lucida 13", undo=True, wrap=WORD)
    file = None
    word_wrap = True
    dark_mode = False
    TextArea.pack(expand=True, fill=BOTH)

    # Bind the TextArea to update status and bottom bar on key release
    TextArea.bind("<KeyRelease>", lambda event: (update_status_bar(), update_bottom_bar()))

    # Create a MenuBar
    MenuBar = Menu(root)

    # File Menu
    FileMenu = Menu(MenuBar, tearoff=0)
    FileMenu.add_command(label="New", command=newFile)
    FileMenu.add_command(label="Open", command=openFile)
    FileMenu.add_command(label="Save", command=saveFile)
    FileMenu.add_command(label="Save As", command=saveAsFile)
    FileMenu.add_command(label="Print", command=printFile)
    FileMenu.add_separator()
    FileMenu.add_command(label="Exit", command=quitApp)
    MenuBar.add_cascade(label="File", menu=FileMenu)

    # Edit Menu
    EditMenu = Menu(MenuBar, tearoff=0)
    EditMenu.add_command(label="Cut", command=cut)
    EditMenu.add_command(label="Copy", command=copy)
    EditMenu.add_command(label="Paste", command=paste)
    EditMenu.add_command(label="Undo", command=undo)
    EditMenu.add_command(label="Redo", command=redo)
    MenuBar.add_cascade(label="Edit", menu=EditMenu)

    # Format Menu
    FormatMenu = Menu(MenuBar, tearoff=0)
    FormatMenu.add_command(label="Word Wrap", command=toggle_word_wrap)
    FormatMenu.add_command(label="Change Font Size", command=change_font_size_popup)
    MenuBar.add_cascade(label="Format", menu=FormatMenu)

    # View Menu
    ViewMenu = Menu(MenuBar, tearoff=0)
    ViewMenu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)
    MenuBar.add_cascade(label="View", menu=ViewMenu)

    # Help Menu
    HelpMenu = Menu(MenuBar, tearoff=0)
    HelpMenu.add_command(label="About Notepad", command=about)
    MenuBar.add_cascade(label="Help", menu=HelpMenu)

    root.config(menu=MenuBar)

    # Adding Scrollbar
    Scroll = Scrollbar(root)
    Scroll.pack(side=RIGHT, fill=Y)
    Scroll.config(command=TextArea.yview)
    TextArea.config(yscrollcommand=Scroll.set)

    # Adding Status Bar
    status_var = StringVar()
    status_var.set("Line: 1, Column: 1")
    StatusBar = Label(root, textvariable=status_var, anchor='w', font="lucida 10", relief=SUNKEN, bg="lightgrey")
    StatusBar.pack(side=BOTTOM, fill=X)

    # Adding Bottom Bar
    bottom_var = StringVar()
    bottom_var.set("No file selected")
    BottomBar = Label(root, textvariable=bottom_var, anchor='w', font="lucida 10 bold", relief=SUNKEN, bg="red", fg="white")
    BottomBar.pack(side=BOTTOM, fill=X)

    root.mainloop()
