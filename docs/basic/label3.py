"""Display images as buttons."""

from tklib import *
from PIL import Image, ImageTk

class Demo(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Label('Show images as buttons', font='Arial 24')

        dir = os.listdir('icons')
        n, m = 2, 5
        self.images = []
        Frame()
        for i in range(n):
            for j in range(m):
                k = m*i + j
                label = dir[k]
                path = 'icons/' + label
                img0 = Image.open(path)
                img = ImageTk.PhotoImage(img0)
                self.images.append(img)
                lb = Button(image=img, text=label, compound='top')
                lb.grid(row=i, column=j)

if __name__ == '__main__':
    Demo().run()