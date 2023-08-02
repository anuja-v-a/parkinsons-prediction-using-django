import pandas as pd
data=pd.read_csv('parkinsons.csv')
import pickle
data=data.drop('name',axis=1)
data=data.drop(['MDVP:Fhi(Hz)',
'MDVP:Jitter(%)',
'MDVP:RAP',
'MDVP:PPQ', 'Jitter:DDP',
'Shimmer:APQ3', 'Shimmer:APQ5','NHR'
],axis=1)
X = data.drop('status', axis=1)
Y = data['status']
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
from xgboost import XGBClassifier
model5 = XGBClassifier()
svm=model5.fit(X_train, Y_train)
pickle.dump(svm, open('park.pkl', 'wb'))
 