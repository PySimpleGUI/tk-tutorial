"""Using themes and styles."""

import tkinter as tk
import tkinter.ttk as ttk
from tklib import *

class Demo(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Label('Style TButton', font='Arial 24')
        Label('configure TButton')
        
        s = ttk.Style()
        themes = s.theme_names()
        s.configure('TButton', font='Arial 24')
  
        for t in themes:
            Button(t)

if __name__ == '__main__':
    Demo().run()