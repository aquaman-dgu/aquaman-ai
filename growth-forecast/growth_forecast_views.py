import pandas as pd
import pickle
import xgboost
import argparse



with open('./model/xgb_length.pkl', 'rb') as file:
    length = pickle.load(file)
    
with open('./model/xgb_weight.pkl', 'rb') as file:
   weight = pickle.load(file)

def predict(current_length, current_weight, current_feed):
    current_length = float(current_length)
    current_weight = float(current_weight)
    current_feed = float(current_feed)
    
    length_df = pd.DataFrame(columns=['체장(mm)', '체중(g)', '개별 사료 급이량(g)'])

    length_df.loc[0] = [current_length, current_weight, current_feed]
    weight_df = length_df.copy()
    
    future_length = length.predict(length_df)
    weight_df['7일 후 체장(mm)'] = future_length
    future_weight = weight.predict(weight_df)
    
    list = [future_length[0], future_weight[0]]
    print(list)
def main():
    
    parser = argparse.ArgumentParser(description='Growth Forecast Views')
    parser.add_argument('--test', nargs=3, type=float, help='Test arguments (length weight feed)', required=True)
    opt = parser.parse_args()
    
    length, weight, feed = opt.test
    predict(length,weight,feed)
    
if __name__ == "__main__":
    main()