# -*- coding: utf-8 -*-
import time
from tkinter import *
from tkinter import ttk
import tkinter as tk
import requests
from tkinter import messagebox
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from shortcut_tools.common import base_function, get_config, yaml_update


class WindowsAddProperty:
    data = get_config.get_config()

    trans_type_combobox = None
    category_combobox = None
    picture_var = None
    video_var = None
    attorney_var = None
    promotion_var = None
    key_var = None
    sole_var = None
    entertained_var = None
    bargaining_var = None
    environment_loop = None
    erp_username_input_loop_text = None
    erp_username_input_loop = None
    password_input_loop_text = None
    password_input_loop = None
    city_code_input_loop_text = None
    city_code_input_loop = None
    organ_id_input_loop_text = None
    organ_id_input_loop = None
    brand_id_input_loop_text = None
    brand_id_input_loop = None
    estate_code_input_loop_text = None
    estate_code_input_loop = None
    erp_username_var = None
    password_var = None
    city_code_var = None
    brand_id_var = None
    organ_id_var = None
    estate_code_var = None

    def windows_add_property(self, root):
        """
        新增房源
        :return:
        """
        trans_type = Label(root, text='房源类型')
        trans_type.grid(row=0, column=0, pady=5, sticky=E)
        self.trans_type_combobox = ttk.Combobox(root, width=20)
        self.trans_type_combobox['value'] = ('二手房', '租房')
        self.trans_type_combobox['state'] = 'readonly'
        self.trans_type_combobox.current(0)
        self.trans_type_combobox.grid(row=0, column=1, pady=5, sticky='NW')

        category = Label(root, text='房源用途')
        category.grid(row=1, column=0, pady=5, sticky=E)
        self.category_combobox = ttk.Combobox(root, width=20)
        self.category_combobox['value'] = ('普通住宅', '别墅', '商住两用', '车位', '商铺', '写字楼', '厂房', '土地')
        self.category_combobox['state'] = 'readonly'
        self.category_combobox.current(0)
        self.category_combobox.grid(row=1, column=1, pady=5, sticky='NW')

        category = Label(root, text='房源标记')
        category.grid(row=0, column=2, pady=5, sticky=E)

        self.picture_var = IntVar()
        mark_checkbutton_picture = Checkbutton(root, text="图勘", variable=self.picture_var, onvalue=1, offvalue=0)
        mark_checkbutton_picture.grid(row=1, column=2, pady=5, sticky=W)
        self.video_var = IntVar()
        mark_checkbutton_video = Checkbutton(root, text="视频", variable=self.video_var, onvalue=1, offvalue=0)
        mark_checkbutton_video.grid(row=1, column=3, pady=5, sticky=W)
        self.attorney_var = IntVar()
        mark_checkbutton_attorney = Checkbutton(root, text="委托", variable=self.attorney_var, onvalue=1, offvalue=0)
        mark_checkbutton_attorney.grid(row=1, column=4, pady=5, sticky=W)
        self.promotion_var = IntVar()
        mark_checkbutton_promotion = Checkbutton(root, text="速销", variable=self.promotion_var, onvalue=1, offvalue=0)
        mark_checkbutton_promotion.grid(row=2, column=2, pady=5, sticky=W)
        self.key_var = IntVar()
        mark_checkbutton_key = Checkbutton(root, text="钥匙", variable=self.key_var, onvalue=1, offvalue=0)
        mark_checkbutton_key.grid(row=2, column=3, pady=5, sticky=W)
        self.sole_var = IntVar()
        mark_checkbutton_key = Checkbutton(root, text="独家", variable=self.sole_var, onvalue=1, offvalue=0)
        mark_checkbutton_key.grid(row=2, column=4, pady=5, sticky=W)
        self.entertained_var = IntVar()
        mark_checkbutton_key = Checkbutton(root, text="封盘", variable=self.entertained_var, onvalue=1, offvalue=0)
        mark_checkbutton_key.grid(row=3, column=2, pady=5, sticky=W)
        self.bargaining_var = IntVar()
        mark_checkbutton_key = Checkbutton(root, text="议价", variable=self.bargaining_var, onvalue=1, offvalue=0)
        mark_checkbutton_key.grid(row=3, column=3, pady=5, sticky=W)

        environment = Label(root, text='环境')
        environment.grid(row=2, column=0, pady=5, sticky=E)
        self.environment_loop = ttk.Combobox(root, width=20)
        self.environment_loop['value'] = ('beta', 'prod')
        self.environment_loop['state'] = 'readonly'
        self.environment_loop.current(0)
        self.environment_loop.grid(row=2, column=1, pady=5, sticky='NW')

        erp_username_input = Label(root, text='账号')
        erp_username_input.grid(row=3, column=0, pady=5, sticky=E)
        self.erp_username_input_loop_text = StringVar()
        self.erp_username_input_loop = Entry(root, width=20, textvariable=self.erp_username_input_loop_text)
        self.erp_username_input_loop_text.set(self.data["username"])
        self.erp_username_input_loop.grid(row=3, column=1, pady=5, sticky='EW')

        password_input = Label(root, text='密码')
        password_input.grid(row=4, column=0, pady=5, sticky=E)
        self.password_input_loop_text = StringVar()
        self.password_input_loop = Entry(root, width=20, textvariable=self.password_input_loop_text, show='*')
        self.password_input_loop_text.set(self.data["password"])
        self.password_input_loop.grid(row=4, column=1, pady=5, sticky='EW')

        city_code_input = Label(root, text='城市编码')
        city_code_input.grid(row=5, column=0, pady=5, sticky=E)
        self.city_code_input_loop_text = StringVar()
        self.city_code_input_loop = Entry(root, width=20, textvariable=self.city_code_input_loop_text)
        self.city_code_input_loop_text.set(self.data["city_code"])
        self.city_code_input_loop.grid(row=5, column=1, pady=5, sticky='EW')

        brand_id_input = Label(root, text='品牌ID')
        brand_id_input.grid(row=6, column=0, pady=5, sticky=E)
        self.brand_id_input_loop_text = StringVar()
        self.brand_id_input_loop = Entry(root, width=20, textvariable=self.brand_id_input_loop_text)
        self.brand_id_input_loop_text.set(self.data["brand_id"])
        self.brand_id_input_loop.grid(row=6, column=1, pady=5, sticky='EW')

        organ_id_input = Label(root, text='分公司ID')
        organ_id_input.grid(row=7, column=0, pady=5, sticky=E)
        self.organ_id_input_loop_text = StringVar()
        self.organ_id_input_loop = Entry(root, width=20, textvariable=self.organ_id_input_loop_text)
        self.organ_id_input_loop_text.set(self.data["organ_id"])
        self.organ_id_input_loop.grid(row=7, column=1, pady=5, sticky='EW')

        estate_code_input = Label(root, text='小区ID')
        estate_code_input.grid(row=8, column=0, pady=5, sticky=E)
        self.estate_code_input_loop_text = StringVar()
        self.estate_code_input_loop = Entry(root, width=20, textvariable=self.organ_id_input_loop_text)
        self.estate_code_input_loop_text.set(self.data["organ_id"])
        self.estate_code_input_loop.grid(row=8, column=1, pady=5, sticky='EW')

        remember = Label(root, text='保存信息')
        remember.grid(row=4, column=2, pady=5, sticky=E)

        self.erp_username_var = IntVar()
        erp_username_var_button = Checkbutton(root, text="账号", variable=self.erp_username_var, onvalue=1, offvalue=0)
        erp_username_var_button.grid(row=5, column=2, pady=5, sticky=W)

        self.password_var = IntVar()
        password_var_button = Checkbutton(root, text="密码", variable=self.password_var, onvalue=1, offvalue=0)
        password_var_button.grid(row=5, column=3, sticky=W)

        self.city_code_var = IntVar()
        city_code_var_button = Checkbutton(root, text="城市", variable=self.city_code_var, onvalue=1, offvalue=0)
        city_code_var_button.grid(row=5, column=4, sticky=W)

        self.brand_id_var = IntVar()
        brand_id_var_button = Checkbutton(root, text="品牌", variable=self.brand_id_var, onvalue=1, offvalue=0)
        brand_id_var_button.grid(row=6, column=2, sticky=W)

        self.organ_id_var = IntVar()
        organ_id_var_button = Checkbutton(root, text="公司", variable=self.organ_id_var, onvalue=1, offvalue=0)
        organ_id_var_button.grid(row=6, column=3, sticky=W)

        self.estate_code_var = IntVar()
        estate_code_var_button = Checkbutton(root, text="小区", variable=self.estate_code_var, onvalue=1, offvalue=0)
        estate_code_var_button.grid(row=6, column=4, sticky=W)

        tips = Label(root, text='注意：点击查询才能记住信息')
        tips.config(fg="red")
        tips.grid(row=9, column=1, sticky=W)

        Button(root, width=8, height=1, text="新增房源", command="").grid(row=10, column=1, columnspan=2)
        Button(root, width=8, text="删除保存", command="").grid(row=10, column=2, columnspan=2)
