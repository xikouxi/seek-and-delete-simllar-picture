# -*- coding: utf-8 -*-

from compiler.ast import flatten
import cv2
import numpy as np
import os

def pHash(imgfile):
    # 加载并调整图片为32x32灰度图片
    img = cv2.imread(imgfile, 0)
    img = cv2.resize(img, (32, 32), interpolation=cv2.INTER_CUBIC)

    # 创建二维列表
    h, w = img.shape[:2]
    vis0 = np.zeros((h, w), np.float32)
    vis0[:h, :w] = img  # 填充数据

    # 二维Dct变换
    vis1 = cv2.dct(cv2.dct(vis0))
    # 拿到左上角的8 * 8
    vis1 = vis1[0:8, 0:8]

    # 把二维list变成一维list
    img_list = flatten(vis1.tolist())

    # 计算均值
    avg = sum(img_list) * 1. / len(img_list)
    avg_list = ['0' if i < avg else '1' for i in img_list]

    # 得到哈希值
    return ''.join(['%x' % int(''.join(avg_list[x:x + 4]), 2) for x in range(0, 8 * 8, 4)])


def getHamming(diff=[], diff2=[]):  # 计算两点间汉明距离
    hamming_distance = 0
    for i in range(len(diff)):
        if diff[i] != diff2[i]:
            hamming_distance += 1

    return hamming_distance

if __name__ == '__main__':
    path = r'hashquchong'#图片位置
    img_path = path
    imgs_n = []
    num = []
    img_files = [os.path.join(rootdir, file) for rootdir, _, files in os.walk(path) for file in files if
                 (file.endswith('.jpg'))]
    for currIndex, filename in enumerate(img_files):
        if not os.path.exists(img_files[currIndex]):
            print 'not exist', img_files[currIndex]
            break
        img = pHash(img_files[currIndex])
        img1 = pHash(img_files[currIndex + 1])
        hanming = getHamming(img, img1)
        if hanming <= 5:
            imgs_n.append(img_files[currIndex + 1])
            print img_files[currIndex], img_files[currIndex + 1], hanming
        else:
            print 'hanming',img_files[currIndex], img_files[currIndex + 1], hanming
        currIndex += 1
        if currIndex >= len(img_files)-1:
            break
    for image in imgs_n:
        os.remove(image)
