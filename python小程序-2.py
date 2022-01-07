# -*- coding: utf-8 -*-
import time
from tkinter import *
from tkinter import ttk
import requests
from tkinter import messagebox

root = Tk()
root.title('设备信息查询')
root.geometry('700x400')

interface_address = Label(root, text='URL')
interface_address.grid(row=0, column=0, pady=5, sticky=E)
interface_address_loop_text = StringVar()
interface_address_loop = Entry(root, width=70, textvariable=interface_address_loop_text)
interface_address_loop_text.set('https://rd.bosma.cn/bosma-smart-frontend/api/ipcdata/getEventWithTagByStatus')
interface_address_loop.grid(row=0, column=1, pady=5, sticky='EW')

token_input = Label(root, text='TOKEN')
token_input.grid(row=1, column=0, pady=5, sticky=E)
token_input_loop_text = StringVar()
token_input_loop = Entry(root, width=50, textvariable=token_input_loop_text)
token_input_loop_text.set('')
token_input_loop.grid(row=1, column=1, pady=5, sticky='EW')

device_id = Label(root, text='设备ID')
device_id.grid(row=2, column=0, pady=5, sticky=E)
device_id_loop_text = StringVar()
device_id_loop = Entry(root, width=50, textvariable=device_id_loop_text)
device_id_loop_text.set('')
device_id_loop.grid(row=2, column=1, pady=5, sticky='EW')

alarm_type = Label(root, text='报警类型')
alarm_type.grid(row=3, column=0, pady=5, sticky=E)
alarm_type_loop_text = StringVar()
alarm_type_loop = Entry(root, width=50, textvariable=alarm_type_loop_text)
alarm_type_loop_text.set('10,20,30,40,50,60,95,103')
alarm_type_loop.grid(row=3, column=1, pady=5, sticky='EW')

time_zone_offset_minutes = Label(root, text='时区偏移分钟数')
time_zone_offset_minutes.grid(row=4, column=0, pady=5, sticky=E)
time_zone_offset_minutes_loop_text = StringVar()
time_zone_offset_minutes_loop = Entry(root, width=50, textvariable=time_zone_offset_minutes_loop_text)
time_zone_offset_minutes_loop_text.set('480')
time_zone_offset_minutes_loop.grid(row=4, column=1, pady=5, sticky='EW')

is_local_status = Label(root, text='是否查询本地状态')
is_local_status.grid(row=5, column=0, pady=5, sticky=E)
is_local_status_loop = ttk.Combobox(root, width=70)
is_local_status_loop['value'] = ('是', '否')
is_local_status_loop['state'] = 'readonly'
is_local_status_loop.current(0)
is_local_status_loop.grid(row=5, column=1, pady=5, sticky='NW')

is_cloud_status = Label(root, text='是否查询云存储状态')
is_cloud_status.grid(row=6, column=0, pady=5, sticky=E)
is_cloud_status_loop = ttk.Combobox(root, width=70)
is_cloud_status_loop['value'] = ('是', '否')
is_cloud_status_loop['state'] = 'readonly'
is_cloud_status_loop.current(0)
is_cloud_status_loop.grid(row=6, column=1, pady=5, sticky='NW')

page_size = Label(root, text='每页多少条')
page_size.grid(row=7, column=0, pady=5, sticky=E)
page_size_loop_text = StringVar()
page_size_loop = Entry(root, width=50, textvariable=page_size_loop_text)
page_size_loop_text.set('100')
page_size_loop.grid(row=7, column=1, pady=5, sticky='EW')

page_current = Label(root, text='第几页')
page_current.grid(row=8, column=0, pady=5, sticky=E)
page_current_loop_text = StringVar()
page_current_loop = Entry(root, width=50, textvariable=page_current_loop_text)
page_current_loop_text.set('1')
page_current_loop.grid(row=8, column=1, pady=5, sticky='EW')

app_version = Label(root, text='程序版本')
app_version.grid(row=9, column=0, pady=5, sticky=E)
app_version_loop_text = StringVar()
app_version_loop = Entry(root, width=50, textvariable=app_version_loop_text)
app_version_loop_text.set('2.3.0 test_build005')
app_version_loop.grid(row=9, column=1, pady=5, sticky='EW')


def center_window():
    """窗口居中"""
    screen_height = root.winfo_screenheight()
    screen_width = root.winfo_screenwidth()
    root.update_idletasks()
    root.geometry('%dx%d+%d+%d' % (root.winfo_width(), root.winfo_height(), (screen_width - root.winfo_width()) / 2,
                                   (screen_height - root.winfo_height()) / 2))
    root.deiconify()


center_window()


def clear_response():
    """
    清空文件数据
    'r'：读
    'w'：写
    'a'：追加
    'r+' == r+w（可读可写，文件若不存在就报错(IOError)）
    'w+' == w+r（可读可写，文件若不存在就创建）
    'a+' ==a+r（可追加可写，文件若不存在就创建）
    :return:
    """
    fw = open("response_data.txt", 'w')
    fw.truncate()


def save_response(key, value1="", value2="", value3=""):
    """
    保存数据到文件
    'r'：读
    'w'：写
    'a'：追加
    'r+' == r+w（可读可写，文件若不存在就报错(IOError)）
    'w+' == w+r（可读可写，文件若不存在就创建）
    'a+' ==a+r（可追加可写，文件若不存在就创建）
    :return:
    """
    fw = open("response_data.txt", 'a+')
    fw.write(key + value1 + value2 + value3)  # 将字符串写入文件中
    value3.rstrip("\n")  # 为去除行尾换行符
    fw.write("\n")  # 换行


def events_status():
    try:
        url = interface_address_loop_text.get()

        events_status_headers = {"appVersion": app_version_loop_text.get()}

        events_status_value = {
            "token": token_input_loop_text.get(),
            "timeZoneOffsetMinutes": time_zone_offset_minutes_loop_text.get(),
            "devicePids": device_id_loop_text.get(),
            "alarmType": alarm_type_loop_text.get(),
            "localStatus": is_local_status_loop.get(),
            "cloudStatus": is_cloud_status_loop.get(),
            "pageSize": page_size_loop_text.get(),
            "pageCurrent": page_current_loop.get()
        }

        # 判断是否需要查询本地状态
        if is_local_status_loop.get() == "是":
            events_status_value["localStatus"] = 1
        else:
            del events_status_value["localStatus"]

        # 判断是否需要查询云存储状态
        if is_cloud_status_loop.get() == "是":
            events_status_value["cloudStatus"] = 1
        else:
            del events_status_value["cloudStatus"]

        # 判断是否有输入为空
        if "" in events_status_value.values() or "" in events_status_headers.values():
            messagebox.askokcancel("警告", "输入信息不可为空")

        response = requests.post(url, headers=events_status_headers, data=events_status_value).json()
        data_list = response["data"]["data"]
        sort_date = response["data"]["sortDate"]

        print("token", token_input_loop_text.get())
        print("devicePids", device_id_loop_text.get())
        print("sortDate：", sort_date)

        if len(data_list) != 0:
            print("全部数据")

        clear_response()
        save_response("全部数据-----")
        save_response("token：", token_input_loop_text.get())
        save_response("devicePids：", device_id_loop_text.get())
        save_response("sortDate：", sort_date)

        response_list = []
        for i in range(len(data_list)):
            dt = response["data"]["data"][i]["dt"]
            tm = response["data"]["data"][i]["tm"]
            data_time = dt + "  " + tm
            local_status = response["data"]["data"][i]["localStatus"]
            cloud_status = response["data"]["data"][i]["cloudStatus"]
            play_way = response["data"]["data"][i]["playWay"]

            print("第" + str(i + 1) + "个-------")
            print("dt + tm：", data_time)
            print("localStatus：", local_status)
            print("cloudStatus：", cloud_status)
            print("playWay：", play_way)

            save_response("第", str(i + 1), "个-------")
            save_response("dt + tm：", dt, "  ", tm)
            save_response("localStatus：", str(local_status))
            save_response("cloudStatus：", str(cloud_status))
            save_response("playWay：", play_way)

            if local_status == 1 and play_way != "local" or local_status == 0 and cloud_status == 1 and play_way != "cloud" or local_status == 0 and cloud_status == 2 and play_way != "cloud" or local_status == -1 and cloud_status == -1 and play_way is not None:
                response_json = {"datatime": data_time,
                                 "localStatus": local_status,
                                 "cloudStatus": cloud_status,
                                 "playWay": play_way}
                response_list.append(response_json)
        time.sleep(1)
        if len(response_list) == 0:
            messagebox.askokcancel("查询结果", "数据正常")
        else:
            print("错误数据：", response_list)
            save_response("错误数据：", str(response_list))
            messagebox.askokcancel("查询结果", "查询完成，存在错误数据")
    except KeyError:
        pass


button1 = Button(root, width=20, height=2, text="查询", command=events_status).grid(row=10, columnspan=2)

root.mainloop()
