#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# **********************************************************
# * Author        : huangtao
# * Email         : huangtao@yimian.me
# * Create time   : 2018/4/17 下午2:34
# * Last modified : 2018/4/17 下午2:34
# * Filename      : util.py.py
# * Description   : 公共方法
# **********************************************************

import re
import sys


def clearHtml(str):
    if '☞' in str:
        str = str.replace('☞', '<')
    res = re.sub(r'<(?!img).*?>', '',str)
    res = re.sub(r'<img.*?alt="','',res)
    res = re.sub(r'<[^>]+>','',res)
    res = res.replace('">',"")
    return res

import pygame  # pip install pygame


def playMusic(filename, loops=0, start=0.0, value=0.5):
    """
    :param filename: 文件名
    :param loops: 循环次数
    :param start: 从多少秒开始播放
    :param value: 设置播放的音量，音量value的范围为0.0到1.0
    :return:
    """
    flag = False  # 是否播放过
    pygame.mixer.init()  # 音乐模块初始化
    while 1:
        if flag == 0:
            pygame.mixer.music.load(filename)
            # pygame.mixer.music.play(loops=0, start=0.0) loops和start分别代表重复的次数和开始播放的位置。
            pygame.mixer.music.play(loops=loops, start=start)
            pygame.mixer.music.set_volume(value)  # 来设置播放的音量，音量value的范围为0.0到1.0。
        if pygame.mixer.music.get_busy() == True:
            flag = True
        else:
            if flag:
                pygame.mixer.music.stop()  # 停止播放
                break
