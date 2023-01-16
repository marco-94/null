# -*- coding: utf-8 -*-
from tkinter import *


class WindowsThree:
    @staticmethod
    def windows_three(root):
        """
        窗口3
        :return:
        """
        erp_username_input = Label(root, text='敬请期待')
        erp_username_input.grid(row=2, column=0, pady=5, sticky=E)
