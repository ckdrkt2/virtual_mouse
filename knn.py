from tslearn.clustering import TimeSeriesKMeans
from tslearn.generators import random_walks
import pandas as pd

a = pd.read_csv('test.csv')

# print(a)

km = TimeSeriesKMeans(n_clusters=5, 
                      metric="dtw", 
                      max_iter=5,
                      random_state=42)
prediction = km.fit_predict(a)

print(prediction)