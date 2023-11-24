from flask import Flask, request, jsonify, render_template,Blueprint
import numpy as np
from PIL import Image
from io import BytesIO
import datetime
import random


bp= Blueprint('test',__name__,url_prefix='/')

@bp.route('/image' , methods=['POST'])
def showImage():
    if request.method == 'POST':
        try:  
            print(request.form)
            
            # spring boot로부터 받은 이미지 처리리
            img_data = request.data
            img_array = np.frombuffer(img_data, dtype=np.uint8)
            image = Image.open(BytesIO(img_array))
            
            # 유니크한 파일명
            img_name = uniquenumber()
            print(img_name)
            image.save("./static/img/%s.jpg" % (img_name))
            
            success = "success"
            message = "Image received successfully"
            response_data = {"status": success, "message": message}
            return jsonify(response_data)
        except Exception as e:
            
            print("error: " + e)
            # 예외 처리
            error_data = {"status": "error", "message": str(e)}
            return jsonify(error_data), 500  # 500은 Internal Server Error를 나타냄
    else:
        return jsonify(error_data), 500  # 500은 Internal Server Error를 나타냄


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