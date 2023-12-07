import pandas as pd
import pickle
import xgboost

# 예측에 사용될 XGBoost 회귀 모델
with open('./growth-forecast/model/xgb_length.pkl', 'rb') as file:
    xgboost1 = pickle.load(file)
    
with open('./growth-forecast/model/xgb_weight.pkl', 'rb') as file:
    xgboost2 = pickle.load(file)

# OS 양식장을 test 양식장으로 선정
data1 = pd.read_csv("./growth-forecast/csv/OS_data.csv")
data2 = pd.read_csv("./growth-forecast/csv/IC_data.csv")
data3 = pd.read_csv("./growth-forecast/csv/HM_data.csv")
data4 = pd.read_csv("./growth-forecast/csv/TP_data.csv")
data5 = pd.read_csv("./growth-forecast/csv/GM_data.csv")

# 데이터 준비
df_list = [data2, data3, data4, data5]
df_test = data1
train_data = pd.concat(df_list).sample(frac=1).reset_index(drop=True)
test_data = df_test.copy()

# 첫 번째 예측
X_test = test_data[['체장(mm)','체중(g)','개별 사료 급이량(g)']]
prediction1 = xgboost1.predict(X_test)
test_data['7일 후 체장(mm)'] = prediction1

# 두 번째 예측
X_test['7일 후 체장(mm)'] = prediction1
prediction2 = xgboost2.predict(X_test)
test_data['7일 후 체중(g)'] = prediction2

#결과 출력
print(test_data)