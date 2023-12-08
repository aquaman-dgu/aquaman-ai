from flask import Flask, request, Blueprint, jsonify
import os
import pandas as pd
import pickle
import xgboost


#app = Flask(__name__)
bp= Blueprint('growth_forecast',__name__,url_prefix='/')


# 모델의 weight path
length_path = os.path.join(bp.root_path + "\\models\\", "xgb_length.pkl")
with open(length_path, 'rb') as file:
    length = pickle.load(file)
    
weight_path = os.path.join(bp.root_path + "\\models\\", "xgb_weight.pkl")
with open(weight_path, 'rb') as file:
   weight = pickle.load(file)

@bp.route('/growth_forecast/predict', methods=['GET'])
def predict():
    current_length = float(request.args.get('current_length', 0.0))
    current_weight = float(request.args.get('current_weight', 0.0))
    current_feed = float(request.args.get('current_weight', 0.0))
    
    length_df = pd.DataFrame(columns=['체장(mm)', '체중(g)', '개별 사료 급이량(g)'])

    '7일 후 체장(mm)'
    length_df.loc[0] = [current_length, current_weight, current_feed]
    weight_df = length_df.copy()
    
    future_length = length.predict(length_df)
    weight_df['7일 후 체장(mm)'] = future_length
    future_weight = weight.predict(weight_df)
    
    
    return jsonify({"7일 후 체장(mm)" : float(future_length[0]), "7일 후 체중(g)" : float(future_weight[0])})

#if __name__ == '__main__':
#    app.run(debug=True)
