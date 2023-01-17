# -*- coding: utf-8 -*-
import tkinter as tk
from shortcut_tools.common import base_function


# 主窗口
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("450x400")
        self.title('快捷工具')
        base_function.DefaultConfiguration(self).menu_bar()
        base_function.DefaultConfiguration(self).center_window()


App().mainloop()
