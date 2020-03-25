# -*- coding: UTF-8 -*-
import os
import cv2
import time


def picvideo(path, size):
    filelist = os.listdir(path)
    fps = 1
    file_path = r"C:/Users/24540/Desktop/file/picture" + "-" + time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime()) + ".mp4"
    video = cv2.VideoWriter(file_path, 0x00000021, fps, size)
    for item in filelist:
        if item.endswith('.jpg') or item.endswith('.png'):
            item = path + '/' + item
            img = cv2.imread(item)
            video.write(img)
    video.release()
picvideo(r'C:/Users/24540/Desktop/file/picture/',(1920,1080))
