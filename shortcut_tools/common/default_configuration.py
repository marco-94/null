# -*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from shortcut_tools.tabs import windows_add_property, windows_three, windows_sms_code


# 定义默认配置
class DefaultConfiguration:
    def __init__(self, root):
        self.root = root

    def menu_bar(self):
        """
        定义工具栏
        :param :
        :return:
        """

        menu_tab = ttk.Notebook(self.root)
        menu_tab.pack(fill=tk.BOTH, expand=True)

        windows_sms_code_frame = tk.Frame(self.root)
        windows_two_frame = tk.Frame(self.root)
        windows_three_frame = tk.Frame(self.root)

        menu_tab.add(windows_sms_code_frame, text="验证码查询")
        menu_tab.add(windows_two_frame, text="新增房源")
        menu_tab.add(windows_three_frame, text="工具三")

        windows_sms_code.WindowsSmsCode().windows_sms_code(windows_sms_code_frame)
        windows_add_property.WindowsAddProperty().windows_add_property(windows_two_frame)
        windows_three.WindowsThree.windows_three(windows_three_frame)

    def center_window(self):
        """窗口居中"""
        screen_height = self.root.winfo_screenheight()
        screen_width = self.root.winfo_screenwidth()
        self.root.update_idletasks()
        self.root.geometry('%dx%d+%d+%d' % (self.root.winfo_width(),
                                            self.root.winfo_height(),
                                            (screen_width - self.root.winfo_width()) / 2,
                                            (screen_height - self.root.winfo_height()) / 2))
        self.root.deiconify()

    @staticmethod
    def show_message(message, message_type='info', timeout=2000):
        """消息提示"""

        root = tk.Tk()
        root.withdraw()
        try:
            root.after(timeout, root.destroy)
            if message_type == 'info':
                messagebox.showinfo('Info', message, master=root)
            elif message_type == 'warning':
                messagebox.showwarning('Warning', message, master=root)
            elif message_type == 'error':
                messagebox.showerror('Error', message, master=root)
        except Exception:
            pass

    @staticmethod
    def show_result(result, title=None):
        """
        显示可复制结果信息
        :return:
        """
        show_code_root = Tk()
        show_code_root.title(str(title))
        show_code_root.geometry('300x100')
        show_code_root.resizable(False, False)
        screen_height = show_code_root.winfo_screenheight()
        screen_width = show_code_root.winfo_screenwidth()
        show_code_root.update_idletasks()
        show_code_root.geometry('%dx%d+%d+%d' % (
            show_code_root.winfo_width(), show_code_root.winfo_height(),
            (screen_width - show_code_root.winfo_width()) / 2,
            (screen_height - show_code_root.winfo_height()) / 2))
        show_code_root.deiconify()
        selectable_msg = tk.Text(show_code_root, width=35, height=4, relief='flat', bg='gray94', wrap='word',
                                 font=('consolas', '20'))
        selectable_msg.insert(1.0, str(result))
        selectable_msg.configure(state='disabled')
        selectable_msg.pack(pady=30, padx=100)
        show_code_root.mainloop()

    @staticmethod
    def show_response_error(response):
        """
        展示警告信息
        :param response:
        :return:
        """
        if response.status_code != 200:
            error_content = (eval(str(response.content, encoding="utf-8")))
            error_msg = error_content["error"] + "  "
            messagebox.askokcancel("警告", error_msg + response.url)
            return False
        elif response.json()['code'] != "200":
            messagebox.askokcancel("警告", response.json()['msg'])
            return False
