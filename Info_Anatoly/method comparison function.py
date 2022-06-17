from sklearn.neighbors import KNeighborsRegressor
import pandas
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import KFold
from sklearn import datasets, linear_model
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import scale
from sklearn.ensemble import RandomForestRegressor
import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import log_loss
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import PassiveAggressiveRegressor


msft = yf.Ticker("MSFT")
print(msft)
data = yf.download("AAPL", start="2000-08-01", end="2017-09-01")
data_test = yf.download("AAPL", start="2018-08-01", end="2019-09-01")
print (data)
X = data[['Open', 'High', 'Low']]
y = data['Close']

X_test = data_test[['Open', 'High', 'Low']]
y_test = data_test['Close']

'''
def Training(method,x,y) -> str:
	rfc=RandomForestRegressor(n_estimators=10, random_state=241)
	knn=KNeighborsRegressor(n_neighbors=5)
	PAR=PassiveAggressiveRegressor(max_iter=100, random_state=0)
	lr=LinearRegression()

	if (method == 'rfc'):
		rfc.fit(X,y)
		pred = rfc.predict(X_test)
		answer = mean_squared_error(y_test, pred)
	if (method == 'knn'):
		knn.fit(X,y)
		pred = knn.predict(X_test)
		answer = mean_squared_error(y_test, pred)
	if (method == 'PAR'):
		PAR.fit(X,y)
		pred = PAR.predict(X_test)
		answer = mean_squared_error(y_test, pred)
	if (method == 'lr'):
		lr.fit(X,y)
		pred = lr.predict(X_test)
		answer = mean_squared_error(y_test, pred)
	return answer
	
print('Введите метод')
method = input()
print(Training(method))
'''



dictionary = {'rfc': 'RandomForestRegressor', 'knn': 'KNeighborsRegressor','PAR': 'PassiveAggressiveRegressor','lr': 'LinearRegression'}
m = input()
new_m = dictionary.get(m)
new_m.fit(X,y)
pred = new_m.predict(X_test)
nswer = mean_squared_error(y_test, pred)
print(answer)