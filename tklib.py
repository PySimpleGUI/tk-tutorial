import sys, os
import tkinter as tk
import tkinter.ttk as ttk

import math
from PIL import ImageGrab

class Callback:
    """Provide a callback function."""
    def cb(self, event=None):
        """Execute the cmd string in the widget context."""
        exec(self.cmd)

class Frame(ttk.Frame):
    """Create a frame around widgets."""
    def __init__(self, nb=None, **kwargs):
        if nb == None:
            super(Frame, self).__init__(App.parent, **kwargs)
        else:
            super(Frame, self).__init__(App.nb, **kwargs)
            App.nb.add(self, text=nb)
            print(App.nb, self, nb)
        # App.stack.append(App.parent)
        # App.parent = self
        self.grid()

class Label(ttk.Label):
    """Create a Label object."""
    def __init__(self, text='Label', **kwargs):
        super(Label, self).__init__(App.parent, text=text, **kwargs)
        self.grid()

class Button(ttk.Button, Callback):
    """Create a Button object."""
    def __init__(self, text='Button', cmd='', **kwargs):
        self.cmd = cmd
        super(Button, self).__init__(App.parent, text=text, command=self.cb, **kwargs)
        self.bind('<Return>', self.cb)
        self.grid()

class Radiobutton:
    """Create a Radiobutton object."""
    def __init__(self, items='Radio', cmd='', **kwargs):
        self.items = items.split(';')
        self.cmd = cmd
        self.val = tk.IntVar()
        self.val.set(0)
        for i, item in enumerate(items.split(';')):
            r = ttk.Radiobutton(App.parent, text=item, variable=self.val, value=i, command=self.cb, **kwargs)
            r.grid(sticky='w')

    def cb(self):
        """Evaluate the cmd string in the Radiobutton context."""
        self.item = self.items[self.val.get()]
        exec(self.cmd)

class Checkbox:
    """Create a Checkbox object."""
    def __init__(self, items='Check', cmd='', **kwargs):
        self.items = items.split(';')
        self.val = []
        self.cmd = cmd
        for i, item in enumerate(items.split(';')):
            self.val.append(tk.IntVar())
            c = ttk.Checkbutton(App.parent, text=item, command=self.cb, variable=self.val[i], **kwargs)
            c.grid(sticky='w')

    def cb(self):
        """Evaluate the cmd string in the Checkbox context."""
        self.selection = []
        for i, item in enumerate(self.items):
            if self.val[i].get() == 1:
                self.selection.append(item)
        exec(self.cmd)

class Entry(ttk.Entry, Callback):
    """Create an Entry object with a command string."""
    def __init__(self, label='', cmd='', **kwargs):
        self.var = tk.StringVar()
        self.cmd = cmd
        if label == '':
            super(Entry, self).__init__(App.parent, textvariable=self.var, **kwargs)
            self.grid()
        else:
            fr = ttk.Frame(App.parent)
            ttk.Label(fr, text=label).grid()
            super(Entry, self).__init__(fr, textvariable=self.var, **kwargs)
            self.grid(row=0, column=1)
            fr.grid(sticky='e')
        self.bind('<Return>', self.cb)

class Canvas(tk.Canvas):
    """Define a canvas."""
    def __init__(self, **kwargs):
        # super(Canvas, self).__init__(App.parent, width=w, height=h, bg='light blue')
        super(Canvas, self).__init__(App.parent, **kwargs)
        self.grid()

    def polygon(self, x0, y0, r, n, **kwargs):
        points = []
        for i in range(n):
            a = 2 * math.pi * i / n
            x = x0 + math.sin(a) * r
            y = y0 + math.cos(a) * r
            points.append(x)
            points.append(y)
        self.create_polygon(points, **kwargs)

class Listbox(tk.Listbox):
    """Define a Listbox object."""
    def __init__(self, items='Listbox', cmd='', **kwargs):
        self.cmd = cmd
        super(Listbox, self).__init__(App.parent, **kwargs)
        if isinstance(items, str):
            items = items.split(';')
        self.items = items
        for item in items:
            self.insert(tk.END, item)
        for i in range(0, self.size(), 2):
            self.itemconfigure(i, background='#f0f0ff')
        self.grid()
        self.bind('<<ListboxSelect>>', self.cb)

    def cb(self, event):
        """Evaluate the cmd string in the Listbox context."""
        self.item = self.items[self.curselection()[0]]
        exec(self.cmd)

class Scale(tk.Scale):
    """Define a Scale object."""
    def __init__(self, **kwargs):
        self.var = tk.IntVar()
        super(Scale, self).__init__(App.parent, variable=self.var, **kwargs)
        self.grid()

class Combobox(ttk.Combobox):
    """Define a Combobox."""
    def __init__(self, label='', values='', cmd='', **kwargs):
        self.cmd = cmd
        if isinstance(values, str):
            values = values.split(';')
        self.val = tk.StringVar()
        self.val.set(values[0])
        if label == '':
            super(Combobox, self).__init__(App.parent, textvariable=self.val, **kwargs)
            self.grid()
        else:
            fr = ttk.Frame(App.parent)
            ttk.Label(fr, text=label).grid()
            super(Combobox, self).__init__(fr, textvariable=self.val, **kwargs)
            self.grid(row=0, column=1)
            fr.grid(sticky='e')

        self['values'] = values
        self.bind('<<ComboboxSelected>>', self.cb)

    def cb(self, event):
        """Evaluate the cmd string in the Combobox context."""
        self.item = self.val.get()
        exec(self.cmd)

class Spinbox(ttk.Spinbox, Callback):
    """Define a Spinbox widget."""
    def __init__(self, label='', cmd='', to=100, **kwargs):
        self.cmd = cmd
        self.val = tk.StringVar()
        self.val.set(0)

        if label == '':
            super(Spinbox, self).__init__(App.parent, textvariable=self.val, to=to, **kwargs)
            self.grid()
        else:
            fr = ttk.Frame(App.parent)
            ttk.Label(fr, text=label).grid()
            super(Spinbox, self).__init__(fr, textvariable=self.val, to=to, **kwargs)
            self.grid(row=0, column=1)
            fr.grid(sticky='e')

        self.bind('<Return>', self.cb)

class Separator(ttk.Separator):
    """Insert a separator line."""
    def __init__(self, **kwargs):
        super(Separator, self).__init__(App.parent, **kwargs)
        self.grid(sticky="we", pady=5)

class Labelframe(ttk.Labelframe):
    """Insert a labelframe."""
    def __init__(self, **kwargs):
        super(Labelframe, self).__init__(App.parent, **kwargs)
        App.stack.append(App.parent)
        App.parent = self
        self.grid()

class Text(tk.Text):
    """Insert a text area."""
    def __init__(self, text='', scroll='', **kwargs):
        if scroll == '':
            super(Text, self).__init__(App.parent, **kwargs)
            self.grid()
        else:
            frame = ttk.Frame(App.parent)
            frame.grid()
            super(Text, self).__init__(frame, **kwargs)
            self.grid(row=0, column=0)
            if 'x' in scroll:
                scrollx = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.xview)
                scrollx.grid(row=1, column=0, sticky='we')
                self.configure(xscrollcommand=scrollx.set)
            if 'y' in scroll:
                scrolly = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.yview)
                scrolly.grid(row=0, column=1, sticky='ns')
                self.configure(yscrollcommand=scrolly.set)
        self.insert('1.0', text)

class Scrollbars:
    """Add xy scrollbars to a widget."""
    def add_scrollbars(self, Widget, scroll, **kwargs):
        if scroll == '':
            super(Widget, self).__init__(App.parent, **kwargs)
            self.grid()
        else:
            frame = ttk.Frame(App.parent)
            frame.grid()
            super(Widget, self).__init__(frame, **kwargs)
            self.grid(row=0, column=0)
            if 'x' in scroll:
                scrollx = ttk.Scrollbar(frame, orient=tk.HORIZONTAL, command=self.xview)
                scrollx.grid(row=1, column=0, sticky='we')
                self.configure(xscrollcommand=scrollx.set)
            if 'y' in scroll:
                scrolly = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.yview)
                scrolly.grid(row=0, column=1, sticky='ns')
                self.configure(yscrollcommand=scrolly.set)

# class Canvas(tk.Canvas, Scrollbars):
#     def __init__(self, **kwargs):
#         self.add_scrollbars(Canvas, scroll='', **kwargs)

class Treeview(ttk.Treeview):
    """Insert a treeview area."""
    def __init__(self, items=[], **kwargs):
        super(Treeview, self).__init__(App.parent, **kwargs)
        for item in items:
            self.insert('', 'end', text=item)
        self.grid()
        self.bind()
        self.bind('<<TreeviewSelect>>', self.select)
        self.bind('<<TreeviewOpen>>', self.open)
        self.bind('<<TreeviewClose>>', self.close)

    def select(self, event=None):
        print('select', self.focus())

    def open(self, event=None):
        print('open')

    def close(self, event=None):
        print('close')
    


class Pandedwindow(ttk.Panedwindow):
    """Insert a paned window."""
    def __init__(self, **kwargs):
        super(Pandedwindow, self).__init__(App.parent, **kwargs)
        App.stack.append(self)
        App.parent = self
        self.grid()

class Notebook(ttk.Notebook):
    def __init__(self, **kwargs):
        super(Notebook, self).__init__(App.root, **kwargs)
        App.nb = self
        self.grid()

class Window():
    """Open a new window."""
    def __init__(self, title='Window'):
        top = tk.Toplevel(App.root)
        top.title(title)
        frame = ttk.Frame(top, width=200, height=200, padding=(5, 10))
        frame.pack()
        App.parent = frame
        App.stack = [App.root]

        App.win = top
        App.menus = [tk.Menu(App.win)]
        App.win['menu'] = App.menus[0]

class Menu(tk.Menu):
    """Add a Menu() node to which a menu Item() can be attached."""
    def __init__(self, label, id=0, **kwargs):
        super(Menu, self).__init__(App.menus[0], **kwargs)
        App.menus[id].add_cascade(menu=self, label=label)
        App.menus.append(self)

class ContextMenu(tk.Menu):
    def __init__(self, widget):
        """Create a context menu attached to a widget."""
        super(ContextMenu, self).__init__(widget)
        App.menus.append(self)

        if (App.root.tk.call('tk', 'windowingsystem')=='aqua'):
            widget.bind('<2>', self.popup)
            widget.bind('<Control-1>', self.popup)
        else:
            widget.root.bind('<3>', self.popup)

    def popup(self, event):
        """Open a popup menu."""
        self.post(event.x_root, event.y_root)
        return 'break'

class Item(Callback):
    """Add a menu item to a Menu() node. Default is the last menu (id=-1)."""
    def __init__(self, label, cmd='', acc='', id=-1, **kwargs):
        self.cmd = cmd
        if acc != '':
            key = '<{}>'.format(acc)
            App.root.bind(key, self.cb)

        if label == '-':
            App.menus[id].add_separator()
        elif label[0] == '*':
            App.menus[id].add_checkbutton(label=label[1:], command=self.cb, accelerator=acc, **kwargs)
        elif label[0] == '#':
            App.menus[id].add_radiobutton(label=label[1:], command=self.cb, accelerator=acc, **kwargs)
        else:
            App.menus[id].add_command(label=label, command=self.cb, accelerator=acc, **kwargs)

class App(tk.Frame):
    """Define the application base class."""
    root = tk.Tk()
    root.option_add('*tearOff', False)

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    parent = root
    stack = [parent]

    menubar = tk.Menu(root)
    root['menu'] = menubar
    menus = [menubar]

    def __init__(self):
        """Define the Tk() root widget and a background frame."""
        frame = ttk.Frame(App.root, width=200, height=200, padding=(5, 10))
        frame.grid()
        App.parent = frame
        App.root.bind('<Key>', self.callback)
        App.root.bind('<Escape>', quit)
        App.root.createcommand('tk::mac::ShowPreferences', self.preferences)
        App.root.createcommand('tk::mac::ShowHelp', self.help)

    def run(self):
        """Run the main loop."""
        self.root.mainloop()

    def save_img(self):
        """Save a screen capture to the current folder."""
        App.root.update()
        x = App.root.winfo_rootx()
        y = App.root.winfo_rooty()
        w = App.root.winfo_width()
        h = App.root.winfo_height()
        print(x, y, w, h)
        im = ImageGrab.grab((x, y, x+w, y+h))

        name = type(self).__name__
        module = sys.modules['__main__']
        path, name = os.path.split(module.__file__)
        name, ext = os.path.splitext(name)
        filename = path + '/' + name + '.png'
        im.save(filename)

    def callback(self, event):
        """Execute a callback function."""
        if event.char == 'p':
            self.save_img()

    def preferences(self):
        """Show preferences dialog."""
        print('show preferences')

    def help(self):
        """Show help menu."""
        print('show help')

if __name__ == '__main__':
    App().run()