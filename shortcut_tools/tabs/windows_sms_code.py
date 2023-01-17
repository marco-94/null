# -*- coding: utf-8 -*-
"""
查询验证码
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


class WindowsSmsCode:
    data = get_config.get_config()

    interface_address_loop_text = None
    ops_username_input_loop_text = None
    ops_username_input_loop = None
    erp_username_input_loop_text = None
    erp_username_input_loop = None
    password_input_loop_text = None
    password_input_loop = None
    environment_loop = None
    ops_username_var = None
    erp_username_var = None
    password_var = None

    def windows_sms_code(self, root):
        """
        窗口1元素
        :return:
        """
        interface_address = Label(root, text='查询接口')
        interface_address.grid(row=0, column=0, pady=5, sticky=E)
        self.interface_address_loop_text = StringVar()
        interface_address_loop = Entry(root, width=40, textvariable=self.interface_address_loop_text)
        self.interface_address_loop_text.set(self.data["select_url"])
        interface_address_loop.grid(row=0, column=1, pady=5, sticky='EW')

        ops_username_input = Label(root, text='待查询账号')
        ops_username_input.grid(row=1, column=0, pady=5, sticky=E)
        self.ops_username_input_loop_text = StringVar()
        self.ops_username_input_loop = Entry(root, width=40, textvariable=self.ops_username_input_loop_text)
        self.ops_username_input_loop_text.set(self.data["phone"])
        self.ops_username_input_loop.grid(row=1, column=1, pady=5, sticky='EW')

        self.ops_username_var = IntVar()
        ops_username_var_button = Checkbutton(root, text="记住账号", variable=self.ops_username_var, onvalue=1, offvalue=0)
        ops_username_var_button.grid(row=1, column=2, pady=5, sticky=W)

        erp_username_input = Label(root, text='ERP账号')
        erp_username_input.grid(row=2, column=0, pady=5, sticky=E)
        self.erp_username_input_loop_text = StringVar()
        self.erp_username_input_loop = Entry(root, width=40, textvariable=self.erp_username_input_loop_text)
        self.erp_username_input_loop_text.set(self.data["username"])
        self.erp_username_input_loop.grid(row=2, column=1, pady=5, sticky='EW')

        self.erp_username_var = IntVar()
        erp_username_var_button = Checkbutton(root, text="记住账号", variable=self.erp_username_var, onvalue=1, offvalue=0)
        erp_username_var_button.grid(row=2, column=2, pady=5, sticky=W)

        password_input = Label(root, text='密码')
        password_input.grid(row=3, column=0, pady=5, sticky=E)
        self.password_input_loop_text = StringVar()
        self.password_input_loop = Entry(root, width=40, textvariable=self.password_input_loop_text, show='*')
        self.password_input_loop_text.set(self.data["password"])
        self.password_input_loop.grid(row=3, column=1, pady=5, sticky='EW')

        self.password_var = IntVar()
        password_var_button = Checkbutton(root, text="记住密码", variable=self.password_var, onvalue=1, offvalue=0)
        password_var_button.grid(row=3, column=2, sticky=W)

        environment = Label(root, text='环境')
        environment.grid(row=4, column=0, pady=5, sticky=E)
        self.environment_loop = ttk.Combobox(root, width=40)
        self.environment_loop['value'] = ('beta', 'prod')
        self.environment_loop['state'] = 'readonly'
        self.environment_loop.current(0)
        self.environment_loop.grid(row=4, column=1, pady=5, sticky='NW')

        tips = Label(root, text='注意：只能查询五分钟之内的验证码，点击查询才能记住信息')
        tips.config(fg="red")
        tips.grid(row=5, column=0, sticky=W, columnspan=2)

        Button(root, width=8, height=1, text="查询", command=self.events_status).grid(row=6, column=0, columnspan=2)
        Button(root, width=8, text="取消记住", command=self.delete_input).grid(row=6, column=1, columnspan=2)

    @staticmethod
    def show_code(code):
        """
        展示验证码
        :param code:
        :return:
        """
        show_code_root = Tk()
        show_code_root.title('验证码')
        show_code_root.geometry('350x100')
        show_code_root.resizable(False, False)
        screen_height = show_code_root.winfo_screenheight()
        screen_width = show_code_root.winfo_screenwidth()
        show_code_root.update_idletasks()
        show_code_root.geometry('%dx%d+%d+%d' % (
            show_code_root.winfo_width(), show_code_root.winfo_height(),
            (screen_width - show_code_root.winfo_width()) / 2,
            (screen_height - show_code_root.winfo_height()) / 2))
        show_code_root.deiconify()
        show_code_text = Text(show_code_root, font=('验证码', 20, 'bold'))
        show_code_text.insert(INSERT, '\n')
        show_code_text.insert(INSERT, '\t' + code)
        show_code_text.config(state='disabled')
        show_code_text.pack()
        show_code_root.mainloop()

    def delete_input(self):
        """
        删除保存的信息
        :return:
        """
        self.ops_username_input_loop.delete(0, 'end')
        self.erp_username_input_loop.delete(0, 'end')
        self.password_input_loop.delete(0, 'end')
        yaml_update.UpdateYaml().up_yml("phone", "")
        yaml_update.UpdateYaml().up_yml("username", "")
        yaml_update.UpdateYaml().up_yml("password", "")

    def get_public_key(self):
        """
        组装公钥
        :return: 公钥
        """
        public_key = False
        for _ in range(1):
            # 获取公钥
            domain = base_function.PublicFunction(self).get_domain(self.environment_loop.get())
            get_public_key_response = requests.get(url=domain + self.data["get_public_key_url"])

            # 如果接口报错或返回错误，则提示错误，并结束退出
            if get_public_key_response.status_code != 200 or get_public_key_response.json()['code'] != '200':
                base_function.DefaultConfiguration.show_response_error(get_public_key_response)
                break

            public_keys = get_public_key_response.json()["data"]
            # 替换公钥字符"-"和"_"
            keys = public_keys.replace("-", "+")
            rsa_keys = keys.replace("_", "/")
            # 组成真正的公钥
            public_key = '-----BEGIN PUBLIC KEY-----\n' + rsa_keys + '\n-----END PUBLIC KEY-----'
        return public_key

    def encrpt(self, password, public_key):
        """
        密码加密
        :param password: 明文密码
        :param public_key: 组装好的公钥
        :return: 已加密的密码
        """
        psd = False
        if self.get_public_key():
            rsa_key = RSA.importKey(public_key)
            cipher = PKCS1_v1_5.new(rsa_key)
            cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
            psd = cipher_text.decode()
        return psd

    def get_access_token(self, username, password):
        """
        登录erp账号
        :param username:
        :param password:
        :return:
        """
        access_token = False
        password = self.encrpt(password, self.get_public_key())
        domain = base_function.PublicFunction(self).get_domain(self.environment_loop.get())
        if password:
            for _ in range(1):
                headers = {"Content-Type": "application/json"}
                authorize_params = {
                    "scope": "openid",
                    "response_type": "code",
                    "client_id": "585014642717982720",
                    "redirect_url": "https://localhost:8443/uac/",
                    "state": "e268443e43d93dab7ebef303bbe9642f",
                    "auth_type": "BPassword"
                }
                authorize_response = requests.get(url=domain + self.data["authorize_url"],
                                                  params=authorize_params)

                # 如果接口报错或返回错误，则提示错误，并结束退出
                if authorize_response.status_code != 200 or authorize_response.json()['code'] != '200':
                    base_function.DefaultConfiguration.show_response_error(authorize_response)
                    break

                code_key = authorize_response.json()['data']['code_key']

                execute_json = {
                    "c_name": "BPasswordLogin",
                    "input_param": {
                        "regionCode": "86",
                        "username": username,
                        "password": password
                    },
                    "code_key": code_key
                }

                execute_response = requests.post(url=domain + self.data["execute_url"],
                                                 headers=headers,
                                                 json=execute_json)

                # 如果接口报错或返回错误，则提示错误，并结束退出
                if execute_response.status_code != 200 or execute_response.json()['code'] != '200':
                    base_function.DefaultConfiguration.show_response_error(execute_response)
                    break

                code = execute_response.json()['data']['code']
                state = execute_response.json()['data']['state']
                user_id = execute_response.json()['data']['userId']
                access_json = {
                    "client_id": 585014642717982720,
                    "client_secret": "b9c7398eebe909a01603d5fba2c55086",
                    "code": code,
                    "state": state,
                    "userId": user_id
                }
                access_token_response = requests.post(url=domain + self.data["access_token_url"],
                                                      headers=headers,
                                                      json=access_json)

                # 如果接口报错或返回错误，则提示错误，并结束退出
                if access_token_response.status_code != 200 or access_token_response.json()['code'] != '200':
                    base_function.DefaultConfiguration.show_response_error(access_token_response)
                    break

                access_token = access_token_response.json()['data']['access_token']
        return access_token

    def events_status(self):
        """
        查询验证码部分，只查询五分钟内的验证码
        :return:
        """
        domain = base_function.PublicFunction(self).get_domain(self.environment_loop.get())
        try:
            for _ in range(1):
                # 判断输入框是否为空或非法输入
                # 手机号正则
                pattern = re.compile(R"[1][3456789]\d{9}")
                # 输入字符串是否包含中文正则
                chinese_pattern = re.compile(u'[\u4e00-\u9fa5]')

                if self.interface_address_loop_text.get() == "":
                    messagebox.askokcancel("警告", "查询接口信息不可为空")
                    break
                elif self.ops_username_input_loop_text.get() == "":
                    messagebox.askokcancel("警告", "待查询账号信息不可为空")
                    break
                elif self.erp_username_input_loop_text.get() == "":
                    messagebox.askokcancel("警告", "ERP账号信息不可为空")
                    break
                elif self.password_input_loop_text.get() == "":
                    messagebox.askokcancel("警告", "密码信息不可为空")
                    break
                elif not pattern.match(self.ops_username_input_loop_text.get()):
                    messagebox.askokcancel("警告", "待查询账号格式不正确")
                    break
                elif not pattern.match(self.erp_username_input_loop_text.get()):
                    messagebox.askokcancel("警告", "ERP账号格式不正确")
                    break
                elif chinese_pattern.match(self.password_input_loop_text.get()):
                    messagebox.askokcancel("警告", "密码格式不正确")
                    break
                elif len(self.password_input_loop_text.get()) < 8:
                    messagebox.askokcancel("警告", "密码长度不正确")
                    break

                # 保存查询信息
                if self.ops_username_var.get() == 1:
                    yaml_update.UpdateYaml().up_yml("phone", str(self.ops_username_input_loop_text.get()))
                if self.erp_username_var.get() == 1:
                    yaml_update.UpdateYaml().up_yml("username", self.erp_username_input_loop_text.get())
                if self.password_var.get() == 1:
                    yaml_update.UpdateYaml().up_yml("password", self.password_input_loop_text.get())

                # 判断正确之后，先给个提示信息
                base_function.DefaultConfiguration(self).show_message("查询中，请等待！")

                url = domain + self.interface_address_loop_text.get()
                username = self.erp_username_input_loop_text.get()
                password = self.password_input_loop_text.get()

                token = self.get_access_token(username, password)

                # token正常获取到才执行
                if token:
                    events_status_headers = {"authorization": token}

                    events_status_value = {
                        "receiverPhone": self.ops_username_input_loop_text.get(),
                        "smsBusinessType": 2,
                        "condition": {
                            "createTimeEnd": base_function.DefaultConfiguration.get_time()[0],
                            "createTimeStart": base_function.DefaultConfiguration.get_time()[1]},
                        "pageNo": 1,
                        "rowCntPerPage": 1
                    }

                    events_status_response = requests.post(url=url,
                                                           json=events_status_value,
                                                           headers=events_status_headers).json()

                    if events_status_response["data"]["list"] is None:
                        messagebox.askokcancel("查询结果", "验证码查询为空")
                        break
                    else:
                        code = eval(events_status_response["data"]["list"][0]["sendText"])["code"]
                        base_function.DefaultConfiguration.show_result(code, "验证码")
                        return code
        except KeyError:
            pass
