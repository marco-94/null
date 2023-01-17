# -*- coding: utf-8 -*-
"""
用户登录
"""
import time
from tkinter import *
from tkinter import ttk
import requests
from tkinter import messagebox
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from shortcut_tools.common import base_function, get_config, yaml_update


class WindowsLogin:
    data = get_config.get_config()

    erp_username_input_loop_text = None
    erp_username_input_loop = None
    password_input_loop_text = None
    password_input_loop = None
    environment_loop = None
    erp_username_var = None
    password_var = None

    def windows_login(self, root):
        """
        窗口1元素
        :return:
        """
        erp_username_input = Label(root, text='ERP账号')
        erp_username_input.grid(row=2, column=0, pady=5, sticky=E)
        self.erp_username_input_loop_text = StringVar()
        self.erp_username_input_loop = Entry(root, width=30, textvariable=self.erp_username_input_loop_text)
        self.erp_username_input_loop_text.set(self.data["username"])
        self.erp_username_input_loop.grid(row=2, column=1, pady=5, sticky='EW')

        self.erp_username_var = IntVar()
        erp_username_var_button = Checkbutton(root, text="记住账号", variable=self.erp_username_var, onvalue=1, offvalue=0)
        erp_username_var_button.grid(row=2, column=2, pady=5, sticky=W)

        password_input = Label(root, text='密码')
        password_input.grid(row=3, column=0, pady=5, sticky=E)
        self.password_input_loop_text = StringVar()
        self.password_input_loop = Entry(root, width=30, textvariable=self.password_input_loop_text, show='*')
        self.password_input_loop_text.set(self.data["password"])
        self.password_input_loop.grid(row=3, column=1, pady=5, sticky='EW')

        self.password_var = IntVar()
        password_var_button = Checkbutton(root, text="记住密码", variable=self.password_var, onvalue=1, offvalue=0)
        password_var_button.grid(row=3, column=2, sticky=W)

        environment = Label(root, text='环境')
        environment.grid(row=4, column=0, pady=5, sticky=E)
        self.environment_loop = ttk.Combobox(root, width=30)
        self.environment_loop['value'] = ('beta', 'prod')
        self.environment_loop['state'] = 'readonly'
        self.environment_loop.current(0)
        self.environment_loop.grid(row=4, column=1, pady=5, sticky='NW')

        Button(root, width=8, height=1, text="登录", command="").grid(row=6, column=0, columnspan=2)
        Button(root, width=8, text="取消记住", command="").grid(row=6, column=2, columnspan=2)
