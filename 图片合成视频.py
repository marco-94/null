# -*- coding: UTF-8 -*-
import os
import cv2
import time
from PIL import Image
from moviepy.editor import CompositeAudioClip, VideoFileClip, AudioFileClip


def pic_video(path, size):
    """
    图片合成视频
    :param path:
    :param size:
    :return:
    """
    file_list = os.listdir(path)
    fps = 1
    file_path = r"C:/Users/24540/Desktop/file/picture/" + "-" + time.strftime("%Y-%m-%d-%H_%M_%S",
                                                                              time.localtime()) + ".mp4"
    video = cv2.VideoWriter(file_path, 0x00000021, fps, size)
    for item in file_list:
        if item.endswith('.jpg') or item.endswith('.png'):
            item = path + '/' + item
            img = cv2.imread(item)
            video.write(img)
    video.release()


# pic_video(r'C:/Users/24540/Desktop/file/picture/', (1920, 1080))


def pic_to_video(img_path, video_path):
    """
    图片合成视频
    视频编码与文件格式对应关系
    MJPG == .avi
    jpeg == .mov
    mp4v == .mp4/.3gp/.asf
    :param img_path:
    :param video_path:
    :return:
    """
    images = os.listdir(img_path)
    fps = 1   # 帧率
    four_cc = cv2.VideoWriter_fourcc(*"mp4v")
    im = Image.open(img_path + images[0])
    video_writer = cv2.VideoWriter(video_path, four_cc, fps, im.size)
    for im_name in range(len(images)):
        frame = cv2.imread(img_path + images[im_name])
        video_writer.write(frame)
    video_writer.release()


# img_paths = "D:/test/yjyz/test_data/picture/environment/"
# video_paths = "D:/test/yjyz/test_data/video/video_test_mp3.mp4"
# pic_to_video(img_paths, video_paths)


def video_add_music():
    """
    给视频加背景音乐
    :return:
    """
    # 视频文件
    video_file = 'D:/test/yjyz/test_data/video/test11-video-mov.mov'
    video = VideoFileClip(video_file)
    # 音频文件
    videos = video.set_audio(AudioFileClip('C:/Users/24540/Desktop/test_mp3.mp3'))
    # 保存合成视频，注意加上参数audio_codec='aac'，否则音频无声音，部分需要指定编辑器参数codec="libx264"
    videos.write_videofile('D:/test/yjyz/test_data/video/test11-video-mov-mp3.mov', audio_codec='aac', codec="libx264")


# video_add_music()
