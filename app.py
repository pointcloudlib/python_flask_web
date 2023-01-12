from urllib import request
from flask import Flask, jsonify
from flask import render_template, request
import sqlite3
import Pixel_area_actual_quality
import impurity_break_rate
import numpy as np
import os
import pandas as pd
import xlwt
import cv2

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

data_dict = {}
result_dict = {}


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/word')
def word():
    return render_template('picture.html')


@app.route('/word', methods=['POST'])
def success():
    if request.method == 'POST':
        objFile = request.files.get('file')
        strFileName = objFile.filename
        strFilePath = "./static/segmentation/" + strFileName
        objFile.save(strFilePath)
        return render_template('picture.html')


@app.route('/movie', methods=['POST'])
def test():
    path = 'static/segmentation'
    global data_dict, result_dict
    data_dict = Pixel_area_actual_quality.count(path)
    result_dict = impurity_break_rate.cal_result(data_dict)
    # dataList存质量，dataRateList存率
    datalist = []
    dataRateList = []
    image_name = data_dict['图像索引']
    quality_green = data_dict['蔗叶质量']
    quality_blue = data_dict['蔗梢质量']
    quality_yellow = data_dict['破损质量']
    quality_red = data_dict['原料蔗质量']

    sum_impurity = result_dict['总含杂率']
    break_result = result_dict['总破损率']

    for i in range(len(image_name)):  # 每一行的内容
        data = []
        data.append(image_name[i])
        data.append(quality_red[i])
        data.append(quality_green[i])
        data.append(quality_blue[i])
        data.append(quality_yellow[i])
        data.append(sum_impurity[i])
        data.append(break_result[i])
        datalist.append(data)

    return render_template('count.html', movies=datalist)


@app.route('/team')
def team():
    return render_template('video.html')


@app.route('/movie')
def movie():
    datalist = []
    return render_template('count.html', movies=datalist)


def str2num(data):
    if data == 0:
        return 0
    return float(data[:-1])


@app.route('/score')
def score():
    global data_dict, result_dict
    image_name = result_dict['图像索引']
    sum_impurity = result_dict['总含杂率']
    break_result = result_dict['总破损率']
    sum_impurity = list(map(str2num, sum_impurity))
    break_result = list(map(str2num, break_result))
    print('data', image_name, sum_impurity, break_result)
    return render_template('view.html', image_name=image_name, sum_impurity=sum_impurity, break_result=break_result)


@app.route('/save', methods=['GET', 'POST'])
def save_excel():
    global data_dict, result_dict
    save_dict = {}
    save_dict.update(data_dict)
    save_dict.update(result_dict)
    save_excel_path = './数据导出.xls'
    Pixel_area_actual_quality.write_data(save_excel_path, save_dict)
    return render_template('count.html')


if __name__ == '__main__':
    app.run()
