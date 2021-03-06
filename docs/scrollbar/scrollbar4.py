"""Widget with a scrollbar."""
from tklib import *

class Text(tk.Text):
    def __init__(self, scroll='', **kwargs):
        self = Scrollable(tk.Text, scroll=scroll, **kwargs)
        print(self)

class Demo(App):
    def __init__(self): 
        super().__init__()
        text = 'hello ' * 100
        Label("Text with scrollbars", font="Arial 18")

        Label('scroll=')
        Text(height=5)
        
        Label('scroll=x')
        Text(height=5, scroll='x', wrap='none')

        Label('scroll=y')
        Text(height=5, scroll='y')

        Label('scroll=xy')
        Text(height=5, scroll='xy', wrap='none')

Demo().run()