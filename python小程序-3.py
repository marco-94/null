# -*- coding: utf-8 -*-
import re
import time
from tkinter import *
from tkinter import ttk
import requests
from tkinter import messagebox
import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

# 为了方便维护，全部接口地址写一起
# 查询验证码接口
select_url = "/ops.web.api/sms/api/v1/task/page/send"
# 获取公钥接口
get_public_key_url = "/sso/security/k"
# 登录的三个接口
authorize_url = "/sso/oidc/authorize/"
execute_url = "/sso/oidc/execute/"
access_token_url = "/sso/oidc/accessToken/"


root = Tk()
root.title('OPS登录验证码查询')
root.geometry('400x300')

interface_address = Label(root, text='查询接口')
interface_address.grid(row=0, column=0, pady=5, sticky=E)
interface_address_loop_text = StringVar()
interface_address_loop = Entry(root, width=40, textvariable=interface_address_loop_text)
interface_address_loop_text.set(select_url)
interface_address_loop.grid(row=0, column=1, pady=5, sticky='EW')

ops_username_input = Label(root, text='待查询账号')
ops_username_input.grid(row=1, column=0, pady=5, sticky=E)
ops_username_input_loop_text = StringVar()
ops_username_input_loop = Entry(root, width=40, textvariable=ops_username_input_loop_text)
ops_username_input_loop_text.set('')
ops_username_input_loop.grid(row=1, column=1, pady=5, sticky='EW')

erp_username_input = Label(root, text='ERP账号')
erp_username_input.grid(row=2, column=0, pady=5, sticky=E)
erp_username_input_loop_text = StringVar()
erp_username_input_loop = Entry(root, width=40, textvariable=erp_username_input_loop_text)
erp_username_input_loop_text.set('')
erp_username_input_loop.grid(row=2, column=1, pady=5, sticky='EW')

password_input = Label(root, text='密码')
password_input.grid(row=3, column=0, pady=5, sticky=E)
password_input_loop_text = StringVar()
password_input_loop = Entry(root, width=40, textvariable=password_input_loop_text, show='*')
password_input_loop_text.set('')
password_input_loop.grid(row=3, column=1, pady=5, sticky='EW')

environment = Label(root, text='环境')
environment.grid(row=4, column=0, pady=5, sticky=E)
environment_loop = ttk.Combobox(root, width=40)
environment_loop['value'] = ('beta', 'prod')
environment_loop['state'] = 'readonly'
environment_loop.current(0)
environment_loop.grid(row=4, column=1, pady=5, sticky='NW')

tips = Label(root, text='注意：只能查询五分钟之内的验证码')
tips.grid(row=5, column=1, sticky=W)


def center_window():
    """窗口居中"""
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()
    root.update_idletasks()
    root.geometry('%dx%d+%d+%d' % (root.winfo_width(), root.winfo_height(), (screen_width - root.winfo_width()) / 2,
                                   (screen_height - root.winfo_height()) / 2))
    root.deiconify()


center_window()


def get_time():
    """
    获取当前时间的时间戳和过去五分钟的时间戳
    """
    current_time = round(time.time() * 1000)
    past_time = round(time.time() * 1000 - 300000)
    return current_time, past_time


def get_domain():
    """
    获取查询环境域名
    :return:
    """
    if environment_loop.get() == "beta":
        domain = "https://api-beta.yjzf.com"
    else:
        domain = "https://api.yjzf.com"
    return domain


def get_public_key():
    """
    组装公钥
    :return: 公钥
    """
    # 获取公钥
    get_public_key_response = requests.get(url=get_domain() + get_public_key_url).json()
    public_keys = get_public_key_response["data"]
    # 替换公钥字符"-"和"_"
    keys = public_keys.replace("-", "+")
    rsa_keys = keys.replace("_", "/")
    # 组成真正的公钥
    public_key = '-----BEGIN PUBLIC KEY-----\n' + rsa_keys + '\n-----END PUBLIC KEY-----'
    return public_key


def encrpt(password, public_key):
    """
    密码加密
    :param password: 明文密码
    :param public_key: 组装好的公钥
    :return: 已加密的密码
    """
    rsa_key = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(rsa_key)
    cipher_text = base64.b64encode(cipher.encrypt(password.encode()))
    return cipher_text.decode()


def get_access_token(username, password):
    """
    登录erp账号
    :param username:
    :param password:
    :return:
    """
    access_token = ""
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
        authorize_response = requests.get(url=get_domain() + authorize_url, params=authorize_params).json()
        code_key = authorize_response['data']['code_key']
        execute_json = {
            "c_name": "BPasswordLogin",
            "input_param": {
                "regionCode": "86",
                "username": username,
                "password": encrpt(password, get_public_key())
            },
            "code_key": code_key
        }

        execute_response = requests.post(url=get_domain() + execute_url, headers=headers,
                                         json=execute_json).json()

        # 账号密码错误时，返回警告，并直接结束
        if execute_response['code'] == "4000031001":
            messagebox.askokcancel("警告", execute_response['msg'])
            break

        code = execute_response['data']['code']
        state = execute_response['data']['state']
        user_id = execute_response['data']['userId']
        access_json = {
            "client_id": 585014642717982720,
            "client_secret": "b9c7398eebe909a01603d5fba2c55086",
            "code": code,
            "state": state,
            "userId": user_id
        }
        access_token_response = requests.post(url=get_domain() + access_token_url, headers=headers,
                                              json=access_json).json()
        access_token = access_token_response['data']['access_token']
    return access_token


def events_status():
    """
    查询验证码部分，只查询五分钟内的验证码
    :return:
    """
    try:
        for _ in range(1):
            # 判断输入框是否为空或非法输入
            # 手机号正则
            pattern = re.compile(R"[1][3456789]\d{9}")
            # 输入字符串是否包含中文正则
            chinese_pattern = re.compile(u'[\u4e00-\u9fa5]')

            if interface_address_loop_text.get() == "":
                messagebox.askokcancel("警告", "查询接口信息不可为空")
                break
            elif ops_username_input_loop_text.get() == "":
                messagebox.askokcancel("警告", "待查询账号信息不可为空")
                break
            elif erp_username_input_loop_text.get() == "":
                messagebox.askokcancel("警告", "ERP账号信息不可为空")
                break
            elif password_input_loop_text.get() == "":
                messagebox.askokcancel("警告", "密码信息不可为空")
                break
            elif not pattern.match(ops_username_input_loop_text.get()):
                messagebox.askokcancel("警告", "待查询账号格式不正确")
                break
            elif not pattern.match(erp_username_input_loop_text.get()):
                messagebox.askokcancel("警告", "ERP账号格式不正确")
                break
            elif chinese_pattern.match(password_input_loop_text.get()):
                messagebox.askokcancel("警告", "密码格式不正确")
                break
            elif len(password_input_loop_text.get())<8:
                messagebox.askokcancel("警告", "密码长度不正确")
                break

            url = get_domain() + interface_address_loop_text.get()
            username = erp_username_input_loop_text.get()
            password = password_input_loop_text.get()

            events_status_headers = {"authorization": get_access_token(username, password)}

            if events_status_headers["authorization"] == "":
                break

            events_status_value = {
                "receiverPhone": ops_username_input_loop_text.get(),
                "smsBusinessType": 2,
                "condition": {
                    "createTimeEnd": get_time()[0],
                    "createTimeStart": get_time()[1]},
                "pageNo": 1,
                "rowCntPerPage": 10
            }

            events_status_response = requests.post(url=url, json=events_status_value,
                                                   headers=events_status_headers).json()

            if events_status_response["data"]["list"] is None:
                messagebox.askokcancel("查询结果", "验证码查询为空")
                break
            else:
                list_len = int(len(events_status_response["data"]["list"]))
                list_code = []
                for i in range(list_len):
                    try:
                        code = eval(events_status_response["data"]["list"][i]["sendText"])["code"]
                        list_code.append(code)
                    except:
                        continue
                code = list_code[0]
                messagebox.askokcancel("验证码", code)
                return code
    except KeyError:
        pass


button1 = Button(root, width=20, height=2, text="查询", command=events_status).grid(row=10, columnspan=2)

root.mainloop()
