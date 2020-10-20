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


def read_image(imagePath):
    image = cv2.imdecode(np.fromfile(imagePath, dtype=np.uint8), -1)
    return image


def judge_gray_value_proper(image):
    ROI = image[0:1023, 128:1151]
    mean, std = cv2.meanStdDev(ROI)
    if mean < MeanValThresh[0]:
        isProper = -1       # 图像灰度值太暗
    elif mean > MeanValThresh[1]:
        isProper = 0        # 图像灰度值太亮
    else:
        isProper = 1        # 图像灰度值合适
    return isProper


# 图像路径
imagePath = 'E:/原木视觉测量/原木测量图像保存/圆木图像01/1576226614501.bmp'
# 读入图像
img = read_image(imagePath)
# 判断图像亮度是否合适
isOK = judge_gray_value_proper(img)
print(isOK)
#显示图像
cv2.imshow('image', img)
K = cv2.waitKey(0)

