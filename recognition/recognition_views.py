import os
import base64
from ultralytics import YOLO
from io import BytesIO
import argparse

# parser 등록
parser = argparse.ArgumentParser(description='Argparse Tutorial')
parser.add_argument('--test', default='sample1.jpg',help='test image data')
opt = parser.parse_args()

print(opt.test)


# 모델의 weight path
# 모델 테스팅 경로
# model_path = os.path.join("recognition\\models\\", "recognition.pt")

# test_views api 테스팅 경로
model_path = os.path.join("models\\", "recognition.pt")

recog =  YOLO(model_path)

# 이미지가 save 될 path
save_path = os.getcwd()

print(save_path)
# 이미지를 불러올 path
base_path = '..\\static\\img\\'

def convert_images_to_base64(folder_path):
    image_data = {}
    print("여기까지")
    print(folder_path)
    
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
            key = f'fish{idx}'
            image_data[key] = encoded_image

    return image_data

def predict(image_name : str):
    image_list = []
    path_name = base_path + image_name
    
    if not image_name:
        return "이미지가 올바르지 않습니다."

    try:
        result = recog.predict(path_name, save = True, retina_masks=True, imgsz = 1280, 
                               conf=0.7, save_crop=True, project=save_path, name=image_name[:-4])
        image_data = convert_images_to_base64(save_path + "\\" + image_name[:-4])


    except Exception as e:
        return f"예측 중 오류 발생: {str(e)}"
    
    return image_data

def main():
    
    # test_views에서 테스트
    file = str(opt.test)
    predict(file)
    
    # 모델 테스트
    # predict("sample1.jpg")

if __name__ == "__main__":

    main()