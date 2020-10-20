#!/usr/bin/env python
# -- coding: utf-8 --
"""
Created by XuMin on 2020/6/18
"""

"""
Image preprocess based on OpenCV
"""

# import os
import numpy as np
# import time
import cv2

# 平均灰度值上下限
MeanValThresh = [50, 200]
# 掩膜创建参数
x = 639
y = 511
r = 450


def read_image(imagePath):
    image = cv2.imdecode(np.fromfile(imagePath, dtype=np.uint8), -1)
    return image


def is_grayImage_proper(image):
    # ROI = image[0:1023, 128:1151]
    # mean, std = cv2.meanStdDev(ROI)
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask = cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
    newImage = cv2.add(image, np.zeros(np.shape(image), dtype=np.uint8), mask=mask)
    mean = cv2.mean(newImage, mask=mask)[0]
    mean = round(mean, 2)       # 小数点后保留两位有效数字
    if MeanValThresh[0] < mean < MeanValThresh[1]:
        isProper = 1        # 灰度图像亮度合适
    elif mean < MeanValThresh[0]:
        isProper = 0        # 灰度图像太暗
    else:
        isProper = 2        # 灰度图像太亮
    return isProper


# 图像路径
# imagePath = 'E:/原木视觉测量/原木测量图像保存/圆木图像01/1576226614501.bmp'
# # 读入图像
# image = read_image(imagePath)
# # 判断图像亮度是否合适
# isOK = is_grayImage_proper(image)
# print(isOK)
# # 显示图像
# cv2.imshow('image', image)
# K = cv2.waitKey(0)
