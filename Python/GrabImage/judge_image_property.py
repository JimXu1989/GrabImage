#!/usr/bin/env python
# -- coding: utf-8 --
"""
判断采集的激光图像与灰度图像的亮度是否满足要求
Created by XuMin on 2020/8/18
"""

"""
Image processing is based on OpenCV
"""

# import os
import numpy as np
# import time
import cv2

# 激光图像二值化阈值
LaserThresh = 200
# 激光图像平均灰度门限值
LaserMeanThresh = [10, 100]
# 激光区域面积门限值
LaserAreaThresh = [5000, 45000]

# 灰度图像平均灰度门限
GrayMeanThresh = [50, 200]

# 掩膜创建参数
x = 639
y = 511
r = 450


# 读入图像
def read_image(imagePath):
    image = cv2.imdecode(np.fromfile(imagePath, dtype=np.uint8), -1)
    return image


# 计算区域面积
def region_area(image):
    size = image.shape
    ret, BinaryReg = cv2.threshold(image, LaserThresh, 255, cv2.THRESH_BINARY)
    area = 0
    for i in range(size[0]):
        for j in range(size[1]):
            if BinaryReg[i, j] == 255:
                area = area + 1
    return area


# 由激光图像的平均灰度值与二值化后区域面积，判断激光图像亮度是否合适。
# 返回值“0”表示图像太暗，“2”表示图像太亮，“1”表示图像亮度合适
def is_laserImage_proper(image):
    # 使用mask来设置圆形ROI
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask = cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
    newImage = cv2.add(image, np.zeros(np.shape(image), dtype=np.uint8), mask=mask)
    mean = cv2.mean(newImage, mask=mask)[0]
    mean = round(mean, 2)
    if LaserMeanThresh[0] < mean < LaserMeanThresh[1]:
        ret, BinaryReg = cv2.threshold(image, LaserThresh, 255, cv2.THRESH_BINARY)
        currArea = cv2.countNonZero(BinaryReg)
        if LaserAreaThresh[0] < currArea < LaserAreaThresh[1]:
            isProper = 1  # 激光图像亮度合适
        elif currArea <= LaserAreaThresh[0]:
            isProper = 0  # 激光图像太暗
        else:
            isProper = 2  # 激光图像太亮
    elif mean < LaserMeanThresh[0]:
        isProper = 0  # 激光图像太暗
    else:
        isProper = 2  # 激光图像太亮
    return isProper


def is_grayImage_proper(image):
    # 使用mask来设置圆形ROI
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    mask = cv2.circle(mask, (x, y), r, (255, 255, 255), -1)
    newImage = cv2.add(image, np.zeros(np.shape(image), dtype=np.uint8), mask=mask)
    mean = cv2.mean(newImage, mask=mask)[0]
    mean = round(mean, 2)  # 小数点后保留两位有效数字
    if GrayMeanThresh[0] < mean < GrayMeanThresh[1]:
        isProper = 1  # 灰度图像亮度合适
    elif mean < GrayMeanThresh[0]:
        isProper = 0  # 灰度图像太暗
    else:
        isProper = 2  # 灰度图像太亮
    return isProper


# # #  判断激光图像属性是否合格
# 激光图像路径
imagePath1 = 'E:/原木视觉测量/原木测量图像保存/光纹图像01/1576227768434.bmp'
# 读入图像
laserImage = read_image(imagePath1)
# 判断激光图像亮度是否合适
isLaserOK = is_laserImage_proper(laserImage)
print(isLaserOK)

# # #  判断灰度图像属性是否合格
# 灰度图像路径
imagePath2 = 'E:/原木视觉测量/原木测量图像保存/圆木图像01/1576377497223-900.bmp'
# 读入图像
grayImage = read_image(imagePath2)
# 判断灰度图像亮度是否合适
isGrayOK = is_grayImage_proper(grayImage)
print(isGrayOK)


# # 显示图像
# cv2.imshow('image', laserImage)
# K = cv2.waitKey(0)
