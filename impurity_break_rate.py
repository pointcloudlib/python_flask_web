import os
import pandas as pd
import xlwt
import cv2
import Pixel_area_actual_quality
import numpy as np


def fix(datas):
    result = []
    for i in range(len(datas)):
        if datas[i] == 0:
            result.append(0)
        else:
            result.append(str(round(datas[i] * 100, 3)) + '%')

    return result


def cal_result(data_dict):
    # quality_green

    result_dict = {}

    green_result = []
    blue_result = []
    yellow_result = []
    all_result = []
    break_result = []
    quality_red = np.array(data_dict['原料蔗质量'])
    quality_green = np.array(data_dict['蔗叶质量'])
    quality_blue = np.array(data_dict['蔗梢质量'])
    quality_yellow = np.array(data_dict['破损质量'])

    quality_red_yellow = quality_red + quality_yellow

    quality_sum = []
    quality_sum.append(quality_green)
    quality_sum.append(quality_blue)
    quality_sum.append(quality_yellow)
    quality_sum.append(quality_red)
    quality_sum = np.array(quality_sum)

    quality_sum = np.sum(quality_sum, axis=0)
    green_result = quality_green / quality_sum
    blue_result = quality_blue / quality_sum
    yellow_result = quality_yellow / quality_sum
    break_result = quality_yellow / quality_red_yellow
    sum_impurity = green_result + blue_result + yellow_result

    green_result = fix(green_result)
    blue_result = fix(blue_result)
    yellow_result = fix(yellow_result)
    break_result = fix(break_result)
    sum_impurity = fix(sum_impurity)

    result_dict['图像索引'] = data_dict['图像索引']
    result_dict['蔗叶含杂率'] = green_result
    result_dict['蔗梢含杂率'] = blue_result
    result_dict['破损含杂率'] = yellow_result
    result_dict['总含杂率'] = sum_impurity
    result_dict['总破损率'] = break_result

    return result_dict


if __name__ == '__main__':
    jpgs_path = "datasets/JPEGImages"
    pngs_path = "datasets/SegmentationClass"
    save_excel_path = './含杂_破损率.xls'
    data = Pixel_area_actual_quality.count(pngs_path)
    result = cal_result(data)
    Pixel_area_actual_quality.write_data(save_excel_path, result)
