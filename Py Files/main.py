import threading
import re
import os
import future.moves.tkinter.font as font

from future.moves import tkinter
from future.moves.tkinter import filedialog
from PIL import Image

root = tkinter.Tk()
root.geometry("300x400")
root.configure(bg='lightblue')
root.title("Convert Images")

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(root.winfo_screenheight() / 2 - 100 - windowHeight / 2)

root.geometry("+{}+{}".format(positionRight, positionDown))


def __init__():
    global items, fonts, textVars

    # Dictionary
    textVars = {
        "importFileLabelVar": tkinter.StringVar()
    }
    textVars.get("importFileLabelVar").set("Files Selected:")

    fonts = {
        "importFileFont": font.Font(family='Assistant Bold', size=15),
        "cancelFont": font.Font(family='Assistant Bold', size=12),
        "fileLabelFont": font.Font(family='Assistant Bold', size=12)
    }
    items = {
        "labels": {
            "importFileLabel": tkinter.Label(root, text=textVars.get("importFileLabelVar").get(),
                                             relief=tkinter.RAISED,
                                             borderwidth=0,
                                             font=fonts.get("fileLabelFont"),
                                             bg='lightblue')
        },
        "buttons": {
            "importButton": tkinter.Button(root, text="   Import Files    ", bg="#0373fc", activebackground='#0373fc',
                                           font=fonts.get("importFileFont"), borderwidth=0,
                                           command=lambda: clickEventImport("<Button-1>")),
            "convertButtonPNG": tkinter.Button(root, text="     Convert To PNG      ", bg="#0373fc",
                                               activebackground='#0373fc',
                                               font=fonts.get("importFileFont"), borderwidth=0,
                                               command=lambda: convertImageTo("png")),
            "convertButtonJPG": tkinter.Button(root, text="     Convert To JPG      ", bg="#0373fc",
                                               activebackground='#0373fc',
                                               font=fonts.get("importFileFont"), borderwidth=0,
                                               command=lambda: convertImageTo("jpg")),
            "convertButtonJPEG": tkinter.Button(root, text="    Convert To JPEG     ", bg="#0373fc",
                                                activebackground='#0373fc',
                                                font=fonts.get("importFileFont"), borderwidth=0,
                                                command=lambda: convertImageTo("jpeg")),
            "convertButtonWEBG": tkinter.Button(root, text="   Convert To WEBP    ", bg="#0373fc",
                                                activebackground='#0373fc',
                                                font=fonts.get("importFileFont"), borderwidth=0,
                                                command=lambda: convertImageTo("webp")),
            "cancel": tkinter.Button(root, text=" Cancel ", bg="#0373fc", activebackground='#0373fc',
                                     font=fonts.get("cancelFont"),
                                     borderwidth=0, command=lambda: restart())
        }
    }

    items.get("buttons").get("importButton").pack(side=tkinter.TOP, expand=tkinter.YES)
    items.get("labels").get("importFileLabel").pack(side=tkinter.TOP, expand=tkinter.YES)
    for item in items.get("buttons"):
        if item == "cancel": break
        items.get("buttons").get(item).pack(side=tkinter.TOP, expand=tkinter.YES)


def clearScreen():
    for item in items.keys():
        for name in items.get(item):
            items.get(item).get(name).pack_forget()


def restart():
    clearScreen()
    __init__()


def changeFileText(text):
    items.get("labels").get("importFileLabel").config(text=text)
    items.get("buttons").get("importButton").config(state=tkinter.NORMAL, bg="#0373fc")


def convertImageTo(filetype):
    try:
        exportLoc = filedialog.askdirectory()
        for filename in files:
            temp = filename
            filename = filename.strip()
            os.rename(temp, filename)
            Image.open(filename).convert('RGB').save(
                exportLoc + "/" + re.search("(.*)[.](.*)", filename.split("/")[-1]).group(1) + "." + filetype)
            items.get("labels").get("importFileLabel").config(text="Completed Converting")
            items.get("buttons").get("cancel").pack_forget()

            # timer for 5 secs
            suc = threading.Timer(4, lambda: changeFileText("Files Selected:"))
            suc.start()
    except:
        items.get("labels").get("importFileLabel").config(text="An Error Occurred")
        items.get("buttons").get("cancel").pack_forget()
        err = threading.Timer(4, lambda: changeFileText("Files Selected:"))
        err.start()


def newInit():
    clearScreen()
    items.get("buttons").get("importButton").config(bg="lightgray", state=tkinter.DISABLED)
    items.get("buttons").get("importButton").pack(side=tkinter.TOP, expand=tkinter.YES)
    items.get("buttons").get("cancel").pack(side=tkinter.TOP, expand=tkinter.YES)
    items.get("labels").get("importFileLabel").pack(side=tkinter.TOP, expand=tkinter.YES)
    for item in items.get("buttons"):
        items.get("buttons").get(item).pack(side=tkinter.TOP, expand=tkinter.YES)


def clickEventImport(event):
    global files
    files = filedialog.askopenfilenames(initialdir="/", title="Select Files", filetypes=(("Image Files",
                                                                                          "*.png"),
                                                                                         ("Image Files",
                                                                                          "*.jpg"),
                                                                                         ("Image Files",
                                                                                          "*.jpeg"),
                                                                                         ("Image Files",
                                                                                          "*.webp"),
                                                                                         ("All Files",
                                                                                          "*.*")))
    s = "File Selected: "
    if len(files) <= 3:
        for file in files:
            s += "\n" + file.split("/")[-1]
    else: s = "Multiple Files Selected"
    textVars.get("importFileLabelVar").set(s)
    items.get("labels").get("importFileLabel").config(text=textVars.get("importFileLabelVar").get())
    newInit()


__init__()
root.mainloop()
