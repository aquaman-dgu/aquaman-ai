from flask import Flask, request, jsonify, render_template,Blueprint
import numpy as np
from PIL import Image
from io import BytesIO
import datetime
import random
import subprocess
import os
import sys
import json


bp= Blueprint('test',__name__,url_prefix='/')

#path adjusting
def get_path(path):
    change_path = path.replace("\\",'/')
    return change_path


@bp.route('/image' , methods=['POST'])
def showImage():
    # if request.method == 'POST':
    try:  
        print(request.form)
        
        global details
        details = request.form
        img_data = request.files['file']
        image = img_data.read()

        print(img_data)
        length = float(details['length'])
        weight = float(details['weight'])
        feed = float(details['feed'])
        
        print(length)
        print(weight)
        print(feed)

        # 성장 예측 모델
        growth_result = getGrowthModelResult(length, weight,feed)
        
        growth_result = str(growth_result)
        print("gr:" + growth_result)
        growth_result = eval(growth_result)
        flength = str(growth_result[0]) # 소수 첫째 자리 출력
        fweight = str(growth_result[1]) # 소수 첫째 자리 출력
        
        print("7일후 체장: "+ flength)
        print("7일후 체중: " + fweight)

            
        # spring boot로부터 받은 이미지 처리
        
        img_array = np.frombuffer(image, dtype=np.uint8)
        image = Image.open(BytesIO(img_array))
        # 유니크한 파일명 생성해서 이미지 static/img/파일명 저장
        img_name = uniquenumber()
        p = get_path("C:/Users/roger/aquaman-ai")
        os.chdir(p)
        print(img_name)
        image.save("./static/img/%s.jpg" % (img_name)) 
        
        # 질병 모델 돌리기
        print("=== recognition model start ===")

        recog_result = getRecongnitionModelResult(str(img_name))
        
        print("=== disease model start ===")
        desease_result = getDiseaseResult(recog_result)
        print("desease result: " + desease_result)
        message = "image respond succesfully"
        success = "success"
        response_data = {"status": success, "message": message, "value" : desease_result, "length" : flength , "weight" : fweight}
        
        print(response_data)
        return jsonify(response_data)
    except Exception as e:
        
        print(e)
        # 예외 처리
        error_data = {"status": "error", "message": str(e)}
        return jsonify(error_data), 500  # 500은 Internal Server Error를 나타냄
# else:
#     return jsonify(error_data), 500  # 500은 Internal Server Error를 나타냄


def uniquenumber():
    date_time = datetime.datetime.now()
    alist=[]
    for i in range(1):
        a = random.randint(1, 100)
        alist.append(a)
        while a in alist:
            a = random.randint(1, 100)
    alist.append(a)
    reg_num = (str(date_time.year) + str(date_time.month) + str(date_time.day) +str(date_time.second)+ str(a)) #  년도 + 월 + 일 + 초 + 1~100 난수
    return reg_num



def getRecongnitionModelResult(img_name):
    path = os.path.join(os.getcwd(), "recognition")
    print("현재 경로는: " + path)
    fpath = get_path(path)
    os.chdir(fpath)
    img = img_name+".jpg"
    cmd =['python','recognition_views.py','--test','%s' %(img)]
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True,encoding='UTF-8' ).stdout
    arr = []
    arr = fd_popen.read().split('\\')
    fd_popen.close()
    result = arr[0][0:len(img_name)]
    print("결과: " + result)
    return result


def getDiseaseResult(img_name):
    fpath = get_path("C:/Users/roger/aquaman-ai/disease")
    os.chdir(fpath)
    print("현재 경로는: " + fpath)
    cmd =['python','disease_views.py','--test','%s' %(img_name)]
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, encoding='utf-8').stdout
    data = fd_popen.read().strip()
    print("Data는 : " +  data)
    return img_name
    

def getGrowthModelResult(length, weight,feed):
    fpath = get_path("C:/Users/roger/aquaman-ai/growth-forecast")
    os.chdir(fpath)
    print("현재 경로는: " + fpath)
    cmd = ['python', 'growth_forecast_views.py', '--test', str(length), str(weight), str(feed)]
    result = subprocess.check_output(cmd, shell=True, encoding='utf-8' )
    return result
