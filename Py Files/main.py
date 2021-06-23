import threading
import re
import os
import future.moves.tkinter.font as font

from future.moves import tkinter
from future.moves.tkinter import filedialog
from PIL import Image
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

root = tkinter.Tk()
root.configure(bg='lightblue')

windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
positionDown = int(root.winfo_screenheight() / 2 - 100 - windowHeight / 2)

root.geometry("+{}+{}".format(positionRight, positionDown))


def __init__():
    global items, fonts, textVars, start

    # Dictionary
    textVars = {
        "startLabelVar": tkinter.StringVar(),
        "importFileLabelVar": tkinter.StringVar()
    }
    textVars.get("importFileLabelVar").set("Files Selected:")
    textVars.get("startLabelVar").set("Choose What Type Of Files \nYou Would Like To \nConvert To(Videos / Images):")

    fonts = {
        "importFileFont": font.Font(family='Assistant Bold', size=15),
        "cancelFont": font.Font(family='Assistant Bold', size=12),
        "fileLabelFont": font.Font(family='Assistant Bold', size=12),
        "startLabelFont": font.Font(family='Assistant Bold', size=12),
        "startImage": font.Font(family='Assistant Bold', size=12),
        "startVideo": font.Font(family='Assistant Bold', size=12)
    }
    start = {
        "image": tkinter.Button(root, text="     Convert Images     ", bg="#0373fc", activebackground='#0373fc',
                                font=fonts.get("importFileFont"), borderwidth=0, command=imageStart),
        "video": tkinter.Button(root, text="     Convert Videos     ", bg="#0373fc", activebackground='#0373fc',
                                font=fonts.get("importFileFont"), borderwidth=0, command=videoStart)
    }
    items = {
        "labels": {
            "startLabel": tkinter.Label(root, text=textVars.get("startLabelVar").get(),
                                        relief=tkinter.RAISED,
                                        borderwidth=0,
                                        font=fonts.get("startLabelFont"),
                                        bg='lightblue'),
            "importFileLabel": tkinter.Label(root, text=textVars.get("importFileLabelVar").get(),
                                             relief=tkinter.RAISED,
                                             borderwidth=0,
                                             font=fonts.get("fileLabelFont"),
                                             bg='lightblue')
        },
        "ImageButtons": {
            "importButton": tkinter.Button(root, text="   Import Files    ", bg="#0373fc", activebackground='#0373fc',
                                           font=fonts.get("importFileFont"), borderwidth=0,
                                           command=lambda: clickEventImportImage("<Button-1>")),
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
                                     borderwidth=0, command=lambda: restartImage()),
            "back": tkinter.Button(root, text=" Back ", bg="#0373fc", activebackground='#0373fc',
                                   font=fonts.get("cancelFont"),
                                   borderwidth=0, command=lambda: startScreen())
        },
        "VideoButtons": {
            "importButton": tkinter.Button(root, text="   Import Files    ", bg="#0373fc", activebackground='#0373fc',
                                           font=fonts.get("importFileFont"), borderwidth=0,
                                           command=lambda: clickEventImportVideo("<Button-1>")),
            "convertButtonMP4": tkinter.Button(root, text="   Convert To MP4    ", bg="#0373fc",
                                               activebackground='#0373fc',
                                               font=fonts.get("importFileFont"), borderwidth=0,
                                               command=lambda: convertVideoTo("mp4")),
            "convertButtonMOV": tkinter.Button(root, text="   Convert To MOV    ", bg="#0373fc",
                                               activebackground='#0373fc',
                                               font=fonts.get("importFileFont"), borderwidth=0,
                                               command=lambda: convertVideoTo("mov")),
            "convertButtonAVI": tkinter.Button(root, text="    Convert To AVI     ", bg="#0373fc",
                                               activebackground='#0373fc',
                                               font=fonts.get("importFileFont"), borderwidth=0,
                                               command=lambda: convertVideoTo("avi")),
            "convertButtonMKV": tkinter.Button(root, text="   Convert To MKV    ", bg="#0373fc",
                                               activebackground='#0373fc',
                                               font=fonts.get("importFileFont"), borderwidth=0,
                                               command=lambda: convertVideoTo("mkv")),
            "cancel": tkinter.Button(root, text=" Cancel ", bg="#0373fc", activebackground='#0373fc',
                                     font=fonts.get("cancelFont"),
                                     borderwidth=0, command=lambda: restartVideo()),
            "back": tkinter.Button(root, text=" Back ", bg="#0373fc", activebackground='#0373fc',
                                   font=fonts.get("cancelFont"),
                                   borderwidth=0, command=lambda: startScreen())
        }
    }
    startScreen()


def imageStart():
    root.geometry("300x400")
    root.title("Select Image Files")
    clearScreen()
    items.get("ImageButtons").get("importButton").pack(side=tkinter.TOP, expand=tkinter.YES)
    items.get("labels").get("importFileLabel").pack(side=tkinter.TOP, expand=tkinter.YES)
    for item in items.get("ImageButtons"):
        if item == "cancel":
            continue
        items.get("ImageButtons").get(item).pack(side=tkinter.TOP, expand=tkinter.YES)
    items.get("labels").get("importFileLabel").config(text="Files Selected: ")
    items.get("ImageButtons").get("importButton").config(state=tkinter.NORMAL, bg="#0373fc")


def videoStart():
    root.geometry("300x400")
    root.title("Select Video Files")
    clearScreen()
    items.get("VideoButtons").get("importButton").pack(side=tkinter.TOP, expand=tkinter.YES)
    items.get("labels").get("importFileLabel").pack(side=tkinter.TOP, expand=tkinter.YES)
    for item in items.get("VideoButtons"):
        if item == "cancel":
            continue
        items.get("VideoButtons").get(item).pack(side=tkinter.TOP, expand=tkinter.YES)
    items.get("labels").get("importFileLabel").config(text="Files Selected: ")
    items.get("VideoButtons").get("importButton").config(state=tkinter.NORMAL, bg="#0373fc")


def startScreen():
    clearScreen()
    root.geometry("250x250")
    root.title("Start Screen")
    items.get("labels").get("startLabel").pack(side=tkinter.TOP, expand=tkinter.YES)
    for startItem in start.keys():
        start.get(startItem).pack(side=tkinter.TOP, expand=tkinter.YES)


def clearScreen():
    for item in start.keys():
        start.get(item).pack_forget()
    for item in items.keys():
        for name in items.get(item):
            items.get(item).get(name).pack_forget()


def restartVideo():
    clearScreen()
    videoStart()


def restartImage():
    clearScreen()
    imageStart()


def changeFileText(text):
    items.get("labels").get("importFileLabel").config(text=text)
    items.get("ImageButtons").get("importButton").config(state=tkinter.NORMAL, bg="#0373fc")


def convertImageTo(filetype):
    exportLoc = filedialog.askdirectory()
    if exportLoc == "":
        clearScreen()
        imageStart()
        return
    for filename in files:
        temp = filename
        filename = filename.strip()
        os.rename(temp, filename)
        Image.open(filename).convert('RGB').save(
            exportLoc + "/" + re.search("(.*)[.](.*)", filename.split("/")[-1]).group(1) + "." + filetype)
        items.get("labels").get("importFileLabel").config(text="Completed Converting")
        items.get("ImageButtons").get("cancel").pack_forget()

        # timer for 5 secs
        suc = threading.Timer(4, lambda: changeFileText("Files Selected:"))
        suc.start()


def convertVideoTo(filetype):
    items.get("labels").get("importFileLabel").config(text="Converting...\n(Its OK the program is not responding)")
    exportLoc = filedialog.askdirectory()
    print(exportLoc)
    if exportLoc == "":
        clearScreen()
        videoStart()
        return
    for file in files:
        clip = VideoFileClip(file)
        clip.write_videofile(exportLoc + "/" + re.search("(.*)[.](.*)", file.split("/")[-1]).group(1) + "." + filetype, codec="libx264")
    items.get("labels").get("importFileLabel").config(text="Done Converting!")
    suc = threading.Timer(4, lambda: restartVideo())
    suc.start()


def selectedFilesImage():
    clearScreen()
    root.geometry("300x450")
    items.get("ImageButtons").get("importButton").config(state=tkinter.DISABLED, bg="gray")
    items.get("ImageButtons").get("importButton").pack(side=tkinter.TOP, expand=tkinter.YES)
    items.get("ImageButtons").get("cancel").pack(side=tkinter.TOP, expand=tkinter.YES)
    items.get("labels").get("importFileLabel").pack(side=tkinter.TOP, expand=tkinter.YES)
    for item in items.get("ImageButtons").keys():
        items.get("ImageButtons").get(item).pack(side=tkinter.TOP, expand=tkinter.YES)


def selectedFilesVideo():
    clearScreen()
    root.geometry("300x450")
    items.get("VideoButtons").get("importButton").config(state=tkinter.DISABLED, bg="gray")
    items.get("VideoButtons").get("importButton").pack(side=tkinter.TOP, expand=tkinter.YES)
    items.get("VideoButtons").get("cancel").pack(side=tkinter.TOP, expand=tkinter.YES)
    items.get("labels").get("importFileLabel").pack(side=tkinter.TOP, expand=tkinter.YES)
    for item in items.get("VideoButtons").keys():
        items.get("VideoButtons").get(item).pack(side=tkinter.TOP, expand=tkinter.YES)


def clickEventImportImage(event):
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
    s = "Files Selected: "
    if len(files) <= 3:
        for file in files:
            s += "\n" + file.split("/")[-1]
    else:
        s = "Multiple Files Selected"
    textVars.get("importFileLabelVar").set(s)
    items.get("labels").get("importFileLabel").config(text=textVars.get("importFileLabelVar").get())
    selectedFilesImage()


def clickEventImportVideo(event):
    global files
    files = filedialog.askopenfilenames(initialdir="/", title="Select Files", filetypes=(("Image Files",
                                                                                          "*.mp4"),
                                                                                         ("Image Files",
                                                                                          "*.avi"),
                                                                                         ("Image Files",
                                                                                          "*.mov"),
                                                                                         ("Image Files",
                                                                                          "*.mkv"),
                                                                                         ("All Files",
                                                                                          "*.*")))
    s = "Files Selected: "
    if len(files) <= 3:
        for file in files:
            s += "\n" + file.split("/")[-1]
    else:
        s = "Multiple Files Selected"
    textVars.get("importFileLabelVar").set(s)
    items.get("labels").get("importFileLabel").config(text=textVars.get("importFileLabelVar").get())
    selectedFilesVideo()


__init__()
root.mainloop()
