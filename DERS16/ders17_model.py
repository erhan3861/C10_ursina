# model.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

class GoalkeeperModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        

    def train(self):
        X, y = self.load_data()
        if X is not None and y is not None:
            self.model.fit(X, y)

        
    def predict(self, X):
        predictions = self.model.predict(X)
        reaction_time = predictions[0][0]
        direction = predictions[0][1]

        return round(reaction_time,3), round(direction)
    
    def save_model(self):
        """
        .pkl uzantılı dosyalar, Python'un pickle modülü 
        veya joblib kütüphanesi kullanılarak oluşturulmuş 
        serileştirilmiş (pickle) dosyalardır. 
        
        Serileştirme, bir Python nesnesinin bayt dizisi halinde 
        saklanması ve daha sonra bu bayt dizisinden 
        orijinal nesnenin yeniden oluşturulması işlemidir.
        """
        joblib.dump(self.model, 'goalkeeper_model.pkl')
        
    def load_model(self):
        self.model = joblib.load('goalkeeper_model.pkl')

    def save_data(self, click_position, reaction_time, direction):
        data = {
            'click_x': [round(click_position[0],3)],
            'click_y': [round(click_position[1],3)],
            'click_z': [round(click_position[2],3)],
            'reaction_time': [reaction_time],
            'direction': [direction]
        }
        df = pd.DataFrame(data)
        
        if not os.path.isfile('goalkeeper_data.csv'):
            df.to_csv('goalkeeper_data.csv', index=False)
        else:
            df.to_csv('goalkeeper_data.csv', mode='a', header=False, index=False)

    def load_data(self):
        if os.path.isfile('goalkeeper_data.csv'):
            data = pd.read_csv('goalkeeper_data.csv')
            X = data[['click_x', 'click_y', 'click_z']].values
            y = data[['reaction_time', 'direction']].values
            return X, y
        else:
            return None, None

# Örnek veri oluşturma ve model eğitimi
if __name__ == "__main__":
    model = GoalkeeperModel()
    model.train()
    model.save_model()
