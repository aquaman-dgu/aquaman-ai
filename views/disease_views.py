from flask import Flask, request, Blueprint, jsonify
import os
from ultralytics import YOLO
from PIL import Image
import base64
from io import BytesIO
import shutil

bp= Blueprint('disease',__name__,url_prefix='/')


# 모델의 weight path
model_path = os.path.join(bp.root_path + "\\models\\", "disease.pt")
disease =  YOLO(model_path)

# static folder의 path
temp_list = bp.root_path.split("\\")
base_path = ""
for i in range(len(temp_list) - 1) :
    base_path += temp_list[i] + "\\"

# 이미지가 save 될 path
save_path = base_path + "disease\\"

def resize_image(input_path, output_path, target_size=(640, 640), fill_color=(255, 255, 255)):
    try:
        # 이미지 열기
        original_image = Image.open(input_path)

        # 현재 크기 얻기
        width, height = original_image.size

        # 이미지를 target_size로 확장
        new_image = Image.new("RGB", target_size, fill_color)
        new_image.paste(original_image, ((target_size[0] - width) // 2, (target_size[1] - height) // 2))

        # 새 이미지 저장
        new_image.save(output_path)
        print(f"Image resized and saved to {output_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def move_jpg_files_and_delete_subfolders(folder_path):
    # 폴더 내 모든 파일과 하위 폴더 목록 가져오기
    items = os.listdir(folder_path)

    for item in items:
        item_path = os.path.join(folder_path, item)

        # 폴더인지 파일인지 확인
        if os.path.isdir(item_path):
            # 하위 폴더 내 모든 파일 목록 가져오기
            subfolder_items = os.listdir(item_path)

            for subfolder_item in subfolder_items:
                if subfolder_item.lower().endswith('.jpg'):
                    # jpg 파일을 'A' 폴더로 이동
                    source_file_path = os.path.join(item_path, subfolder_item)
                    destination_file_path = os.path.join(folder_path, subfolder_item)
                    shutil.move(source_file_path, destination_file_path)

            # 하위 폴더 삭제
            shutil.rmtree(item_path)
            
def convert_images_to_base64(folder_path):
    image_data = {}
    
    # 폴더 내 모든 파일 목록 가져오기
    files = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]
    
    for idx, file in enumerate(files, start=1):
        file_path = os.path.join(folder_path, file)
        
        with open(file_path, 'rb') as image_file:
            # 이미지 파일을 읽어서 BytesIO로 변환
            image_bytesio = BytesIO(image_file.read())
            
            # BytesIO에서 Base64로 인코딩
            encoded_image = base64.b64encode(image_bytesio.getvalue()).decode('utf-8')
            
            # '개체1', '개체2', ..., '개체N' 형식의 키로 데이터에 추가
            key = f'개체{idx}'
            image_data[key] = encoded_image

    return image_data

@bp.route('/disease')
def print_root() :
    return base_path


@bp.route('/disease/predict', methods=['GET'])
def predict():
    folder_name = request.args.get('folder_name', '')
    
    # recognition이 자른 사진들이 존재하는 path
    path_name = base_path + "recognition\\" + folder_name + "\\crops\\넙치"
    
    # 사진들의 이름 list  
    crops_list = os.listdir(path_name)
    
    # 사진들을 640x640으로 resizing해서 저장하는 경로
    folder_path = save_path + folder_name + "\\resized"
    if not os.path.exists(folder_path) :
        os.makedirs(folder_path)
    
    for item in crops_list :
        resize_image(path_name + "\\" + item, folder_path + "\\" + item)
        
    
    if not folder_name :
        return "URL 매개변수 'image_name'에 이미지 이름을 제공해주세요.", 400

    try:
        for item in crops_list :
            result = disease.predict(folder_path + "\\" + item, save = True, retina_masks=True, imgsz = 640, 
                               conf=0.7, project=save_path + folder_name + "\\disease", name='num')
        move_jpg_files_and_delete_subfolders(save_path + folder_name + "\\disease")
        images_data = convert_images_to_base64(save_path + folder_name + "\\disease")
        return jsonify({"images": images_data})
    

    except Exception as e:
        return f"예측 중 오류 발생: {str(e)}", 500
    
    

#if __name__ == '__main__':
#    app.run(debug=True)
