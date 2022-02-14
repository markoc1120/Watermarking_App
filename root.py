import tkinter as tk
from tkinter import filedialog
from PIL import Image


class MainApplication(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.filename = None
        self.filename_mk = None
        # IMAGE
        self.canvas = tk.Canvas(width=600, height=512)
        self.image = tk.PhotoImage(file='/Users/markoc1120/PycharmProjects/Watermarking_App/logo.png')
        self.canvas.create_image(300, 256, image=self.image)
        self.canvas.grid(column=0, columnspan=3, row=0)

        # ADD_IMG BUTTON
        self.add_img = tk.Button(text='Add Image', command=self.browse_files)
        self.add_img.config(width=12, padx=10)
        self.add_img.grid(column=0, row=1)

        # IMG_SELECTED LABEL
        self.img_selected = tk.Label(text='Nothing selected')
        self.img_selected.config(padx=10)
        self.img_selected.grid(column=1, row=1)

        # ADD_WATERMARK BUTTON
        self.add_wm = tk.Button(text='Add Watermark', command=self.browse_mk)
        self.add_wm.config(width=12, padx=10)
        self.add_wm.grid(column=0, row=2)

        # WM_SELECTED LABEL
        self.wm_selected = tk.Label(text='Nothing selected')
        self.wm_selected.config(padx=10)
        self.wm_selected.grid(column=1, row=2)

        # MAKE MAGIC TO HAPPEN
        self.magic = tk.Button(text='Make Magic', command=self.magic_func)
        self.magic.config(padx=10)
        self.magic.grid(column=0, columnspan=2, row=3)

    def browse_files(self):
        self.filename = filedialog.askopenfilename(initialdir="/",
                                                   title="Select a File",
                                                   filetypes=(("Jpeg files", "*.jpg"),
                                                              ("all files", "*.*")))
        # Change label contents
        self.img_selected.configure(text="File Opened: " + self.filename)

    def browse_mk(self):
        self.filename_mk = filedialog.askopenfilename(initialdir="/",
                                                      title="Select a File",
                                                      filetypes=(("Png files", "*.png"),
                                                                 ("all files", "*.*")))
        # Change label contents
        self.wm_selected.configure(text="File Opened: " + self.filename_mk)

    def magic_func(self):
        # Opening images
        img = Image.open(self.filename)
        wm_image = Image.open(self.filename_mk)

        # Setting watermark size ideal for the image
        mk_size = (round(img.width / 10), round(img.height / 10))
        wm_image.thumbnail(mk_size)

        # Make watermark opacity lower and then paste the images together
        paste_mask = wm_image.convert('L').point(lambda x: min(x, 100))
        img.paste(wm_image, (img.width - round(img.width / 8), img.height - round(img.height / 8)), mask=paste_mask)

        # Locating files, and then saves it there with a sign of 'watermarked_'
        filename_list = self.filename.split('/')
        img.save('/'.join(filename_list[:-1]) + '/watermarked_' + filename_list[-1])


if __name__ == "__main__":
    root = tk.Tk()
    root.title('WaterMark')
    MainApplication(root)
    root.mainloop()
