import xlwt
import cv2
import os
import pandas as pd
import numpy as np


# 计算面积
def count_area_and_c(img_bin):
    c = 0
    s = 0
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT, (15, 15))  # 构造一个用于形态学使用的核函数，
    binary = cv2.morphologyEx(img_bin, cv2.MORPH_OPEN, kernel)
    image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 边缘
    if len(contours) > 0:
        for i in range(len(contours)):
            s += cv2.contourArea(contours[i])
    return c, s


def count(path):
    '''
    计算面积
    :param path: 
    :return: 面积
    '''

    BLUE = 15  # 蔗梢
    RED = 38  # 原料蔗
    GREEN = 75  # 蔗叶
    YELLOW = 113  # 破损

    data_dict = {}
    image_name = []  # 存放文件名
    # areas_blue = []  # 15
    # areas_red = []  # 38
    # areas_green = []  # 75
    # areas_yellow = []  # 113
    counts_red = []
    counts_green = []
    counts_yellow = []
    counts_blue = []

    print('len', len(os.listdir(path)))

    for id in os.listdir(path):
        print(id)
        image_name.append(id)
        # 初始化
        area_red = 0
        area_green = 0
        area_yellow = 0
        area_blue = 0
        count_red = 0
        count_green = 0
        count_yellow = 0
        count_blue = 0

        image_path = os.path.join(path, id)
        # print('image_path', image_path)
        image = cv2.imread(image_path)  # 读入图片
        # cv2.imshow("image", image)
        # cv2.waitKey(0)
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 转化成灰度图像
        for i in range(len(img_gray)):  # 计算某类别颜色区域像素和
            for j in range(len(img_gray[i])):
                if img_gray[i][j] == RED:
                    count_red += 1
                elif img_gray[i][j] == GREEN:
                    count_green += 1
                elif img_gray[i][j] == YELLOW:
                    count_yellow += 1
                elif img_gray[i][j] == BLUE:
                    count_blue += 1

        ret_y, img_bin_yellow = cv2.threshold(img_gray, YELLOW - 1, 255, cv2.THRESH_BINARY)
        ret_g, img_bin_green = cv2.threshold(img_gray, GREEN - 1, 255, cv2.THRESH_BINARY)
        ret_r, img_bin_red = cv2.threshold(img_gray, RED - 1, 255, cv2.THRESH_BINARY)
        ret_b, img_bin_blue = cv2.threshold(img_gray, BLUE - 1, 255, cv2.THRESH_BINARY)

        # cv2.imshow("images",img_gray)

        yellow_c, yellow_s = count_area_and_c(img_bin_yellow)
        green_c, green_s = count_area_and_c(img_bin_green)
        red_c, red_s = count_area_and_c(img_bin_red)
        blue_c, blue_s = count_area_and_c(img_bin_blue)

        # 确定面积
        area_yellow = yellow_s
        area_green = green_s - yellow_s
        area_red = red_s - green_s
        area_blue = blue_s - red_s

        # areas_red.append(area_red)
        # areas_green.append(area_green)
        # areas_yellow.append(area_yellow)
        # areas_blue.append(area_blue)
        counts_red.append(count_red)
        counts_green.append(count_green)
        counts_yellow.append(count_yellow)
        counts_blue.append(count_blue)
    # 图像中各类别的实际质量
    quality_red = list(map(f_x, counts_red))
    quality_green = list(map(f_x, counts_green))
    quality_yellow = list(map(f_x, counts_yellow))
    quality_blue = list(map(f_x, counts_blue))

    data_dict['图像索引'] = image_name
    # data_dict['areas_red'] = areas_red
    # data_dict['areas_green'] = areas_green
    # data_dict['areas_yellow'] = areas_yellow
    # data_dict['areas_blue'] = areas_blue
    data_dict['原料蔗面积'] = counts_red
    data_dict['原料蔗质量'] = quality_red
    data_dict['蔗叶面积'] = counts_green
    data_dict['蔗叶质量'] = quality_green
    data_dict['蔗梢面积'] = counts_blue
    data_dict['蔗梢质量'] = quality_blue
    data_dict['破损面积'] = counts_yellow
    data_dict['破损质量'] = quality_yellow

    return data_dict


# 像素面积与质量的拟合方程
def f_x(x):
    if x == 0:
        return 0
    return round(8.559e-05 * x + 0.3689, 3)


# 用字典的方法存入excel表中
def write_data(save_excel_path, data_dict):
    data = pd.DataFrame(data_dict)
    data.to_excel(save_excel_path, index=False)


def main():
    path = 'static/segmentation'  # 图片存放的文件路径
    save_excel_path = './像素面积表.xls'
    data_dict = count(path)
    write_data(save_excel_path, data_dict)

# if __name__ == '__main__':
#     main()
