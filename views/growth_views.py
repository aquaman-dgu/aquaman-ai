#from flask import Blueprint, request, jsonify
import pandas as pd
import pickle
import xgboost

#bp = Blueprint('growth-forecast', __name__, url_prefix='/')

# xgb_length.pkl의 상대 경로 계산
path1 = '../growth-forecast/model/xgb_length.pkl' 
classify_path1 = '/app/growth-forecast/model/xgb_length.pkl'

# xgb_weight.pkl의 상대 경로 계산
path2 = '../growth-forecast/model/xgb_weight.pkl' 
classify_path2 = '/app/growth-forecast/model/xgb_weight.pkl'

# 예측에 사용될 XGBoost 회귀 모델
with open(classify_path1, 'rb') as model_file:
    xgboost1 = pickle.load(model_file)
    
with open(classify_path2, 'rb') as model_file:
    xgboost2 = pickle.load(model_file)
    
# 입력 값
length = float()
weight = float()
feeder = float()

X_user = pd.DataFrame({
    '체장(mm)': [length],
    '체중(g)': [weight],
    '개별 사료 급이량(g)': [feeder]
})

@bp.route('/growth-forecast', methods=['POST'])
def growth_forecast():
    # 첫 번째 예측
    predicted_length = xgboost1.predict(X_user)
    X_user['7일 후 체장(mm)'] = predicted_length

    # 두 번째 예측
    predicted_weight = xgboost2.predict(X_user)
    
    results = [
    "현재 체장: {} mm".format(length),
    "현재 체중: {} g".format(weight),
    "개별 사료 급이량: {} g".format(feeder),
    "7일 후 예상 체장: {} mm".format(predicted_length[0]),
    "7일 후 예상 체중: {} g".format(predicted_weight[0])
    ]

    # return results[체장, 체중, 개별 사료 급이량, 7일 후 체장(mm), 7일 후 체중(g)]
    

