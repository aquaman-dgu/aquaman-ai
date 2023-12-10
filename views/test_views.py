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
        
        # spring boot로부터 받은 이미지 처리
        img_data = request.data
        img_array = np.frombuffer(img_data, dtype=np.uint8)
        image = Image.open(BytesIO(img_array))
        
        # 유니크한 파일명 생성해서 이미지 static/img/파일명 저장
        img_name = uniquenumber()
        p = get_path("C:/Users/roger/aquaman-ai")
        os.chdir(p)
        print(img_name)
        image.save("./static/img/%s.jpg" % (img_name)) 
        
        # 질병 모델 돌리기
        print("=== recognition model start ===")

        result = getRecongnitionModelResult(img_name)
        print(result)
        
        
        success = "success"
        message = "Image received successfully"
        response_data = {"status": success, "message": message}
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
    cmd =['python','recognition_views.py','--test','%s' %(str(img_name))]
    

    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True ).stdout
   
    ## 여기가 에러
    stdout_data = fd_popen.read().split(":")

    # 파일을 닫음 (중요)
    fd_popen.close()


    

def getDiseaseResult(img_name):
    cmd =['python','disease_views.py','--test','%s' %(img_name), '--option'  , '%s' %('modeling')]
    fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True).stdout
    data = fd_popen.read().strip()
    print("Data는 : " +  data)
    
if __name__ == "__main__":

    getRecongnitionModelResult("202312105150.jpg")